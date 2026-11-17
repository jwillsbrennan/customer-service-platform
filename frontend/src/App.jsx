import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [messages, setMessages] = useState([
    { sender: "assistant", content: "Hello! Welcome to customer support. How can I help you today?" }
  ]);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [mode, setMode] = useState("");

  async function sendMessage(event) {
    event.preventDefault();
    const clean = message.trim();
    if (!clean || busy) return;

    setMessages((current) => [...current, { sender: "customer", content: clean }]);
    setMessage("");
    setError("");
    setBusy(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: clean })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "The request could not be completed.");
      setMessages((current) => [...current, { sender: "assistant", content: data.reply }]);
      setMode(data.mode);
    } catch (err) {
      setError(err.message || "Unable to reach the service. Check that the backend is running.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="page">
      <section className="chat-card">
        <header>
          <div className="eyebrow">GROUP 8 · ALPHA MVP</div>
          <h1>Customer Support</h1>
          <p>Ask a question and our support assistant will respond.</p>
        </header>
        <div className="messages" aria-live="polite">
          {messages.map((item, index) => (
            <div className={`message ${item.sender}`} key={index}>
              <span>{item.sender === "customer" ? "You" : "Support assistant"}</span>
              <p>{item.content}</p>
            </div>
          ))}
          {busy && <div className="status">Assistant is preparing a response…</div>}
        </div>
        {error && <p className="error" role="alert">{error}</p>}
        <form onSubmit={sendMessage}>
          <label className="sr-only" htmlFor="message">Your message</label>
          <input
            id="message"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Type your question…"
            maxLength={2000}
            disabled={busy}
          />
          <button disabled={busy || !message.trim()}>{busy ? "Sending…" : "Send"}</button>
        </form>
        <footer>
          {mode === "demo" && "Demo mode: connect an API key to enable AI responses."}
          {mode === "openai" && "AI response generated. Please verify important information."}
          {!mode && "Do not enter passwords, payment details, or sensitive personal information."}
        </footer>
      </section>
    </main>
  );
}
