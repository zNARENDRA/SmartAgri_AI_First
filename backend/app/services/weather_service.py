import httpx
import datetime
from typing import Dict, Any, List
from app.schemas import WeatherAdvisoryResponse, WeatherCurrent, DailyForecastItem, AgroAdvisory

CITY_COORDINATES = {
    "nashik": (19.9975, 73.7898, "Nashik, Maharashtra"),
    "pune": (18.5204, 73.8567, "Pune, Maharashtra"),
    "nagpur": (21.1458, 79.0882, "Nagpur, Maharashtra"),
    "mumbai": (19.0760, 72.8777, "Mumbai, Maharashtra"),
    "ludhiana": (30.9010, 75.8573, "Ludhiana, Punjab"),
    "amritsar": (31.6340, 74.8723, "Amritsar, Punjab"),
    "patiala": (30.3398, 76.3869, "Patiala, Punjab"),
    "lucknow": (26.8467, 80.9462, "Lucknow, Uttar Pradesh"),
    "varanasi": (25.3176, 82.9739, "Varanasi, Uttar Pradesh"),
    "agra": (27.1767, 78.0081, "Agra, Uttar Pradesh"),
    "indore": (22.7196, 75.8577, "Indore, Madhya Pradesh"),
    "bhopal": (23.2599, 77.4126, "Bhopal, Madhya Pradesh"),
    "ahmedabad": (23.0225, 72.5714, "Ahmedabad, Gujarat"),
    "rajkot": (22.3039, 70.8022, "Rajkot, Gujarat"),
    "bengaluru": (12.9716, 77.5946, "Bengaluru, Karnataka"),
    "mysuru": (12.2958, 76.6394, "Mysuru, Karnataka"),
    "chennai": (13.0827, 80.2707, "Chennai, Tamil Nadu"),
    "coimbatore": (11.0168, 76.9558, "Coimbatore, Tamil Nadu"),
    "jaipur": (26.9124, 75.7873, "Jaipur, Rajasthan"),
    "patna": (25.5941, 85.1376, "Patna, Bihar"),
    "hyderabad": (17.3850, 78.4867, "Hyderabad, Telangana")
}

WMO_WEATHER_CODES = {
    0: "Clear Sky ☀️",
    1: "Mainly Clear 🌤️",
    2: "Partly Cloudy ⛅",
    3: "Overcast ☁️",
    45: "Foggy 🌫️",
    48: "Depositing Rime Fog 🌫️",
    51: "Light Drizzle 🌦️",
    53: "Moderate Drizzle 🌦️",
    55: "Dense Drizzle 🌧️",
    61: "Slight Rain 🌧️",
    63: "Moderate Rain 🌧️",
    65: "Heavy Rain ⛈️",
    71: "Slight Snow 🌨️",
    73: "Moderate Snow 🌨️",
    80: "Slight Rain Showers 🌦️",
    81: "Moderate Rain Showers 🌧️",
    82: "Violent Rain Showers ⛈️",
    95: "Thunderstorm ⛈️",
    96: "Thunderstorm with Slight Hail ⛈️"
}

