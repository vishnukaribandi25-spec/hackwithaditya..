import React from "react"
import { Link } from "react-router-dom"
import { useApp } from "../context/AppContext"

const statusConfig = {
  potentially_eligible: { en: "Potentially eligible", te: "సంభావ్యంగా पात्रులు", className: "eligible" },
  not_eligible: { en: "Not eligible", te: "పాత్రులు కారు", className: "not-eligible" },
  needs_verification: { en: "Needs verification", te: "ధృవీకరణ అవసరం", className: "verification" }
}

export default function SchemeCard({ match }) {
  const { language } = useApp()
  const status = statusConfig[match.status] || statusConfig.needs_verification
  const scheme = match.scheme
  const verificationLabel = scheme.verification_status === "mock"
    ? "Mock development data"
    : scheme.verification_status === "verified"
      ? `Verified ${scheme.last_verified || ""}`
      : "Not verified"
  return (
    <article className="scheme-card">
      <div className="scheme-card-top">
        <span className={`status ${status.className}`}>{status[language]}</span>
        <span className="verified">{verificationLabel}</span>
      </div>
      <h3>{language === "te" ? scheme.name_te || scheme.name : scheme.name}</h3>
      <p className="department">{scheme.department}</p>
      <p className="description">{language === "te" ? scheme.description_te || scheme.description : scheme.description}</p>
      <p className="explanation">{match.explanation || match.explanation_reasons?.join(" ")}</p>
      <div className="card-actions">
        <Link className="button secondary" to={`/schemes/${scheme.id}`}>
          {language === "te" ? "వివరాలు చూడండి" : "View details"}
        </Link>
      </div>
    </article>
  )
}
