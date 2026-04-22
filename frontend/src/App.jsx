import { useEffect, useMemo, useRef, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

function CoffeeIcon() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 8h1a4 4 0 0 1 0 8h-1" />
      <path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z" />
      <line x1="6" y1="2" x2="6" y2="4" />
      <line x1="10" y1="2" x2="10" y2="4" />
      <line x1="14" y1="2" x2="14" y2="4" />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="22" y1="2" x2="11" y2="13" />
      <polygon points="22 2 15 22 11 13 2 9 22 2" />
    </svg>
  );
}

function SpinnerIcon() {
  return (
    <svg className="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
      <path d="M12 2a10 10 0 0 1 10 10" />
    </svg>
  );
}

function StatusDot({ ok }) {
  return <span className={`status-dot ${ok ? "ok" : "err"}`} />;
}

function TypingDots() {
  return (
    <div className="typing-dots">
      <span /><span /><span />
    </div>
  );
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "ሰላም! ስለ ቡና ማፍላት፣ ጥራት፣ ግብይት ወይም ታሪክ ጥያቄ ይጠይቁ።",
      contexts: [],
    },
  ]);
  const [input, setInput] = useState("");
  const [topK, setTopK] = useState(3);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [backendInfo, setBackendInfo] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  const canSend = useMemo(() => input.trim().length > 0 && !loading, [input, loading]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(e) {
    e.preventDefault();
    if (!canSend) return;
    const userMessage = { role: "user", content: input.trim(), contexts: [] };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.content, top_k: topK }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Request failed");
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer || "", contexts: data.contexts || [] },
      ]);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }

  async function checkBackend() {
    try {
      const res = await fetch(`${API_BASE}/health`);
      const data = await res.json();
      if (res.ok) setBackendInfo(data);
    } catch {
      setBackendInfo(null);
    }
  }

  async function rebuildIndex() {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/index/rebuild`, { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to rebuild index");
      setError("");
    } catch (err) {
      setError(err.message || "Failed to rebuild index.");
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(e);
    }
  }

  return (
    <div className="app">
      {/* Mobile overlay */}
      {sidebarOpen && <div className="overlay" onClick={() => setSidebarOpen(false)} />}

      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <div className="logo">
            <CoffeeIcon />
            <div>
              <div className="logo-title">Buna</div>
              <div className="logo-sub">Ethiopian Coffee Knowledge</div>
            </div>
          </div>
        </div>

        <div className="sidebar-section">
          <div className="section-label">Retrieval</div>
          <div className="topk-control">
            <div className="topk-header">
              <span>Top K Sources</span>
              <span className="topk-value">{topK}</span>
            </div>
            <input
              type="range"
              min="1"
              max="8"
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="slider"
            />
            <div className="topk-labels"><span>1</span><span>8</span></div>
          </div>
        </div>

        <div className="sidebar-section">
          <div className="section-label">System</div>
          <button className="sidebar-btn" onClick={checkBackend} disabled={loading}>
            Check Backend Status
          </button>
          {backendInfo && (
            <div className="backend-card">
              <div className="backend-row">
                <StatusDot ok={backendInfo.gemini_status === "ready"} />
                <span>Gemini {backendInfo.gemini_status}</span>
              </div>
              <div className="backend-model">{backendInfo.active_model}</div>
              {backendInfo.gemini_error && (
                <div className="backend-error">{backendInfo.gemini_error}</div>
              )}
            </div>
          )}
          <button className="sidebar-btn accent" onClick={rebuildIndex} disabled={loading}>
            {loading ? "Building…" : "Rebuild Index"}
          </button>
        </div>

        <div className="sidebar-footer">
          <span>Ethiopian Coffee Resources</span>
        </div>
      </aside>

      {/* Main */}
      <div className="main">
        {/* Top bar */}
        <header className="topbar">
          <button className="menu-btn" onClick={() => setSidebarOpen((v) => !v)} aria-label="Menu">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>
          <div className="topbar-title">
            <CoffeeIcon />
            <span>Buna</span>
          </div>
          <div className="topbar-right" />
        </header>

        {/* Messages */}
        <div className="messages">
          {messages.map((m, idx) => (
            <div key={idx} className={`msg-row ${m.role}`}>
              {m.role === "assistant" && (
                <div className="avatar">
                  <CoffeeIcon />
                </div>
              )}
              <div className="bubble-wrap">
                <div className="bubble">
                  <p>{m.content}</p>
                  {m.role === "assistant" && m.contexts?.length > 0 && (
                    <details className="evidence-details">
                      <summary>
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><polyline points="6 9 12 15 18 9" /></svg>
                        {m.contexts.length} source{m.contexts.length > 1 ? "s" : ""}
                      </summary>
                      <div className="evidence-list">
                        {m.contexts.map((ctx, i) => (
                          <div key={i} className="evidence-item">
                            <div className="evidence-meta">
                              <span className="evidence-source">{ctx.source}</span>
                              <span className="evidence-score">score {ctx.score?.toFixed?.(3)}</span>
                            </div>
                            <p className="evidence-text">{ctx.text}</p>
                          </div>
                        ))}
                      </div>
                    </details>
                  )}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="msg-row assistant">
              <div className="avatar"><CoffeeIcon /></div>
              <div className="bubble-wrap">
                <div className="bubble"><TypingDots /></div>
              </div>
            </div>
          )}

          {error && <div className="error-banner">{error}</div>}
          <div ref={bottomRef} />
        </div>

        {/* Composer */}
        <div className="composer-wrap">
          <form className="composer" onSubmit={sendMessage}>
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="ጥያቄዎን በአማርኛ ይጻፉ…"
              maxLength={500}
              rows={1}
              className="composer-input"
            />
            <button type="submit" disabled={!canSend} className="send-btn" aria-label="Send">
              {loading ? <SpinnerIcon /> : <SendIcon />}
            </button>
          </form>
          <div className="composer-hint">Enter to send · Shift+Enter for new line</div>
        </div>
      </div>
    </div>
  );
}
