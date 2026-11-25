import React, { useEffect, useState } from "react"
import { useParams, Link, useLocation } from "react-router-dom"
import { getScheme } from "../services/api"
import { useApp } from "../context/AppContext"
import { describeRule, localizedError, localizedScheme, localizedState, t } from "../i18n"

export default function SchemeDetailPage() {
  const { id } = useParams()
  const location = useLocation()
  const { language } = useApp()
  const [scheme, setScheme] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    setError(null)
    setScheme(null)
    getScheme(id)
      .then((response) => setScheme(response.data))
      .catch((requestError) => {
        setError(requestError.response?.status === 404
          ? { kind: "scheme_not_found" }
          : requestError)
      })
  }, [id])

  if (error) return <main className="page"><p className="form-error">{localizedError(error, language)}</p></main>
  if (!scheme) return <main className="page"><p>{t(language, "loading")}</p></main>

  const localized = localizedScheme(scheme, language)
  const isMock = localized.verification_status === "mock"
  const unavailable = new Set(localized.unavailable_fields || [])
  const benefits = language === "te" ? localized.benefits_te : localized.benefits
  const documents = language === "te" ? localized.required_documents_te : localized.required_documents
  const applicationProcess = language === "te"
    ? localized.application_process_te
    : localized.application_process
  return (
    <main className="page detail-page">
      <section className="detail-main">
        <Link className="back-link" to={location.state?.from || "/schemes"}>← {t(language, "backToSchemes")}</Link>
        <span className="eyebrow">{language === "te" ? localized.department_te || localized.department : localized.department}</span>
        <h1>{language === "te" ? localized.name_te || localized.name : localized.name}</h1>
        <p className="detail-description">{language === "te" ? localized.description_te || localized.description : localized.description}</p>
        <p>
          {localized.government_level === "central"
            ? t(language, "centralGovernment")
            : localized.government_level === "state"
              ? t(language, "stateGovernment")
              : t(language, "governmentLevelUnavailable")}
          {" · "}{localizedState(localized.state, language)}
          {localized.state_exclusions?.length
            ? ` (${t(language, "notImplementedIn")} ${localized.state_exclusions.map((state) => localizedState(state, language)).join(", ")})`
            : ""}
        </p>
        {isMock && <p className="disclaimer">{t(language, "mockDisclaimer")}</p>}

        <div className="detail-section">
          <h2>{t(language, "benefits")}</h2>
          {benefits.length ? (
            <ul className="check-list">{benefits.map((item) => <li key={item}>{item}</li>)}</ul>
          ) : (
            <p>{unavailable.has("benefits") ? t(language, "verifiedSourceUnavailable") : t(language, "noBenefitDetails")}</p>
          )}
        </div>

        <div className="detail-section">
          <h2>{t(language, "eligibilityRules")}</h2>
          {(language === "te" ? localized.eligibility_summary_te : localized.eligibility_summary)
            && <p>{language === "te" ? localized.eligibility_summary_te : localized.eligibility_summary}</p>}
          <ul className="check-list">
            {localized.eligibility_rules.map((rule, index) => <li key={`${rule.type}-${index}`}>{describeRule(rule, language)}</li>)}
          </ul>
          {!localized.eligibility_rules.length && <p>{t(language, "manualVerification")}</p>}
        </div>

        <div className="detail-section">
          <h2>{t(language, "requiredDocuments")}</h2>
          {documents.length ? (
            <ul className="document-list">{documents.map((item) => <li key={item}><span>□</span>{item}</li>)}</ul>
          ) : (
            <p>{unavailable.has("required_documents") ? t(language, "documentsUnavailable") : t(language, "noDocumentDetails")}</p>
          )}
        </div>

        <div className="detail-section">
          <h2>{t(language, "howToApply")}</h2>
          {applicationProcess.length ? (
            <ol className="check-list">{applicationProcess.map((step, index) => <li key={`${index}-${step}`}>{step}</li>)}</ol>
          ) : (
            <p>{unavailable.has("application_process") ? t(language, "applicationUnavailable") : t(language, "noApplicationSteps")}</p>
          )}
          {localized.application_url ? (
            <a className="button primary" href={localized.application_url} target="_blank" rel="noreferrer">
              {t(language, "openApplicationPortal")}
            </a>
          ) : (
            <p>{isMock ? t(language, "noMockApplicationLink") : t(language, "noApplicationLink")}</p>
          )}
        </div>

        <div className="source-box">
          <strong>{t(language, "source")}</strong>
          {localized.source_url
            ? <a href={localized.source_url} target="_blank" rel="noreferrer">{localized.source_url}</a>
            : <span>{t(language, "sourceUrlUnavailable")}</span>}
          <span>
            {localized.last_verified
              ? `${t(language, "lastVerified")}: ${localized.last_verified}`
              : t(language, "notVerified")}
          </span>
        </div>
      </section>
    </main>
  )
}
