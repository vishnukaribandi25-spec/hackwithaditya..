import React from "react"
import { Link } from "react-router-dom"
import { useApp } from "../context/AppContext"
import { t } from "../i18n"

export default function Header() {
  const { language, setLanguage } = useApp()
  return (
    <header className="header">
      <Link className="brand" to="/" aria-label={t(language, "homeAria")}>
        <span className="brand-mark">SS</span>
        <span>
          <strong>SchemeSathi</strong>
          <small>{t(language, "schemeGuide")}</small>
        </span>
      </Link>
      <nav className="header-actions">
        <Link className="nav-link" to="/profile">{t(language, "profile")}</Link>
        <Link className="nav-link" to="/catalog">{t(language, "verifiedSchemes")}</Link>
        <button
          className="language-button"
          type="button"
          onClick={() => setLanguage(language === "en" ? "te" : "en")}
          aria-label={t(language, "changeLanguage")}
        >
          {t(language, "switchLanguageLabel")}
        </button>
      </nav>
    </header>
  )
}
