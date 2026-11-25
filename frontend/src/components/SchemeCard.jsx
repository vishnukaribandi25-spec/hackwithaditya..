import React from "react"
import { Link } from "react-router-dom"
import { useApp } from "../context/AppContext"
import { localizeEligibilityText, localizedScheme, t } from "../i18n"

function ConditionList({ title, items, className = "" }) {
  if (!items?.length) return null
  return (
    <div className={`result-detail ${className}`}>
      <strong>{title}</strong>
      <ul>{items.map((item) => <li key={item}>{item}</li>)}</ul>
    </div>
  )
}

export default function SchemeCard({ match }) {
  const { language } = useApp()
  const statusKey = match.match_group === "not_applicable"
    ? "notApplicableBadge"
    : match.status === "potentially_eligible"
      ? "potentiallyEligible"
      : "verificationRequired"
  const statusClass = match.match_group === "not_applicable"
    ? "not-eligible"
    : match.status === "potentially_eligible"
      ? "eligible"
      : "verification"
  const scheme = localizedScheme(match.scheme, language)
  const isRecommendation = match.match_group !== "not_applicable"
  const sourceUrl = match.source_url || scheme.source_url
  const lastVerified = match.last_verified_date || scheme.last_verified
  const explanation = localizeEligibilityText(
    match.explanation || match.explanation_reasons?.join(" "),
    language
  )
  const localizedItems = (items) =>
    (items || []).map((item) => localizeEligibilityText(item, language))
  const verificationSteps = language === "te"
    ? scheme.application_process_te || localizedItems(match.verification_steps)
    : match.verification_steps

  return (
    <article className="scheme-card">
      <div className="scheme-card-top">
        <span className={`status ${statusClass}`}>{t(language, statusKey)}</span>
        <span className="verified">
          {match.verification_status === "verified"
            ? t(language, "verifiedSource")
            : t(language, "notVerified")}
        </span>
      </div>
      <h3>{language === "te" ? scheme.name_te || scheme.name : scheme.name}</h3>
      <p className="department">{language === "te" ? scheme.department_te || scheme.department : scheme.department}</p>
      <p className="description">{language === "te" ? scheme.description_te || scheme.description : scheme.description}</p>
      <p className="explanation">{explanation}</p>
      {isRecommendation && (
        <ConditionList
          title={t(language, "matchedDetails")}
          items={localizedItems(match.matched_conditions)}
        />
      )}
      <ConditionList
        title={t(language, "failedConditions")}
        items={localizedItems(match.failed_conditions)}
        className="failed-detail"
      />
      {isRecommendation && (
        <ConditionList
          title={t(language, "missingChecks")}
          items={localizedItems(match.missing_information)}
        />
      )}
      {isRecommendation && match.verification_required && (
        <ConditionList
          title={t(language, "verificationSteps")}
          items={verificationSteps}
        />
      )}
      <div className="card-actions">
        <Link className="button secondary" to={`/schemes/${scheme.id}`} state={{ from: "/schemes" }}>
          {t(language, "viewDetails")}
        </Link>
      </div>
      <div className="scheme-source">
        {sourceUrl
          ? <a href={sourceUrl} target="_blank" rel="noreferrer">{t(language, "officialSource")}</a>
          : <span>{t(language, "sourceUnavailable")}</span>}
        <span>{lastVerified
          ? `${t(language, "lastVerified")}: ${lastVerified}`
          : t(language, "verificationDateUnavailable")}</span>
      </div>
    </article>
  )
}
