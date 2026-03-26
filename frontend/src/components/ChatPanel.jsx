import { useState, useRef, useEffect } from "react";
import axios from "axios";

export default function ChatPanel({ selectedNode }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi! I can help you analyze the **Order to Cash** process. Ask me anything about orders, deliveries, billing, or payments.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (selectedNode) {
      setInput(`Tell me about ${selectedNode.type} ${selectedNode.id}`);
    }
  }, [selectedNode]);

  async function sendMessage() {
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: userMsg }]);
    setLoading(true);

    try {
      const res = await axios.post("https://o2c-graph-ai-1.onrender.com/api/chat", {
        question: userMsg,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: res.data.answer,
          sql: res.data.sql,
          data: res.data.data,
        },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Sorry, something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div style={{
      width: 340, background: "white",
      borderLeft: "1px solid #e5e5e5",
      display: "flex", flexDirection: "column",
      height: "100%"
    }}>
      {/* Header */}
      <div style={{
        padding: "14px 16px",
        borderBottom: "1px solid #f0f0f0",
      }}>
        <div style={{ fontSize: 13, fontWeight: 600, color: "#333" }}>Chat with Graph</div>
        <div style={{ fontSize: 11, color: "#999", marginTop: 2 }}>Order to Cash</div>
      </div>

      {/* Messages */}
      <div style={{
        flex: 1, overflowY: "auto",
        padding: "16px", display: "flex",
        flexDirection: "column", gap: 12
      }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            display: "flex",
            flexDirection: msg.role === "user" ? "row-reverse" : "row",
            gap: 8, alignItems: "flex-start"
          }}>
            {msg.role === "assistant" && (
              <div style={{
                width: 28, height: 28, borderRadius: "50%",
                background: "#222", color: "white",
                display: "flex", alignItems: "center",
                justifyContent: "center", fontSize: 12,
                fontWeight: 700, flexShrink: 0
              }}>
                D
              </div>
            )}
            <div style={{
              maxWidth: "80%",
              background: msg.role === "user" ? "#222" : "#f5f5f5",
              color: msg.role === "user" ? "white" : "#333",
              padding: "10px 12px",
              borderRadius: msg.role === "user" ? "12px 12px 4px 12px" : "12px 12px 12px 4px",
              fontSize: 13, lineHeight: 1.5
            }}>
              {msg.text}

              {msg.sql && (
                <details style={{ marginTop: 8 }}>
                  <summary style={{ fontSize: 11, color: "#888", cursor: "pointer" }}>
                    View SQL
                  </summary>
                  <pre style={{
                    fontSize: 10, background: "#fff",
                    padding: 8, borderRadius: 4,
                    marginTop: 4, overflow: "auto",
                    color: "#555", border: "1px solid #eee"
                  }}>
                    {msg.sql}
                  </pre>
                </details>
              )}

              {msg.data && msg.data.length > 0 && (
                <details style={{ marginTop: 6 }}>
                  <summary style={{ fontSize: 11, color: "#888", cursor: "pointer" }}>
                    View Data ({msg.data.length} rows)
                  </summary>
                  <div style={{ overflowX: "auto", marginTop: 4 }}>
                    <table style={{
                      fontSize: 10, borderCollapse: "collapse",
                      width: "100%"
                    }}>
                      <thead>
                        <tr>
                          {Object.keys(msg.data[0]).map((k) => (
                            <th key={k} style={{
                              padding: "4px 6px", background: "#f0f0f0",
                              border: "1px solid #ddd", textAlign: "left",
                              whiteSpace: "nowrap"
                            }}>{k}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {msg.data.slice(0, 5).map((row, ri) => (
                          <tr key={ri}>
                            {Object.values(row).map((v, vi) => (
                              <td key={vi} style={{
                                padding: "3px 6px",
                                border: "1px solid #eee",
                                whiteSpace: "nowrap"
                              }}>
                                {String(v ?? "").substring(0, 20)}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </details>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <div style={{
              width: 28, height: 28, borderRadius: "50%",
              background: "#222", color: "white",
              display: "flex", alignItems: "center",
              justifyContent: "center", fontSize: 12, fontWeight: 700
            }}>D</div>
            <div style={{
              background: "#f5f5f5", padding: "10px 14px",
              borderRadius: "12px 12px 12px 4px", fontSize: 13, color: "#999"
            }}>
              Thinking...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Status */}
      <div style={{
        padding: "8px 16px",
        borderTop: "1px solid #f0f0f0",
        fontSize: 11, color: "#888",
        display: "flex", alignItems: "center", gap: 6
      }}>
        <div style={{
          width: 6, height: 6, borderRadius: "50%",
          background: loading ? "#FFA500" : "#4CAF50"
        }} />
        {loading ? "Processing..." : "Ready"}
      </div>

      {/* Input */}
      <div style={{
        padding: "12px 16px",
        borderTop: "1px solid #f0f0f0",
        display: "flex", gap: 8
      }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Ask anything about the data..."
          rows={2}
          style={{
            flex: 1, padding: "8px 12px",
            border: "1px solid #e5e5e5",
            borderRadius: 8, fontSize: 13,
            resize: "none", outline: "none",
            fontFamily: "inherit", color: "#333"
          }}
        />
        <button
          onClick={sendMessage}
          disabled={loading || !input.trim()}
          style={{
            padding: "8px 16px",
            background: loading || !input.trim() ? "#ccc" : "#222",
            color: "white", border: "none",
            borderRadius: 8, cursor: loading ? "not-allowed" : "pointer",
            fontSize: 13, fontWeight: 600,
            alignSelf: "flex-end"
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}