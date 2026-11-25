import React, { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import SchemeCard from "../components/SchemeCard"
import { matchSchemes } from "../services/api"
import { useApp } from "../context/AppContext"
import { localizeEligibilityText, localizedError, t } from "../i18n"

export default function ResultsPage() {
  const { language, profile, matches, setMatches } = useApp()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let active = true
    if (!profile || matches?.matches) {
      setLoading(false)
      return () => { active = false }
    }

    setLoading(true)
    setError("")
    matchSchemes(profile)
      .then((response) => {
        if (active) setMatches(response.data)
      })
      .catch((requestError) => {
        if (active) setError(requestError)
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => { active = false }
  }, [matches, profile, setMatches])

  const recommendations = matches?.matches || []
  const notApplicable = matches?.not_applicable || []
  const isFarmer = profile?.occupation?.trim().replace(/\s+/g, " ").toLowerCase() === "farmer"
  const hasResults = recommendations.length > 0 || notApplicable.length > 0

  return (
    <main className="page">
      <div className="results-heading">
        <div>
          <span className="eyebrow">{t(language, "yourResults")}</span>
          <h1>{isFarmer ? t(language, "farmerResults") : t(language, "potentialMatches")}</h1>
        </div>
        <Link className="button secondary" to="/profile">{t(language, "editProfile")}</Link>
      </div>
      {loading ? (
        <div className="empty-state"><p>{t(language, "loadingResults")}</p></div>
      ) : error ? (
        <div className="empty-state"><p className="form-error">{localizedError(error, language)}</p></div>
      ) : !profile ? (
        <div className="empty-state">
          <p>{t(language, "completeProfile")}</p>
          <Link className="button primary" to="/profile">{t(language, "createProfile")}</Link>
        </div>
      ) : (
        <>
          {matches?.disclaimer && <p className="disclaimer">{localizeEligibilityText(matches.disclaimer, language)}</p>}
          {recommendations.some((match) => match.status === "potentially_eligible") && (
            <section className="results-section">
              <h2>{isFarmer
                ? t(language, "likelyFarmerSchemes")
                : t(language, "potentiallyRelevantSchemes")}</h2>
              <div className="results-grid">
                {recommendations
                  .filter((match) => match.status === "potentially_eligible")
                  .map((match) => <SchemeCard key={match.scheme.id} match={match} />)}
              </div>
            </section>
          )}
          {recommendations.some((match) => match.status === "needs_verification") && (
            <section className="results-section">
              <h2>{t(language, "needsVerification")}</h2>
              <div className="results-grid">
                {recommendations
                  .filter((match) => match.status === "needs_verification")
                  .map((match) => <SchemeCard key={match.scheme.id} match={match} />)}
              </div>
            </section>
          )}
          {notApplicable.length > 0 && (
            <section className="results-section">
              <h2>{t(language, "notApplicable")}</h2>
              <p className="section-note">{t(language, "notApplicableNote")}</p>
              <div className="results-grid">
                {notApplicable.map((match) => <SchemeCard key={match.scheme.id} match={match} />)}
              </div>
            </section>
          )}
          {recommendations.length === 0 && notApplicable.length > 0 && (
            <div className="empty-state">
              <p>{t(language, "noRecommendations")}</p>
            </div>
          )}
          {!hasResults && (
            <div className="empty-state">
              <p>{t(language, "noEvaluatedSchemes")}</p>
            </div>
          )}
        </>
      )}
    </main>
  )
}
