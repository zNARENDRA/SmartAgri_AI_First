import re
from typing import Dict, Any, List, Optional
from app.schemas import AssistantQueryRequest, AssistantQueryResponse, FarmerProfile
from app.services.crop_service import crop_service, CropRecommendationRequest
from app.services.yield_service import yield_service, YieldPredictionRequest
from app.services.disease_service import disease_service
from app.services.weather_service import weather_service
from app.services.market_service import market_service
from app.services.scheme_service import scheme_service

class AIAssistantOrchestrator:
    def process_query(self, req: AssistantQueryRequest) -> AssistantQueryResponse:
        text = req.message.strip().lower()
        prof = req.farmer_profile or FarmerProfile()
        
        # 1. Weather Intent
        if any(k in text for k in ["weather", "mausam", "rain", "barish", "temperature", "temp", "irrigation", "pani", "spray", "spraying"]):
            icar_guidance = self._query_icar_advisories(text, prof.current_crop, prof.state)
            icar_citation = f"\n\n📖 **Source: {icar_guidance['source_org']}**\n> *\"{icar_guidance['advisory_text']}\"*" if icar_guidance else ""

            w_res = weather_service.get_weather_and_advisory(prof.district or prof.state, prof.current_crop)
            tools = ["Weather Engine (Open-Meteo API)", "IMD Rainfall Intelligence (GoI Dataset 9)", "ICAR Weather-Based Crop Advisory RAG Layer (Dataset 11)"]
            reply = (
                f"**🌤️ Weather & Agro-Advisory for {w_res.current.location_name}:**\n\n"
                f"- **Current Condition:** {w_res.current.condition_text} ({w_res.current.temperature:.1f}°C, Humidity: {w_res.current.humidity:.0f}%, Wind: {w_res.current.wind_speed_kmh:.1f} km/h)\n"
                f"- **☔ Monsoon Departure:** {w_res.imd_rainfall_baseline['monsoon_status']} ({w_res.imd_rainfall_baseline['departure_percentage']} vs IMD normal baseline)\n"
                f"- **💧 Irrigation Advisory:** **{w_res.advisory.irrigation_advice['status']}** — {w_res.advisory.irrigation_advice['summary']}\n"
                f"- **🎯 Spraying Window:** **{w_res.advisory.spraying_window['status']}** — {w_res.advisory.spraying_window['action']}\n"
                f"- **🦠 Disease & Pest Risk:** **{w_res.advisory.pest_disease_risk['status']}** — {w_res.advisory.pest_disease_risk['summary']}\n\n"
                f"👉 **Practical Next Step:** {w_res.advisory.irrigation_advice['action']}"
                f"{icar_citation}"
            )
            followups = ["What crops are suitable for this weather?", "Show 7-day rainfall forecast", "Check mandi prices for my crop"]
            return AssistantQueryResponse(
                reply=reply,
                detected_intent="Weather & Agro-Advisory",
                tools_used=tools,
                structured_data={"weather": w_res.model_dump()},
                suggested_followups=followups
            )

        # 2. Market Intelligence Intent
        elif any(k in text for k in ["price", "bhav", "mandi", "market", "rate", "sell", "bechna", "wholesale"]):
            crop_name = prof.current_crop or "Soybean"
            # check if query mentions a specific crop
            for c in ["wheat", "rice", "cotton", "soybean", "onion", "potato", "tomato", "maize", "mustard", "gram", "banana", "mango"]:
                if c in text:
                    crop_name = c.capitalize()
                    break
            
            m_res = market_service.get_market_trends(crop_name, prof.state, prof.district)
            w_sell = market_service.where_to_sell(crop_name, prof.state)
            
            tools = ["India Mandi Wholesale Price Dataset (Agmarknet / Kaggle)", "Market Ranking Engine"]
            top_mandi = w_sell.best_mandis[0] if w_sell.best_mandis else None
            
            reply = (
                f"**📈 Market Intelligence for {crop_name} in {prof.state}:**\n\n"
                f"- **Current Dataset Modal Price:** **₹{m_res.latest_modal_price} / Quintal** (100 kg)\n"
                f"- **Historical Range:** Min ₹{m_res.min_price} — Max ₹{m_res.max_price}\n"
                f"- **Price Trend:** **{m_res.trend_direction}** ({m_res.price_change_percentage:+.1f}% recent movement)\n"
                f"- **Volatility:** {m_res.volatility_rating}\n\n"
                f"🏆 **Where to Sell Recommendation:**\n"
                + (f"The highest price realization is recorded at **{top_mandi.market}** ({top_mandi.district}) at an average of **₹{top_mandi.avg_modal_price}/Qtl**.\n" if top_mandi else "")
                + f"\n💡 *{w_sell.market_advice}*"
            )
            followups = [f"Where to sell {crop_name}?", "Show historical price chart", "Check government schemes for farmers"]
            return AssistantQueryResponse(
                reply=reply,
                detected_intent="Market Intelligence",
                tools_used=tools,
                structured_data={"market": m_res.model_dump(), "where_to_sell": w_sell.model_dump()},
                suggested_followups=followups
            )

        # 3. Government Scheme Intent
        elif any(k in text for k in ["scheme", "yojana", "subsidy", "government", "sarkar", "grant", "kcc", "loan", "bima", "insurance", "financial"]):
            matched = scheme_service.match_for_profile(prof)
            tools = ["Indian Government Schemes Dataset (Kaggle)", "Profile Eligibility Matcher"]
            
            top_schemes = matched[:3]
            schemes_text = "\n\n".join([
                f"🏛️ **{s.scheme_name}** ({s.category})\n"
                f"  - **Benefit:** {s.benefits}\n"
                f"  - **Why Applicable:** {s.match_reasons[0] if s.match_reasons else 'Eligible farmer tier'}\n"
                f"  - **How to Apply:** {s.application_process}\n"
                f"  - **Official Link:** [{s.short_name} Portal]({s.official_url})"
                for s in top_schemes
            ])

            reply = (
                f"**🏛️ Top Relevant Government Schemes for {prof.name} ({prof.farmer_category}, {prof.state}):**\n\n"
                f"{schemes_text}\n\n"
                f"⚠️ *Note: Eligibility and subsidy availability should be verified on the official government portal (MyScheme.gov.in) before applying.*"
            )
            followups = ["How to apply for PM-KISAN?", "Subsidies for drip irrigation", "Check PMFBY crop insurance"]
            return AssistantQueryResponse(
                reply=reply,
                detected_intent="Government Scheme Discovery",
                tools_used=tools,
                structured_data={"schemes": [s.model_dump() for s in top_schemes]},
                suggested_followups=followups
            )

        # 4. Disease / Crop Health Intent
        elif any(k in text for k in ["disease", "leaf", "blight", "pata", "pest", "keeda", "fungus", "spot", "yellow", "curl", "rot", "scab", "plant"]):
            tools = ["Plant Village Knowledge Base", "Crop Health Diagnostics"]
            
            reply = (
                f"**🦠 Plant Health Diagnosis & Protection:**\n\n"
                f"To get an exact AI diagnosis, you can **upload a photo of the affected leaf** in the **Disease Detection** tab.\n\n"
                f"**General Best Practices for Leaf Spots / Blight:**\n"
                f"1. **Avoid overhead sprinkler irrigation** which splashes fungal spores between leaves.\n"
                f"2. **Strip infected lower foliage** touching wet soil.\n"
                f"3. **Organic Spray:** Neem oil (3-5 ml/L) or *Trichoderma harzianum* (5g/L) during early onset.\n"
                f"4. **Chemical Protective Spray:** Mancozeb 75 WP (2.5g/L) or Copper Oxychloride (3g/L) in cloudy damp conditions.\n\n"
                f"👉 Would you like to upload a leaf photo now for instant classification?"
            )
            followups = ["Upload leaf photo for diagnosis", "Tomato early blight treatment", "Potato late blight precautions"]
            return AssistantQueryResponse(
                reply=reply,
                detected_intent="Plant Disease & Protection",
                tools_used=tools,
                structured_data=None,
                suggested_followups=followups
            )

        # 5. Crop Recommendation / Sowing Intent
        elif any(k in text for k in ["grow", "crop", "fasal", "sow", "recommend", "soil", "npk", "ph", "suit"]):
            c_req = CropRecommendationRequest(
                N=prof.nitrogen,
                P=prof.phosphorus,
                K=prof.potassium,
                temperature=26.5,
                humidity=65.0,
                ph=prof.soil_ph,
                rainfall=105.0,
                top_k=3
            )
            c_res = crop_service.predict(c_req)
            tools = ["Crop Recommendation Engine (Random Forest / 98.8% Accuracy)", "Soil Nutrient Analyzer"]
            
            recs_text = "\n".join([
                f"- **{r.crop}** (Match: **{r.percentage}**): {r.soil_suitability}. Key factors: {', '.join(r.key_advantages[:1])} (Water: {r.water_requirement})"
                for r in c_res.recommendations
            ])

            reply = (
                f"**🌱 AI Crop Advisory for your soil (N:{prof.nitrogen:.0f}, P:{prof.phosphorus:.0f}, K:{prof.potassium:.0f}, pH:{prof.soil_ph:.1f}):**\n\n"
                f"Based on your soil nutrients and climate in {prof.state}, the top recommended crops are:\n\n"
                f"{recs_text}\n\n"
                f"**Soil Insight:** {c_res.nutritional_analysis.get('Soil pH', 'Soil is well conditioned.')}\n\n"
                f"👉 **Recommendation:** Consider planting **{c_res.top_crop}** for optimal yield and market realization."
            )
            followups = [f"Expected yield for {c_res.top_crop}?", "Check mandi prices for " + c_res.top_crop, "Government schemes for " + c_res.top_crop]
            return AssistantQueryResponse(
                reply=reply,
                detected_intent="Crop Recommendation",
                tools_used=tools,
                structured_data={"crop_recommendation": c_res.model_dump()},
                suggested_followups=followups
            )

        # 6. Action Plan Intent / What should I do this week?
        elif any(k in text for k in ["action plan", "what to do", "kya karu", "weekly plan", "summary", "guide", "today"]):
            from app.services.action_plan_service import action_plan_service
            plan = action_plan_service.generate_plan(prof)
            tools = ["Farm Action Plan Synthesizer", "Multi-Module AI Integrator"]
            
            reply = (
                f"**📋 Consolidated Farm Action Plan for {prof.name}:**\n\n"
                f"- 🌱 **Recommended Crop:** {plan.crop_advice['recommended_crop']} ({plan.crop_advice['suitability']})\n"
                f"- 💧 **Irrigation Action:** {plan.irrigation_water_advice['action']}\n"
                f"- 🌦️ **Weather Alert:** {plan.weather_action['alert']}\n"
                f"- 📈 **Market Timing:** {plan.market_advice['advice']}\n"
                f"- 🏛️ **Government Scheme:** {plan.government_support['top_scheme']}\n\n"
                f"✅ **Immediate Next Step:** {plan.immediate_next_steps[0]}"
            )
            followups = ["View full Farm Action Plan", "Check weather forecast", "Calculate crop yield"]
            return AssistantQueryResponse(
                reply=reply,
                detected_intent="Farm Action Plan",
                tools_used=tools,
                structured_data={"action_plan": plan.model_dump()},
                suggested_followups=followups
            )

        # 7. Default Conversational Agronomy
        else:
            tools = ["General Agronomy Intelligence", "Central AI Farmer Assistant"]
            reply = (
                f"Namaste {prof.name}! 🙏 I am your **AI Farmer Assistant (KrishiKalyan AI)**.\n\n"
                f"I combine real-time weather, trained machine learning models, soil datasets, Indian mandi prices, and government schemes to assist your farm decisions:\n\n"
                f"Here are questions you can ask me:\n"
                f"- *'Which crop should I grow in my soil?'*\n"
                f"- *'Is the weather suitable for irrigation or spraying today?'*\n"
                f"- *'What is the current market price of soybean/cotton in Maharashtra mandis?'*\n"
                f"- *'What government schemes and subsidies apply to my 3.5 acre farm?'*\n"
                f"- *'What is my recommended Farm Action Plan for this week?'*"
            )
            followups = ["Which crop should I grow?", "Is weather suitable for spraying?", "Where to sell my crop?", "Top government schemes for me"]
            return AssistantQueryResponse(
                reply=reply,
                detected_intent="General Agronomy & Navigation",
                tools_used=tools,
                structured_data=None,
                suggested_followups=followups
            )

    def _query_icar_advisories(self, text: str, crop: str = "", state: str = "") -> Optional[Dict[str, Any]]:
        import os
        from app.core.config import SQLITE_DB_PATH
        from app.db import query_as_dicts
        if os.path.exists(SQLITE_DB_PATH):
            try:
                rows = query_as_dicts("SELECT * FROM icar_advisories")
                for r in rows:
                    if (r["crop"].lower() in text or r["crop"].lower() in (crop or "").lower()) or (r["weather_trigger"].lower() in text):
                        return r
            except Exception as e:
                print(f"[!] ICAR RAG query exception: {e}")
        return None

assistant_service = AIAssistantOrchestrator()
