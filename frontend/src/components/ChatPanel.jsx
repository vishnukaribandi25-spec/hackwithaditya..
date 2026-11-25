import React, { useState } from "react"
import { sendChat } from "../services/api"
import { useApp } from "../context/AppContext"

export default function ChatPanel({ scheme }) {
  const { language } = useApp()
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  async function submit(event) {
    event.preventDefault()
    if (!input.trim()) return
    const question = input.trim()
    setMessages((current) => [...current, { role: "user", text: question }])
    setInput("")
    setLoading(true)
    try {
      const response = await sendChat(question, language, scheme)
      setMessages((current) => [...current, { role: "assistant", text: response.data.reply }])
    } catch {
      setMessages((current) => [...current, {
        role: "assistant",
        text: language === "te"
          ? "AI ఇప్పుడు అందుబాటులో లేదు. పథక వివరాలను చూడండి."
          : "AI is unavailable. Please review the verified scheme details."
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <aside className="chat-panel">
      <div className="chat-header">
        <div>
          <strong>{language === "te" ? "సహాయక చాట్" : "Scheme Assistant"}</strong>
          <span>{language === "te" ? "తెలుగు లేదా ఇంగ్లీష్‌లో అడగండి" : "Ask in English or Telugu"}</span>
        </div>
      </div>
      <div className="chat-messages" aria-live="polite">
        {messages.length === 0 && (
          <p className="chat-empty">
            {language === "te"
              ? "ఈ పథకం గురించి నమ్మకంగా చెప్పగల సమాచారం మాత్రమే."
              : "Ask about documents, benefits or application steps."}
          </p>
        )}
        {messages.map((message, index) => (
          <div key={index} className={`bubble ${message.role}`}>{message.text}</div>
        ))}
        {loading && <div className="bubble assistant">Thinking…</div>}
      </div>
      <form className="chat-form" onSubmit={submit}>
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder={language === "te" ? "మీ ప్రశ్న రాయండి…" : "Ask a question…"}
          aria-label="Chat message"
        />
        <button type="submit" disabled={loading} aria-label="Send">→</button>
      </form>
    </aside>
  )
}
