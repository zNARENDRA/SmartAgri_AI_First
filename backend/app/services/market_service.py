import os
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from app.core.config import SQLITE_DB_PATH, DATA_PROCESSED
from app.db import query_as_dataframe, query_as_dicts
from app.schemas import (
    MarketFilterOptions, MarketTrendResponse, PriceTrendPoint,
    WhereToSellResponse, MandiRankItem
)

class MarketIntelligenceService:
    def __init__(self):
        self.csv_path = os.path.join(DATA_PROCESSED, "mandi_prices_cleaned.csv")
        self.analytics_path = os.path.join(DATA_PROCESSED, "mandi_analytics.json")
        
        if os.path.exists(SQLITE_DB_PATH):
            try:
                self.df = query_as_dataframe(
                    "SELECT state as State, district as District, market as Market, commodity as Commodity, variety as Variety, arrival_date as Arrival_Date, min_price as Min_Price, max_price as Max_Price, modal_price as Modal_Price FROM mandi_prices"
                )
                if not self.df.empty:
                    self.df["Arrival_Date"] = pd.to_datetime(self.df["Arrival_Date"])
                
                rows = query_as_dicts("SELECT data_json FROM mandi_analytics WHERE key = ?", ("main_analytics",))
                if rows:
                    self.analytics = json.loads(rows[0]["data_json"])
                else:
                    self.analytics = {}
            except Exception as e:
                print(f"[!] Exception loading from SQLite DB in MarketIntelligenceService: {e}")
                self.df = pd.DataFrame()
                self.analytics = {}
        elif os.path.exists(self.csv_path):
            self.df = pd.read_csv(self.csv_path)
            self.df["Arrival_Date"] = pd.to_datetime(self.df["Arrival_Date"])
            if os.path.exists(self.analytics_path):
                with open(self.analytics_path, "r", encoding="utf-8") as f:
                    self.analytics = json.load(f)
            else:
                self.analytics = {}
        else:
            self.df = pd.DataFrame()
            self.analytics = {}

    def get_filter_options(self) -> MarketFilterOptions:
        if self.df.empty:
            return MarketFilterOptions(states=[], districts_by_state={}, mandis_by_district={}, commodities=[])
            
        states = sorted(list(self.df["State"].unique()))
        commodities = sorted(list(self.df["Commodity"].unique()))
        
        districts_by_state = {}
        mandis_by_district = {}
        
        for state in states:
            state_df = self.df[self.df["State"] == state]
            dists = sorted(list(state_df["District"].unique()))
            districts_by_state[state] = dists
            
            for dist in dists:
                dist_df = state_df[state_df["District"] == dist]
                mandis = sorted(list(dist_df["Market"].unique()))
                mandis_by_district[f"{state}__{dist}"] = mandis
                
        return MarketFilterOptions(
            states=states,
            districts_by_state=districts_by_state,
            mandis_by_district=mandis_by_district,
            commodities=commodities
        )

    def get_market_trends(
        self,
        commodity: str = "Soybean",
        state: str = "Maharashtra",
        district: Optional[str] = None,
        mandi: Optional[str] = None
    ) -> MarketTrendResponse:
        filtered = self.df[(self.df["Commodity"].str.lower() == commodity.lower()) & (self.df["State"].str.lower() == state.lower())]
        
        if filtered.empty:
            # Fallback to commodity across all states
            filtered = self.df[self.df["Commodity"].str.lower() == commodity.lower()]
            
        if district and district != "All":
            d_filtered = filtered[filtered["District"].str.lower() == district.lower()]
            if not d_filtered.empty:
                filtered = d_filtered
                
        if mandi and mandi != "All":
            m_filtered = filtered[filtered["Market"].str.lower() == mandi.lower()]
            if not m_filtered.empty:
                filtered = m_filtered

        # Aggregate daily average prices
        daily_agg = filtered.groupby("Arrival_Date").agg({
            "Min_Price": "mean",
            "Max_Price": "mean",
            "Modal_Price": "mean"
        }).reset_index().sort_values("Arrival_Date")

        price_history = []
        for _, row in daily_agg.iterrows():
            price_history.append(PriceTrendPoint(
                date=row["Arrival_Date"].strftime("%Y-%m-%d"),
                min_price=int(row["Min_Price"]),
                max_price=int(row["Max_Price"]),
                modal_price=int(row["Modal_Price"])
            ))

        if not daily_agg.empty:
            latest_modal = int(daily_agg["Modal_Price"].iloc[-1])
            min_p = int(daily_agg["Min_Price"].min())
            max_p = int(daily_agg["Max_Price"].max())
            avg_p = round(float(daily_agg["Modal_Price"].mean()), 2)
            
            # Trend calculation (last 14 points vs prior)
            if len(daily_agg) >= 10:
                recent_avg = daily_agg["Modal_Price"].iloc[-5:].mean()
                prior_avg = daily_agg["Modal_Price"].iloc[-15:-5].mean()
                pct_change = round(float(((recent_avg - prior_avg) / prior_avg) * 100), 2)
            else:
                pct_change = 0.0

            if pct_change > 1.5:
                trend_dir = "Rising (Bullish)"
            elif pct_change < -1.5:
                trend_dir = "Falling (Bearish)"
            else:
                trend_dir = "Stable (Range-bound)"

            std_dev = float(daily_agg["Modal_Price"].std())
            volatility = "High" if std_dev > (avg_p * 0.08) else "Moderate" if std_dev > (avg_p * 0.04) else "Low"
        else:
            latest_modal, min_p, max_p, avg_p, pct_change = 4500, 4200, 4800, 4500.0, 0.0
            trend_dir = "Stable"
            volatility = "Low"

        return MarketTrendResponse(
            commodity=commodity,
            state=state,
            district=district,
            mandi=mandi,
            latest_modal_price=latest_modal,
            min_price=min_p,
            max_price=max_p,
            average_price=avg_p,
            price_change_percentage=pct_change,
            trend_direction=trend_dir,
            volatility_rating=volatility,
            price_history=price_history,
            data_attribution="Historical Mandi Wholesale Price Dataset (Agmarknet / Kaggle Reference Series). All price figures in INR (₹) per Quintal (100 kg)."
        )

    def where_to_sell(self, commodity: str = "Soybean", state: str = "Maharashtra") -> WhereToSellResponse:
        filtered = self.df[(self.df["Commodity"].str.lower() == commodity.lower()) & (self.df["State"].str.lower() == state.lower())]
        if filtered.empty:
            filtered = self.df[self.df["Commodity"].str.lower() == commodity.lower()]

        mandi_stats = filtered.groupby(["Market", "District"]).agg({
            "Modal_Price": ["mean", "last", "std"],
            "Max_Price": "max"
        }).reset_index()

        mandi_stats.columns = ["Market", "District", "avg_modal", "latest_price", "vol_std", "max_price"]
        mandi_stats["vol_std"] = mandi_stats["vol_std"].fillna(0.0)
        mandi_stats = mandi_stats.sort_values(by="avg_modal", ascending=False)

        best_mandis = []
        for rank_idx, (_, row) in enumerate(mandi_stats.iterrows(), 1):
            if rank_idx == 1:
                badge = "🏆 Top Historical Realization"
            elif rank_idx == 2:
                badge = "🥈 High Demand Hub"
            elif row["vol_std"] < 100:
                badge = "🛡️ Stable Price Realization"
            else:
                badge = "📈 High Volume Market"

            best_mandis.append(MandiRankItem(
                rank=rank_idx,
                market=row["Market"],
                district=row["District"],
                state=state,
                avg_modal_price=round(float(row["avg_modal"]), 2),
                latest_price=int(row["latest_price"]),
                max_price_recorded=int(row["max_price"]),
                volatility_std=round(float(row["vol_std"]), 2),
                recommendation_badge=badge
            ))

        if best_mandis:
            top_m = best_mandis[0]
            spread_val = round(top_m.avg_modal_price - best_mandis[-1].avg_modal_price, 2)
            spread_text = f"Price spread across mandis is ₹{spread_val} per Quintal. Selling in {top_m.market} ({top_m.district}) yields up to {round((spread_val / best_mandis[-1].avg_modal_price)*100, 1)}% higher revenue."
            advice = f"Target {top_m.market} for premium batches. Group transport with fellow village farmers to offset freight costs and maximize net farm gate margins."
        else:
            spread_text = "Insufficient market data to compute inter-mandi spread."
            advice = "Verify modal prices with local APMC trader registers before transport."

        return WhereToSellResponse(
            commodity=commodity,
            state=state,
            best_mandis=best_mandis[:8],
            price_spread_analysis=spread_text,
            market_advice=advice,
            data_attribution="Based on Agmarknet / Kaggle India Mandi Wholesale Historical Price Dataset. Verify current day arrivals & bids on e-NAM / local APMC gate."
        )

market_service = MarketIntelligenceService()
