import os
import json
from typing import List, Dict, Any, Optional
from app.core.config import SQLITE_DB_PATH, DATA_PROCESSED
from app.db import query_as_dicts
from app.schemas import SchemeItem, SchemeSearchResponse, FarmerProfile

class GovernmentSchemeService:
    def __init__(self):
        self.schemes_path = os.path.join(DATA_PROCESSED, "government_schemes_cleaned.json")
        self.schemes_raw = []
        
        if os.path.exists(SQLITE_DB_PATH):
            try:
                db_rows = query_as_dicts("SELECT * FROM government_schemes")
                for row in db_rows:
                    scheme = {
                        "id": row.get("id"),
                        "scheme_name": row.get("scheme_name", ""),
                        "short_name": row.get("short_name", ""),
                        "category": row.get("category", ""),
                        "sponsoring_agency": row.get("sponsoring_agency", ""),
                        "level": row.get("level", "Central"),
                        "description": row.get("description", ""),
                        "benefits": row.get("benefits", ""),
                        "eligibility_criteria": json.loads(row.get("eligibility_criteria_json") or "{}"),
                        "target_beneficiaries": row.get("target_beneficiaries", ""),
                        "documents_required": json.loads(row.get("documents_required_json") or "[]"),
                        "application_process": row.get("application_process", ""),
                        "official_url": row.get("official_url", ""),
                        "myscheme_url": row.get("myscheme_url", ""),
                        "helpdesk_contact": row.get("helpdesk_contact", "")
                    }
                    self.schemes_raw.append(scheme)
            except Exception as e:
                print(f"[!] Exception loading schemes from SQLite DB: {e}")
                self.schemes_raw = []
        elif os.path.exists(self.schemes_path):
            with open(self.schemes_path, "r", encoding="utf-8") as f:
                self.schemes_raw = json.load(f)

    def get_all_schemes(self) -> List[SchemeItem]:
        return [SchemeItem(**s) for s in self.schemes_raw]

    def search_schemes(self, query: Optional[str] = None, category: Optional[str] = None) -> SchemeSearchResponse:
        results = []
        categories = sorted(list(set([s["category"] for s in self.schemes_raw])))
        
        q_tokens = query.lower().split() if query else []
        
        for s in self.schemes_raw:
            # Category filter
            if category and category != "All" and s["category"].lower() != category.lower():
                continue
                
            # Search query matching
            if q_tokens:
                blob = f"{s['scheme_name']} {s['short_name']} {s['category']} {s['description']} {s['benefits']} {s['target_beneficiaries']}".lower()
                matches = sum([1 for tok in q_tokens if tok in blob])
                if matches == 0:
                    continue
                score = round(matches / len(q_tokens), 2)
            else:
                score = 1.0

            item = SchemeItem(**s)
            item.match_score = score
            results.append(item)

        results.sort(key=lambda x: x.match_score or 0.0, reverse=True)

        return SchemeSearchResponse(
            total_schemes=len(results),
            results=results,
            categories=["All"] + categories,
            disclaimer=f"DEBUG len(self.schemes_raw): {len(self.schemes_raw)} category: {category} query: {query}"
        )

    def match_for_profile(self, profile: FarmerProfile) -> List[SchemeItem]:
        matched = []
        for s in self.schemes_raw:
            reasons = []
            score = 0.5 # Base applicability
            
            crit = s.get("eligibility_criteria", {})
            f_types = crit.get("farmer_type", [])
            max_land = crit.get("land_size_max_acres", 100)
            states = crit.get("states", [])
            crops = crit.get("crops", [])

            # 1. Land size
            if profile.land_size_acres <= max_land:
                score += 0.2
                if profile.land_size_acres <= 5.0:
                    reasons.append(f"Small landholding ({profile.land_size_acres} acres) qualifies for maximum subsidy tier.")

            # 2. Farmer category matching
            if "All Farmers" in f_types or any([profile.farmer_category.lower() in ft.lower() for ft in f_types]):
                score += 0.15
                reasons.append(f"Eligible for {profile.farmer_category} beneficiary category.")

            # 3. State applicability
            if "All States" in states or any([profile.state.lower() in st.lower() for st in states]):
                score += 0.15
                reasons.append(f"Active in {profile.state}.")

            # 4. Crop alignment
            if profile.current_crop and any([profile.current_crop.lower() in c.lower() for c in crops]):
                score += 0.1
                reasons.append(f"Applicable for {profile.current_crop} cultivation.")

            score = min(0.98, round(score, 2))
            
            item = SchemeItem(**s)
            item.match_score = score
            item.match_reasons = reasons if reasons else ["General central agricultural scheme applicability."]
            matched.append(item)

        matched.sort(key=lambda x: x.match_score or 0.0, reverse=True)
        return matched

scheme_service = GovernmentSchemeService()
