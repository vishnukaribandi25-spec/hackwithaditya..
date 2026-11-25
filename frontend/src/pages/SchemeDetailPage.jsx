import React, { useEffect, useState } from "react"
import { useParams, Link } from "react-router-dom"
import ChatPanel from "../components/ChatPanel"
import { getScheme } from "../services/api"
import { useApp } from "../context/AppContext"

export default function SchemeDetailPage() {
  const { id } = useParams()
  const { language } = useApp()
  const [scheme, setScheme] = useState(null)
  const [error, setError] = useState("")
  const telugu = language === "te"

  useEffect(() => {
    getScheme(id).then((response) => setScheme(response.data)).catch(() => setError("Scheme not found"))
  }, [id])

  if (error) return <main className="page"><p className="form-error">{error}</p></main>
  if (!scheme) return <main className="page"><p>Loading…</p></main>

  return (
    <main className="detail-layout">
      <section className="detail-main">
        <Link className="back-link" to="/schemes">← {telugu ? "పథకాలకి తిరిగి" : "Back to schemes"}</Link>
        <span className="eyebrow">{scheme.department}</span>
        <h1>{telugu ? scheme.name_te : scheme.name}</h1>
        <p className="detail-description">{telugu ? scheme.description_te : scheme.description}</p>

        <div className="detail-section">
          <h2>{telugu ? "పని ప్రయోజనాలు" : "Benefits"}</h2>
          <ul className="check-list">{scheme.benefits.map((item) => <li key={item}>{item}</li>)}</ul>
        </div>

        <div className="detail-section">
          <h2>{telugu ? "పత్రాల చెక్లిస్ట్" : "Required documents"}</h2>
          <ul className="document-list">{scheme.documents.map((item) => <li key={item}><span>□</span>{item}</li>)}</ul>
        </div>

        <div className="detail-section">
          <h2>{telugu ? "దరఖాస్తు ఎలా చేయాలి" : "How to apply"}</h2>
          <ol className="steps">
            {(telugu ? scheme.application_steps_te : scheme.application_steps).map((step) => <li key={step}>{step}</li>)}
          </ol>
          <a className="button primary" href={scheme.application_link} target="_blank" rel="noreferrer">
            {telugu ? "అధికారిక పోర్టల్‌ను తెరవండి" : "Open official application portal"}
          </a>
        </div>

        <div className="source-box">
          <strong>{telugu ? "అధికారిక మూలం" : "Official source"}</strong>
          <a href={scheme.official_source} target="_blank" rel="noreferrer">{scheme.official_source}</a>
          <span>Last verified: {scheme.last_verified}</span>
        </div>
      </section>
      <ChatPanel scheme={scheme} />
    </main>
  )
}
