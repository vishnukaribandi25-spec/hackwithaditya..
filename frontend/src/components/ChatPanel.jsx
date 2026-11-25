import React, { useState } from "react"
import { sendChat } from "../services/api"
import { useApp } from "../context/AppContext"
import { t } from "../i18n"

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
        text: t(language, "aiUnavailable")
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <aside className="chat-panel">
      <div className="chat-header">
        <div>
          <strong>{t(language, "assistant")}</strong>
          <span>{t(language, "askLanguage")}</span>
        </div>
      </div>
      <div className="chat-messages" aria-live="polite">
        {messages.length === 0 && (
          <p className="chat-empty">
            {t(language, "chatEmpty")}
          </p>
        )}
        {messages.map((message, index) => (
          <div key={index} className={`bubble ${message.role}`}>{message.text}</div>
        ))}
        {loading && <div className="bubble assistant">{t(language, "thinking")}</div>}
      </div>
      <form className="chat-form" onSubmit={submit}>
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder={t(language, "chatPlaceholder")}
          aria-label={t(language, "chatMessage")}
        />
        <button type="submit" disabled={loading} aria-label={t(language, "send")}>→</button>
      </form>
    </aside>
  )
}
