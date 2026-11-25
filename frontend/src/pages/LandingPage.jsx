import React from "react"
import { Link } from "react-router-dom"
import { useApp } from "../context/AppContext"
import { t } from "../i18n"

export default function LandingPage() {
  const { language } = useApp()
  return (
    <main>
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">{t(language, "heroEyebrow")}</span>
          <h1>{t(language, "heroTitle")}</h1>
          <p>{t(language, "heroDescription")}</p>
          <div className="hero-actions">
            <Link className="button primary" to="/profile">
              {t(language, "startProfile")}
            </Link>
            <Link className="button text" to="/catalog">
              {t(language, "browseVerified")}
            </Link>
          </div>
          <div className="trust-row">
            <span>{t(language, "ruleBasedMatching")}</span>
            <span>{t(language, "officialSources")}</span>
            <span>{t(language, "supportedLanguages")}</span>
          </div>
        </div>
        <div className="hero-visual" aria-hidden="true">
          <div className="visual-card main-card">
            <span className="visual-label">SchemeSathi</span>
            <strong>{t(language, "profileMatching")}</strong>
            <div className="visual-status">{t(language, "noOfficialDecision")}</div>
            <div className="visual-lines"><i /><i /><i /></div>
          </div>
          <div className="visual-card mini-card">
            <span>{t(language, "guidance")}</span>
            <strong>{t(language, "checkOfficialSources")}</strong>
          </div>
        </div>
      </section>
      <section className="feature-grid">
        <article><span>01</span><h2>{t(language, "simpleProfile")}</h2><p>{t(language, "profileOnlyNeeded")}</p></article>
        <article><span>02</span><h2>{t(language, "clearReasons")}</h2><p>{t(language, "seeConditions")}</p></article>
        <article><span>03</span><h2>{t(language, "officialGuidance")}</h2><p>{t(language, "documentsAndLinks")}</p></article>
      </section>
    </main>
  )
}
