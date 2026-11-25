import React, { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { listSchemes } from "../services/api"
import { useApp } from "../context/AppContext"
import { localizedError, localizedScheme, localizedState, t } from "../i18n"

export default function SchemeCatalogPage() {
  const { language } = useApp()
  const [schemes, setSchemes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let active = true
    listSchemes()
      .then((response) => {
        if (active) {
          setSchemes(response.data.filter((scheme) => scheme.verification_status === "verified"))
        }
      })
      .catch((requestError) => {
        if (active) setError(requestError)
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => { active = false }
  }, [])

  return (
    <main className="page">
      <div className="page-heading">
        <span className="eyebrow">{t(language, "verifiedCatalogue")}</span>
        <h1>{t(language, "governmentSchemeInfo")}</h1>
        <p>{t(language, "catalogueIntro")}</p>
      </div>
      {loading ? (
        <div className="empty-state"><p>{t(language, "loadingCatalogue")}</p></div>
      ) : error ? (
        <div className="empty-state"><p className="form-error">{localizedError(error, language)}</p></div>
      ) : schemes.length === 0 ? (
        <div className="empty-state"><p>{t(language, "noVerifiedSchemes")}</p></div>
      ) : (
        <div className="results-grid">
          {schemes.map((record) => {
            const scheme = localizedScheme(record, language)
            return <article className="scheme-card" key={scheme.id}>
              <div className="scheme-card-top">
                <span className="status eligible">{t(language, "verifiedSource")}</span>
                <span className="verified">{scheme.last_verified || t(language, "dateUnavailable")}</span>
              </div>
              <h2>{language === "te" ? scheme.name_te || scheme.name : scheme.name}</h2>
              <p className="department">{language === "te" ? scheme.department_te || scheme.department : scheme.department}</p>
              <p className="description">{language === "te" ? scheme.description_te || scheme.description : scheme.description}</p>
              <div className="scheme-source">
                {scheme.source_url && <a href={scheme.source_url} target="_blank" rel="noreferrer">{t(language, "officialSource")}</a>}
                <span>{localizedState(scheme.state, language)}</span>
              </div>
              <div className="card-actions">
                <Link
                  className="button secondary"
                  to={`/schemes/${scheme.id}`}
                  state={{ from: "/catalog" }}
                >
                  {t(language, "viewSchemeDetails")}
                </Link>
              </div>
            </article>
          })}
        </div>
      )}
    </main>
  )
}
