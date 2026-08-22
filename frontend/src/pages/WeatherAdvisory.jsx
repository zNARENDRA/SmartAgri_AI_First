import React, { useState, useEffect } from "react";
import { useFarmer } from "../context/FarmerContext";
import { getWeatherAdvisory } from "../services/api";
import {
  CloudSun,
  MapPin,
  Search,
  Droplets,
  Wind,
  Thermometer,
  ShieldAlert,
  Calendar,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  RefreshCw,
  Sun,
  CloudRain
} from "lucide-react";
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend
} from "recharts";

export default function WeatherAdvisory() {
  const { profile } = useFarmer();
  // Build location from farmer profile: "District, State" or fallback
  const profileLocation = [profile.district, profile.state].filter(Boolean).join(", ") || "Nashik, Maharashtra";
  const [locationInput, setLocationInput] = useState(profileLocation);
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchWeather = async (loc, lat = null, lon = null) => {
    setLoading(true);
    try {
      const data = await getWeatherAdvisory(loc, profile.current_crop, lat, lon);
      setWeatherData(data);
      if (data && data.current && data.current.location_name) {
        setLocationInput(data.current.location_name);
      }
    } catch (err) {
      console.error("Weather fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchGpsLocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }
    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        fetchWeather("", pos.coords.latitude, pos.coords.longitude);
      },
      () => {
        setLoading(false);
        alert("GPS Location access denied or unavailable. Search any city name in the input box!");
      }
    );
  };

  useEffect(() => {
    // Load weather for farmer's profile location on page open
    fetchWeather(profileLocation);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (locationInput.trim()) {
      fetchWeather(locationInput.trim());
    }
  };

  const chartData = weatherData && weatherData.forecast ? weatherData.forecast.map((f) => ({
    day: f.day_name.slice(0, 3),
    maxTemp: f.temp_max,
    minTemp: f.temp_min,
    rain: f.rain_sum_mm,
    rainProb: f.precipitation_probability_max
  })) : [];

  return (
    <div className="page-wrapper">
      {/* Header & Location Search */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "20px", flexWrap: "wrap", gap: "12px" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
            <span className="badge badge-green">🟢 LIVE Real-time Weather Feed</span>
            <span style={{ fontSize: "12px", color: "#64748b", fontWeight: 600 }}>Open-Meteo Meteorological API</span>
          </div>
          <h1 style={{ fontSize: "24px", fontWeight: 800, color: "#0f172a", letterSpacing: "-0.02em", margin: 0 }}>
            Real-Time Weather & Agro-Advisory
          </h1>
          <p style={{ fontSize: "13px", color: "#64748b", marginTop: "2px" }}>
            Translating live real-time temperature, humidity, and forecasts into precision farming decisions.
          </p>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "6px", width: "100%", maxWidth: "420px" }}>
          <form onSubmit={handleSearch} style={{ display: "flex", gap: "8px", width: "100%" }}>
            <div style={{ position: "relative", flex: 1 }}>
              <MapPin size={16} color="#64748b" style={{ position: "absolute", left: "12px", top: "12px" }} />
              <input
                type="text"
                value={locationInput}
                onChange={(e) => setLocationInput(e.target.value)}
                placeholder="Search City/District (e.g. Pune, Ludhiana, Sangli)"
                className="form-input"
                style={{ paddingLeft: "36px", margin: 0 }}
              />
            </div>
            <button type="submit" disabled={loading} className="btn btn-primary" style={{ flexShrink: 0 }}>
              <Search size={16} />
            </button>
          </form>
          
          <button
            type="button"
            onClick={fetchGpsLocation}
            disabled={loading}
            className="btn btn-secondary"
            style={{ fontSize: "11px", padding: "6px 12px", display: "flex", alignItems: "center", justifyContent: "center", gap: "6px" }}
          >
            <MapPin size={13} color="#059669" /> Use Live GPS Location
          </button>
        </div>
      </div>

      {loading && (
        <div className="card" style={{ textAlign: "center", padding: "40px" }}>
          <div style={{ display: "inline-block", animation: "spin 1s infinite linear" }}>
            <RefreshCw size={28} color="#059669" />
          </div>
          <div style={{ marginTop: "10px", fontSize: "14px", color: "#64748b" }}>
            Fetching meteorological data and computing agro-advisories...
          </div>
        </div>
      )}

      {!loading && weatherData && (
        <>
          {/* Current Weather Banner */}
          <div style={{
            background: "linear-gradient(135deg, #0369a1 0%, #0284c7 60%, #38bdf8 100%)",
            color: "#ffffff",
            borderRadius: "16px",
            padding: "20px 24px",
            marginBottom: "16px",
            boxShadow: "0 10px 20px -5px rgba(2, 132, 199, 0.3)",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "16px"
          }}>
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "12px", color: "#e0f2fe", fontWeight: 600, marginBottom: "2px" }}>
                <MapPin size={14} /> {weatherData.current.location_name}
              </div>
              <h2 style={{ fontSize: "32px", fontWeight: 800, margin: 0 }}>
                {weatherData.current.temperature.toFixed(1)}°C
              </h2>
              <div style={{ fontSize: "14px", color: "#f0f9ff", fontWeight: 600, marginTop: "2px" }}>
                {weatherData.current.condition_text}
              </div>
            </div>

            <div style={{ display: "flex", gap: "16px", background: "rgba(255,255,255,0.15)", padding: "10px 18px", borderRadius: "12px", backdropFilter: "blur(8px)", flexWrap: "wrap" }}>
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: "4px", fontSize: "11px", color: "#e0f2fe" }}>
                  <Droplets size={12} /> Humidity
                </div>
                <div style={{ fontSize: "16px", fontWeight: 700 }}>
                  {weatherData.current.humidity.toFixed(0)}%
                </div>
              </div>

              <div>
                <div style={{ display: "flex", alignItems: "center", gap: "4px", fontSize: "11px", color: "#e0f2fe" }}>
                  <Wind size={12} /> Wind
                </div>
                <div style={{ fontSize: "16px", fontWeight: 700 }}>
                  {weatherData.current.wind_speed_kmh.toFixed(1)} km/h
                </div>
              </div>

              <div>
                <div style={{ display: "flex", alignItems: "center", gap: "4px", fontSize: "11px", color: "#e0f2fe" }}>
                  <CloudRain size={12} /> Rain
                </div>
                <div style={{ fontSize: "16px", fontWeight: 700 }}>
                  {weatherData.current.precipitation_mm.toFixed(1)} mm
                </div>
              </div>
            </div>
          </div>

          {/* GoI IMD Meteorological Rainfall Baseline Card (Dataset 9) */}
          {weatherData.imd_rainfall_baseline && (
            <div className="card" style={{ background: "#f0f9ff", border: "1px solid #bae6fd", marginBottom: "20px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px", flexWrap: "wrap", gap: "8px" }}>
                <div style={{ fontSize: "13px", fontWeight: 800, color: "#0369a1", display: "flex", alignItems: "center", gap: "6px" }}>
                  <CloudRain size={16} /> GoI IMD Meteorological Rainfall Baseline ({weatherData.imd_rainfall_baseline.subdivision})
                </div>
                <span className="badge badge-blue" style={{ fontSize: "11px" }}>
                  {weatherData.imd_rainfall_baseline.monsoon_status}
                </span>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))", gap: "10px", fontSize: "12px", background: "#ffffff", padding: "10px 14px", borderRadius: "8px", border: "1px solid #e0f2fe" }}>
                <div><span style={{ color: "#64748b" }}>Normal Baseline:</span> <strong style={{ color: "#0f172a" }}>{weatherData.imd_rainfall_baseline.normal_rainfall_mm} mm</strong></div>
                <div><span style={{ color: "#64748b" }}>Actual Recorded:</span> <strong style={{ color: "#0284c7" }}>{weatherData.imd_rainfall_baseline.actual_rainfall_mm} mm</strong></div>
                <div><span style={{ color: "#64748b" }}>Monsoon Departure:</span> <strong style={{ color: weatherData.imd_rainfall_baseline.departure_pct >= 0 ? "#059669" : "#d97706" }}>{weatherData.imd_rainfall_baseline.departure_percentage}</strong></div>
              </div>
            </div>
          )}

          {/* 5 Agro-Advisory Action Cards Grid */}
          <h2 style={{ fontSize: "16px", fontWeight: 800, color: "#0f172a", marginBottom: "14px" }}>
            Actionable Agricultural Recommendations
          </h2>

          <div className="grid-3" style={{ marginBottom: "20px" }}>
            {/* 1. Irrigation Advisory */}
            <div className="card" style={{ borderLeft: "4px solid #0284c7" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                <span style={{ fontSize: "13px", fontWeight: 800, color: "#0369a1" }}>💧 Irrigation Timing</span>
                <span className="badge badge-blue">{weatherData.advisory.irrigation_advice.status}</span>
              </div>
              <p style={{ fontSize: "12px", color: "#1e293b", margin: "0 0 6px 0", lineHeight: 1.4 }}>
                {weatherData.advisory.irrigation_advice.summary}
              </p>
              <div style={{ fontSize: "12px", color: "#0284c7", fontWeight: 600 }}>
                {weatherData.advisory.irrigation_advice.action}
              </div>
            </div>

            {/* 2. Spraying Safety Window */}
            <div className="card" style={{ borderLeft: "4px solid #059669" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                <span style={{ fontSize: "13px", fontWeight: 800, color: "#065f46" }}>🎯 Spraying Window</span>
                <span className="badge badge-green">{weatherData.advisory.spraying_window.status}</span>
              </div>
              <p style={{ fontSize: "12px", color: "#1e293b", margin: "0 0 6px 0", lineHeight: 1.4 }}>
                {weatherData.advisory.spraying_window.summary}
              </p>
              <div style={{ fontSize: "12px", color: "#047857", fontWeight: 600 }}>
                {weatherData.advisory.spraying_window.action}
              </div>
            </div>

            {/* 3. Disease & Pest Risk */}
            <div className="card" style={{ borderLeft: "4px solid #e11d48" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                <span style={{ fontSize: "13px", fontWeight: 800, color: "#9f1239" }}>🦠 Pest / Fungal Risk</span>
                <span className="badge badge-red">{weatherData.advisory.pest_disease_risk.status}</span>
              </div>
              <p style={{ fontSize: "12px", color: "#1e293b", margin: "0 0 6px 0", lineHeight: 1.4 }}>
                {weatherData.advisory.pest_disease_risk.summary}
              </p>
              <div style={{ fontSize: "12px", color: "#be185d", fontWeight: 600 }}>
                {weatherData.advisory.pest_disease_risk.action}
              </div>
            </div>

            {/* 4. Heat / Cold Stress */}
            <div className="card" style={{ borderLeft: "4px solid #d97706" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                <span style={{ fontSize: "13px", fontWeight: 800, color: "#92400e" }}>🌡️ Heat & Frost Risk</span>
                <span className="badge badge-amber">{weatherData.advisory.heat_cold_stress.status}</span>
              </div>
              <p style={{ fontSize: "12px", color: "#1e293b", margin: "0 0 6px 0", lineHeight: 1.4 }}>
                {weatherData.advisory.heat_cold_stress.summary}
              </p>
              <div style={{ fontSize: "12px", color: "#b45309", fontWeight: 600 }}>
                {weatherData.advisory.heat_cold_stress.action}
              </div>
            </div>

            {/* 5. Harvest Timing */}
            <div className="card" style={{ borderLeft: "4px solid #7c3aed" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                <span style={{ fontSize: "13px", fontWeight: 800, color: "#6b21a8" }}>🚜 Harvest Timing</span>
                <span className="badge badge-purple">{weatherData.advisory.harvest_recommendation.status}</span>
              </div>
              <p style={{ fontSize: "12px", color: "#1e293b", margin: "0 0 6px 0", lineHeight: 1.4 }}>
                {weatherData.advisory.harvest_recommendation.summary}
              </p>
              <div style={{ fontSize: "12px", color: "#7c3aed", fontWeight: 600 }}>
                {weatherData.advisory.harvest_recommendation.action}
              </div>
            </div>

            {/* 6. Overall Farm Alert Banner */}
            <div className="card" style={{ background: "#f8fafc" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "6px", color: "#0f172a", fontWeight: 800, fontSize: "13px" }}>
                <CheckCircle2 size={15} color="#059669" /> Daily Summary
              </div>
              <p style={{ fontSize: "12px", color: "#475569", lineHeight: 1.4, margin: 0 }}>
                {weatherData.advisory.overall_farm_alert}
              </p>
            </div>
          </div>

          {/* 7-Day Forecast & Temperature/Rainfall Chart */}
          <div className="card" style={{ marginBottom: "20px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px", flexWrap: "wrap", gap: "8px" }}>
              <h3 style={{ fontSize: "15px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
                7-Day Weather Trend & Rainfall Outlook
              </h3>
              <span style={{ fontSize: "11px", color: "#64748b" }}>Daily High/Low Temp (°C) & Rain (mm)</span>
            </div>

            <div style={{ height: "200px", width: "100%", marginBottom: "16px" }}>
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={chartData} margin={{ top: 10, right: 10, bottom: 0, left: 0 }}>
                  <XAxis dataKey="day" tick={{ fontSize: 11 }} />
                  <YAxis yAxisId="left" orientation="left" domain={[10, 45]} unit="°C" tick={{ fontSize: 10 }} width={40} />
                  <YAxis yAxisId="right" orientation="right" domain={[0, 50]} unit="mm" tick={{ fontSize: 10 }} width={35} />
                  <Tooltip />
                  <Legend wrapperStyle={{ fontSize: "11px" }} />
                  <Bar yAxisId="right" dataKey="rain" name="Rain (mm)" fill="#38bdf8" radius={[4, 4, 0, 0]} />
                  <Line yAxisId="left" type="monotone" dataKey="maxTemp" name="Max Temp" stroke="#ef4444" strokeWidth={2.5} dot={{ r: 3 }} />
                  <Line yAxisId="left" type="monotone" dataKey="minTemp" name="Min Temp" stroke="#3b82f6" strokeWidth={2} dot={{ r: 2 }} />
                </ComposedChart>
              </ResponsiveContainer>
            </div>

            {/* 7-Day Forecast Cards (Horizontally Scrollable / Grid Responsive) */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(75px, 1fr))", gap: "8px", width: "100%" }}>
              {weatherData.forecast.map((f, i) => (
                <div key={i} style={{ background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: "8px", padding: "8px 4px", textAlign: "center" }}>
                  <div style={{ fontSize: "11px", fontWeight: 700, color: "#1e293b", marginBottom: "2px" }}>
                    {f.day_name.slice(0, 3)}
                  </div>
                  <div style={{ fontSize: "10px", color: "#64748b", marginBottom: "2px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                    {f.condition_text.split(" ")[0]}
                  </div>
                  <div style={{ fontSize: "12px", fontWeight: 800, color: "#0f172a" }}>
                    {f.temp_max.toFixed(0)}° / {f.temp_min.toFixed(0)}°
                  </div>
                  {f.rain_sum_mm > 0 && (
                    <div style={{ fontSize: "10px", color: "#0284c7", fontWeight: 600, marginTop: "2px" }}>
                      {f.rain_sum_mm.toFixed(1)} mm
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
