import React, { useState, useRef, useEffect } from "react";
import { useFarmer } from "../context/FarmerContext";
import { askAssistant } from "../services/api";
import {
  BotMessageSquare,
  Send,
  Sparkles,
  User,
  Wrench,
  HelpCircle,
  CornerDownLeft,
  RefreshCw,
  Camera,
  Bug,
  CheckCircle2,
  AlertTriangle
} from "lucide-react";

export default function AIAssistant() {
  const { 
    profile, 
    pendingAiContext, 
    setPendingAiContext, 
    setShowCameraScanner 
  } = useFarmer();

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: `Namaste ${profile.name}! 🙏 I am your **AI Farmer Assistant (SmartAgri AI)**.\n\nI combine real-time weather, agronomic intelligence, soil health data, mandi prices, and government schemes to assist your farm decisions.\n\nHow can I help your farm today?`,
      tools: ["Agricultural Intelligence Hub", "Farm Profile Context"],
      followups: [
        "Which crop should I grow in my soil?",
        "Is the weather suitable for spraying today?",
        "What is the current mandi price for my crop?",
        "What government schemes apply to me?",
        "What is my Farm Action Plan for this week?"
      ]
    }
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Handle cross-module pending context (e.g. from Plant Disease Scanner)
  useEffect(() => {
    if (pendingAiContext && pendingAiContext.type === "disease") {
      const d = pendingAiContext;
      const diseaseSummaryMsg = {
        role: "assistant",
        content: `🔍 **Diagnosis Context Received from Plant Disease Scanner**:\n\n• **Detected Crop:** ${d.crop}\n• **Identified Condition:** **${d.condition}** (${d.confidence} match)\n• **Severity:** ${d.severity} • **Pathogen:** ${d.status === "Healthy" ? "None (Plant is healthy)" : "Fungal / Bacterial lesion"}\n\n**Immediate Treatment Advice:**\n• **Organic Cure:** ${d.organicTreatment}\n• **Chemical Fungicide:** ${d.chemicalTreatment}\n• **Cultural Prevention:** ${d.prevention}\n\nHow can I assist further with this diagnosis?`,
        tools: ["Plant Disease Vision", "Agronomic Treatment Guide"],
        followups: [
          `What is the exact water dilution for ${d.chemicalTreatment?.split(" ")[0] || "spray"}?`,
          "Will upcoming rain wash away the spray?",
          "How can I prevent this disease next season?",
          "Are there any subsidized bio-pesticides under PKVY?"
        ]
      };
      setMessages((prev) => [...prev, diseaseSummaryMsg]);
      setPendingAiContext(null); // Clear context once injected
    }
  }, [pendingAiContext]);

  const handleSend = async (queryText) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

    const userMsg = { role: "user", content: textToSend };
    setMessages((prev) => [...prev, userMsg]);
    if (!queryText) setInput("");
    setLoading(true);

    try {
      const historyPayload = messages.map((m) => ({ role: m.role, content: m.content }));
      const res = await askAssistant(textToSend, historyPayload, profile);
      
      const botMsg = {
        role: "assistant",
        content: res.reply,
        tools: res.tools_used,
        intent: res.detected_intent,
        followups: res.suggested_followups
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "We're having trouble connecting right now. Please try again.",
          tools: ["Service Assistant"]
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const formatMarkdown = (text) => {
    if (!text) return "";
    return text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noreferrer" style="color: #059669; text-decoration: underline; font-weight: 600;">$1</a>')
      .replace(/\n/g, "<br />");
  };

  return (
    <div className="page-wrapper">
      {/* Header */}
      <div style={{ marginBottom: "16px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
          <span className="badge badge-green">AI Farmer Assistant</span>
          <span style={{ fontSize: "12px", color: "#64748b", fontWeight: 600 }}>Multi-Tool Agricultural Decision Support</span>
        </div>
        <h1 style={{ fontSize: "24px", fontWeight: 800, color: "#0f172a", letterSpacing: "-0.02em", margin: 0 }}>
          AI Farmer Assistant
        </h1>
        <p style={{ fontSize: "13px", color: "#64748b", marginTop: "2px" }}>
          Ask natural-language questions in English or Hindi. Grounded in weather, crop advisories, mandi prices, and government schemes.
        </p>
      </div>

      {/* Chat Container */}
      <div className="chat-container">
        {/* Messages Body */}
        <div className="chat-messages">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={msg.role === "user" ? "chat-bubble-user" : "chat-bubble-bot"}
            >
              {msg.role === "assistant" && msg.tools && msg.tools.length > 0 && (
                <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginBottom: "8px" }}>
                  {msg.tools.map((tool, ti) => (
                    <span
                      key={ti}
                      style={{
                        background: "#ecfdf5",
                        border: "1px solid #a7f3d0",
                        color: "#047857",
                        fontSize: "11px",
                        fontWeight: 700,
                        padding: "2px 8px",
                        borderRadius: "9999px",
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "4px"
                      }}
                    >
                      <Wrench size={10} /> {tool}
                    </span>
                  ))}
                </div>
              )}

              <div
                style={{ lineHeight: 1.55, fontSize: "13px" }}
                dangerouslySetInnerHTML={{ __html: formatMarkdown(msg.content) }}
              />

              {msg.followups && msg.followups.length > 0 && (
                <div style={{ marginTop: "12px", borderTop: "1px solid #f1f5f9", paddingTop: "8px" }}>
                  <div style={{ fontSize: "11px", color: "#64748b", fontWeight: 700, textTransform: "uppercase", marginBottom: "6px" }}>
                    Suggested Questions:
                  </div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                    {msg.followups.map((f, fi) => (
                      <button
                        key={fi}
                        onClick={() => handleSend(f)}
                        style={{
                          background: "#f1f5f9",
                          border: "1px solid #e2e8f0",
                          borderRadius: "9999px",
                          padding: "5px 10px",
                          fontSize: "11px",
                          color: "#334155",
                          cursor: "pointer",
                          fontWeight: 500,
                          transition: "all 0.15s ease",
                          textAlign: "left"
                        }}
                      >
                        {f}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="chat-bubble-bot" style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div style={{ display: "inline-block", animation: "spin 1s infinite linear" }}>
                <RefreshCw size={16} color="#059669" />
              </div>
              <span style={{ fontSize: "13px", color: "#64748b" }}>
                Analyzing agronomic insights & advice...
              </span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Chat Input Bar with Quick Camera Scanner Button */}
        <div style={{ padding: "12px 14px", background: "#ffffff", borderTop: "1px solid #e2e8f0" }}>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            style={{ display: "flex", gap: "8px", alignItems: "center" }}
          >
            {/* Quick Camera Scan Button */}
            <button
              type="button"
              onClick={() => setShowCameraScanner(true)}
              className="btn btn-secondary"
              style={{ padding: "10px", borderRadius: "10px", flexShrink: 0 }}
              title="Scan Plant Disease Leaf"
              aria-label="Scan Plant Leaf"
            >
              <Camera size={18} color="#059669" />
            </button>

            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything (e.g. spray timing, mandi rate, crop advice)..."
              className="form-input"
              style={{ padding: "10px 14px", fontSize: "13px", margin: 0 }}
            />

            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="btn btn-primary"
              style={{ padding: "10px 16px", flexShrink: 0 }}
              aria-label="Send Message"
            >
              <Send size={16} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
