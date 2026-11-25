import React, { useEffect, useState } from "react"
import { useParams, Link } from "react-router-dom"
import { getScheme } from "../services/api"
import { useApp } from "../context/AppContext"

function describeRule(rule) {
  const label = rule.label || rule.type.replaceAll("_", " ")
  if (rule.values) return `${label}: ${rule.values.join(", ")}`
  if (rule.min !== undefined || rule.max !== undefined) {
    return `${label}: ${rule.min ?? "no minimum"} to ${rule.max ?? "no maximum"}`
  }
  if (rule.attribute) return `${label}: ${rule.attribute} ${rule.operator || "is"} ${rule.value ?? ""}`
  return `${label}: details need verification`
}

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

  const isMock = scheme.verification_status === "mock"
  return (
    <main className="page detail-page">
      <section className="detail-main">
        <Link className="back-link" to="/schemes">← {telugu ? "పథకాలకి తిరిగి" : "Back to schemes"}</Link>
        <span className="eyebrow">{scheme.department}</span>
        <h1>{telugu ? scheme.name_te || scheme.name : scheme.name}</h1>
        <p className="detail-description">{telugu ? scheme.description_te || scheme.description : scheme.description}</p>
        {isMock && <p className="disclaimer">Mock development data only. This is not a government scheme.</p>}

        <div className="detail-section">
          <h2>{telugu ? "పని ప్రయోజనాలు" : "Benefits"}</h2>
          <ul className="check-list">{scheme.benefits.map((item) => <li key={item}>{item}</li>)}</ul>
        </div>

        <div className="detail-section">
          <h2>{telugu ? "పాత్రత నియమాలు" : "Eligibility rules"}</h2>
          <ul className="check-list">
            {scheme.eligibility_rules.map((rule, index) => <li key={`${rule.type}-${index}`}>{describeRule(rule)}</li>)}
          </ul>
        </div>

        <div className="detail-section">
          <h2>{telugu ? "పత్రాల చెక్లిస్ట్" : "Required documents"}</h2>
          <ul className="document-list">{scheme.required_documents.map((item) => <li key={item}><span>□</span>{item}</li>)}</ul>
        </div>

        <div className="detail-section">
          <h2>{telugu ? "దరఖాస్తు ఎలా చేయాలి" : "How to apply"}</h2>
          {scheme.application_url ? (
            <a className="button primary" href={scheme.application_url} target="_blank" rel="noreferrer">
              {telugu ? "అధికారిక పోర్టల్‌ను తెరవండి" : "Open official application portal"}
            </a>
          ) : (
            <p>{isMock ? "No application link is provided for this mock record." : "No application link is currently available."}</p>
          )}
        </div>

        <div className="source-box">
          <strong>{telugu ? "మూలం" : "Source"}</strong>
          {scheme.source_url
            ? <a href={scheme.source_url} target="_blank" rel="noreferrer">{scheme.source_url}</a>
            : <span>No source URL is available for this record.</span>}
          <span>
            {scheme.last_verified ? `Last verified: ${scheme.last_verified}` : "Not verified"}
          </span>
        </div>
      </section>
    </main>
  )
}