class WeatherService:
    def __init__(self):
        self.client = httpx.Client(timeout=8.0)

    def _reverse_geocode(self, lat: float, lon: float) -> str:
        """Reverse geocode lat/lon to a human-readable place name using Nominatim (OpenStreetMap)."""
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=10&addressdetails=1&accept-language=en"
            resp = self.client.get(url, headers={"User-Agent": "SmartAgriAI/1.0"})
            if resp.status_code == 200:
                data = resp.json()
                addr = data.get("address", {})
                # Try city/town/village, then district, then county
                place = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("suburb") or addr.get("county") or addr.get("state_district") or ""
                state = addr.get("state", "")
                if place and state:
                    return f"{place}, {state}"
                elif place:
                    return place
                elif state:
                    return state
                # Fallback to display_name
                display = data.get("display_name", "")
                if display:
                    parts = [p.strip() for p in display.split(",")]
                    # Return first 2 meaningful parts
                    return ", ".join(parts[:2]) if len(parts) >= 2 else parts[0]
        except Exception as e:
            print(f"[Reverse Geocoding Notice] Fallback for ({lat}, {lon}): {e}")
        return ""

    def resolve_location(self, location_query: str = "", lat: float = None, lon: float = None):
        """Resolves location query or lat/lon coordinates to exact latitude, longitude, and display name."""
        if lat is not None and lon is not None:
            # Reverse geocode to get a real place name instead of raw coordinates
            display_name = self._reverse_geocode(float(lat), float(lon))
            if not display_name:
                display_name = f"GPS Location ({float(lat):.2f}°, {float(lon):.2f}°)"
            return float(lat), float(lon), display_name

        if not location_query or location_query.strip() == "":
            return 19.9975, 73.7898, "Nashik, Maharashtra"

        loc_key = location_query.strip().lower().split(",")[0].strip()
        if loc_key in CITY_COORDINATES:
            c_lat, c_lon, display = CITY_COORDINATES[loc_key]
            return c_lat, c_lon, display

        # Query Open-Meteo Geocoding API dynamically for any city/district in India/world
        try:
            g_resp = self.client.get(f"https://geocoding-api.open-meteo.com/v1/search?name={location_query}&count=1&language=en&format=json")
            if g_resp.status_code == 200:
                g_data = g_resp.json()
                results = g_data.get("results", [])
                if results:
                    r = results[0]
                    g_lat = float(r["latitude"])
                    g_lon = float(r["longitude"])
                    name = r.get("name", location_query)
                    state = r.get("admin1", "")
                    country = r.get("country", "")
                    disp = f"{name}, {state}" if state else f"{name}, {country}"
                    return g_lat, g_lon, disp
        except Exception as e:
            print(f"[Geocoding Notice] Fallback for '{location_query}': {e}")

        return 19.9975, 73.7898, f"{location_query.title()}, India"

    def get_weather_and_advisory(self, location_query: str = "Nashik", crop_context: str = "General", lat: float = None, lon: float = None) -> WeatherAdvisoryResponse:
        c_lat, c_lon, display_name = self.resolve_location(location_query, lat, lon)
        
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={c_lat}&longitude={c_lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max&timezone=auto"
            resp = self.client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                return self._parse_api_response(data, display_name, crop_context)
        except Exception as e:
            print(f"[Weather API Notice] Using fallback agro-meteorological simulation: {e}")
            
        return self._generate_fallback_response(display_name, crop_context)

    def get_realtime_temperature_and_weather(self, location_query: str = "", lat: float = None, lon: float = None) -> Dict[str, Any]:
        c_lat, c_lon, display_name = self.resolve_location(location_query, lat, lon)
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={c_lat}&longitude={c_lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&timezone=auto"
            resp = self.client.get(url)
            if resp.status_code == 200:
                curr = resp.json().get("current", {})
                code = int(curr.get("weather_code", 0))
                return {
                    "status": "success",
                    "is_realtime": True,
                    "location_name": display_name,
                    "latitude": c_lat,
                    "longitude": c_lon,
                    "temperature_celsius": float(curr.get("temperature_2m", 28.5)),
                    "humidity_percentage": float(curr.get("relative_humidity_2m", 65.0)),
                    "wind_speed_kmh": float(curr.get("wind_speed_10m", 11.2)),
                    "precipitation_mm": float(curr.get("precipitation", 0.0)),
                    "condition_text": WMO_WEATHER_CODES.get(code, "Partly Cloudy ⛅"),
                    "weather_code": code,
                    "provider": "Open-Meteo Global Realtime Meteorological API",
                    "timestamp": datetime.datetime.now().isoformat()
                }
        except Exception as e:
            print(f"[Realtime Weather API Exception]: {e}")

        return {
            "status": "fallback",
            "is_realtime": False,
            "location_name": display_name,
            "latitude": c_lat,
            "longitude": c_lon,
            "temperature_celsius": 28.5,
            "humidity_percentage": 65.0,
            "wind_speed_kmh": 10.0,
            "precipitation_mm": 0.0,
            "condition_text": "Mainly Clear 🌤️",
            "weather_code": 1,
            "provider": "Agro-Meteorological Service (Offline Fallback)",
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _parse_api_response(self, data: Dict[str, Any], location_name: str, crop: str) -> WeatherAdvisoryResponse:
        curr = data.get("current", {})
        temp = float(curr.get("temperature_2m", 28.5))
        humidity = float(curr.get("relative_humidity_2m", 65.0))
        wind = float(curr.get("wind_speed_10m", 11.2))
        precip = float(curr.get("precipitation", 0.0))
        code = int(curr.get("weather_code", 0))
        cond_text = WMO_WEATHER_CODES.get(code, "Partly Cloudy ⛅")

        current_obj = WeatherCurrent(
            temperature=temp,
            humidity=humidity,
            wind_speed_kmh=wind,
            precipitation_mm=precip,
            condition_text=cond_text,
            weather_code=code,
            location_name=location_name
        )

        daily = data.get("daily", {})
        dates = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        rains = daily.get("precipitation_sum", [])
        rain_probs = daily.get("precipitation_probability_max", [])
        codes = daily.get("weather_code", [])

        forecast_list = []
        for i in range(min(7, len(dates))):
            d_str = dates[i]
            dt = datetime.date.fromisoformat(d_str)
            w_code = int(codes[i]) if i < len(codes) else 1
            forecast_list.append(DailyForecastItem(
                date=d_str,
                day_name=dt.strftime("%A") if i > 0 else "Today",
                temp_max=float(max_temps[i]) if i < len(max_temps) else temp + 3,
                temp_min=float(min_temps[i]) if i < len(min_temps) else temp - 5,
                rain_sum_mm=float(rains[i]) if i < len(rains) else 0.0,
                precipitation_probability_max=int(rain_probs[i]) if i < len(rain_probs) else 10,
                condition_text=WMO_WEATHER_CODES.get(w_code, "Partly Cloudy"),
                weather_code=w_code
            ))

        advisory_obj = self._compute_agro_advisory(current_obj, forecast_list, crop)
        imd_baseline = self._fetch_imd_rainfall_baseline(location_name)
        return WeatherAdvisoryResponse(
            current=current_obj,
            forecast=forecast_list,
            advisory=advisory_obj,
            imd_rainfall_baseline=imd_baseline,
            provider="Open-Meteo Global Meteorological Service"
        )

    def _generate_fallback_response(self, location_name: str, crop: str) -> WeatherAdvisoryResponse:
        today = datetime.date.today()
        current_obj = WeatherCurrent(
            temperature=29.2,
            humidity=62.0,
            wind_speed_kmh=9.5,
            precipitation_mm=0.0,
            condition_text="Mainly Clear 🌤️",
            weather_code=1,
            location_name=location_name
        )
        
        forecast_list = []
        for i in range(7):
            d = today + datetime.timedelta(days=i)
            forecast_list.append(DailyForecastItem(
                date=d.isoformat(),
                day_name=d.strftime("%A") if i > 0 else "Today",
                temp_max=round(31.0 + (i % 3) * 0.8, 1),
                temp_min=round(19.5 + (i % 2) * 0.6, 1),
                rain_sum_mm=0.0 if i != 3 else 4.2,
                precipitation_probability_max=15 if i != 3 else 60,
                condition_text="Partly Cloudy ⛅" if i != 3 else "Light Rain 🌦️",
                weather_code=2 if i != 3 else 61
            ))
            
        advisory_obj = self._compute_agro_advisory(current_obj, forecast_list, crop)
        imd_baseline = self._fetch_imd_rainfall_baseline(location_name)
        return WeatherAdvisoryResponse(
            current=current_obj,
            forecast=forecast_list,
            advisory=advisory_obj,
            imd_rainfall_baseline=imd_baseline,
            provider="Agro-Meteorological Service (Offline Baseline)"
        )

    def _fetch_imd_rainfall_baseline(self, location_name: str) -> Dict[str, Any]:
        import os
        from app.core.config import SQLITE_DB_PATH
        from app.db import query_as_dicts
        
        state = "Maharashtra"
        for st in ["Maharashtra", "Punjab", "Karnataka", "Gujarat", "Uttar Pradesh", "Madhya Pradesh"]:
            if st.lower() in location_name.lower():
                state = st
                break
                
        if os.path.exists(SQLITE_DB_PATH):
            try:
                curr_month = datetime.date.today().strftime("%b")
                rows = query_as_dicts(
                    "SELECT * FROM imd_rainfall WHERE state = ? ORDER BY id LIMIT 1",
                    (state,)
                )
                if rows:
                    r = rows[0]
                    dep = float(r.get("departure_pct", 0.0))
                    status_text = "Above Normal Rainfall (+)" if dep > 10.0 else ("Below Normal Rainfall (-)" if dep < -10.0 else "Normal Monsoon Baseline")
                    return {
                        "state": state,
                        "subdivision": r.get("subdivision", state),
                        "month": r.get("month", curr_month),
                        "season": r.get("season", "Monsoon"),
                        "normal_rainfall_mm": float(r.get("normal_mm", 220.0)),
                        "actual_rainfall_mm": float(r.get("actual_mm", 240.0)),
                        "departure_pct": dep,
                        "departure_percentage": f"{dep:+.1f}%",
                        "monsoon_status": status_text
                    }
            except Exception as e:
                print(f"[!] Warning querying IMD rainfall baseline: {e}")
                
        return {
            "state": state,
            "subdivision": f"{state} Division",
            "month": "Aug",
            "season": "Monsoon",
            "normal_rainfall_mm": 210.0,
            "actual_rainfall_mm": 235.0,
            "departure_pct": 11.9,
            "departure_percentage": "+11.9%",
            "monsoon_status": "Normal Monsoon Baseline"
        }

    def _compute_agro_advisory(self, current: WeatherCurrent, forecast: List[DailyForecastItem], crop: str) -> AgroAdvisory:
        # 1. Total rain expected next 48h
        next_48h_rain = sum([f.rain_sum_mm for f in forecast[:2]])
        
        if next_48h_rain > 15.0:
            irrigation = {
                "status": "SKIP / DELAY",
                "badge_color": "yellow",
                "summary": f"Heavy rainfall ({next_48h_rain:.1f} mm) predicted in the next 48 hours.",
                "action": "Do NOT apply irrigation. Ensure drainage channels are open to prevent standing water."
            }
        elif next_48h_rain > 5.0:
            irrigation = {
                "status": "REDUCE DURATION",
                "badge_color": "blue",
                "summary": f"Moderate showers ({next_48h_rain:.1f} mm) expected.",
                "action": "Reduce drip or furrow irrigation by 50% to save water and energy."
            }
        else:
            irrigation = {
                "status": "OPTIMAL TO IRRIGATE",
                "badge_color": "green",
                "summary": "Dry weather ahead with low rain probability.",
                "action": "Proceed with regular irrigation schedule. Best timings: Early morning (6-9 AM) or evening (5-7 PM)."
            }

        # 2. Spraying window
        if current.wind_speed_kmh < 14.0 and current.precipitation_mm == 0 and (len(forecast) == 0 or forecast[0].precipitation_probability_max < 25):
            spraying = {
                "status": "EXCELLENT WINDOW",
                "badge_color": "green",
                "summary": f"Low wind speed ({current.wind_speed_kmh:.1f} km/h) and no rain expected today.",
                "action": "Safe for pesticide and foliar fertilizer spraying. Morning 7-10 AM provides highest absorption."
            }
        elif current.wind_speed_kmh >= 14.0:
            spraying = {
                "status": "AVOID SPRAYING",
                "badge_color": "red",
                "summary": f"High wind drift risk ({current.wind_speed_kmh:.1f} km/h).",
                "action": "Do not spray chemicals today. High wind causes chemical drift and wasteful spray loss."
            }
        else:
            spraying = {
                "status": "MODERATE RISK",
                "badge_color": "yellow",
                "summary": "Rain probability elevated in coming hours.",
                "action": "Avoid systemic chemicals without rain-fast sticker surfactant."
            }

        # 3. Heat / Cold stress
        if current.temperature > 37.0:
            stress = {
                "status": "HIGH HEAT STRESS",
                "badge_color": "red",
                "summary": f"High ambient temperature ({current.temperature:.1f}°C).",
                "action": "Provide light evening irrigation to reduce soil temperature. Spray anti-transpirants if available."
            }
        elif current.temperature < 10.0:
            stress = {
                "status": "COLD / FROST RISK",
                "badge_color": "blue",
                "summary": f"Low night temperatures ({current.temperature:.1f}°C).",
                "action": "Irrigate fields lightly in evening to raise root-zone heat capacity and prevent frost injury."
            }
        else:
            stress = {
                "status": "FAVORABLE",
                "badge_color": "green",
                "summary": f"Temperature ({current.temperature:.1f}°C) is in the optimal physiological range.",
                "action": "Ideal growing conditions for photosynthesis and vegetative development."
            }

        # 4. Disease / Pest risk
        if current.humidity > 80.0 and (20.0 <= current.temperature <= 30.0):
            disease_risk = {
                "status": "ELEVATED FUNGAL RISK",
                "badge_color": "red",
                "summary": f"High humidity ({current.humidity:.1f}%) and warm weather favor fungal spore germination.",
                "action": "Inspect crop underside for powdery mildew, downy mildew, or blight spots. Keep preventive Trichoderma ready."
            }
        elif current.humidity < 40.0 and current.temperature > 32.0:
            disease_risk = {
                "status": "SUCKING PEST / MITE RISK",
                "badge_color": "yellow",
                "summary": "Dry and warm climate accelerates Spider Mite and Thrips reproduction.",
                "action": "Scout new shoots and leaf undersides for fine webbing or leaf curling."
            }
        else:
            disease_risk = {
                "status": "LOW-MODERATE RISK",
                "badge_color": "green",
                "summary": "Environmental parameters do not trigger active disease outbreak thresholds.",
                "action": "Maintain routine crop monitoring once every 3 days."
            }

        # 5. Harvest timing
        rainy_days = [f for f in forecast[:4] if f.rain_sum_mm > 1.0]
        if len(rainy_days) == 0:
            harvest = {
                "status": "IDEAL HARVEST WINDOW",
                "badge_color": "green",
                "summary": "Clear dry spell for the next 4 consecutive days.",
                "action": "Safe to harvest mature crops and dry harvested grain on threshing floors."
            }
        else:
            harvest = {
                "status": "POSTPONE HARVEST",
                "badge_color": "yellow",
                "summary": f"Rain showers predicted on {rainy_days[0].day_name}.",
                "action": "Store already harvested produce in moisture-proof covered warehouses or tarp sheets."
            }

        alert_msg = f"Weather in {current.location_name}: {current.condition_text}, {current.temperature:.1f}°C. {irrigation['action']}"

        return AgroAdvisory(
            irrigation_advice=irrigation,
            spraying_window=spraying,
            heat_cold_stress=stress,
            pest_disease_risk=disease_risk,
            harvest_recommendation=harvest,
            overall_farm_alert=alert_msg
        )

weather_service = WeatherService()
