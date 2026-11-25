import React from "react"
import { Link } from "react-router-dom"
import { useApp } from "../context/AppContext"

export default function Header() {
  const { language, setLanguage } = useApp()
  return (
    <header className="header">
      <Link className="brand" to="/" aria-label="SchemeSathi home">
        <span className="brand-mark">SS</span>
        <span>
          <strong>SchemeSathi</strong>
          <small>{language === "te" ? "పథక సహాయకుడు" : "Scheme Guide"}</small>
        </span>
      </Link>
      <nav className="header-actions">
        <Link className="nav-link" to="/profile">{language === "te" ? "ప్రొఫైల్" : "Profile"}</Link>
        <Link className="nav-link" to="/schemes">{language === "te" ? "పథకాలు" : "Schemes"}</Link>
        <button
          className="language-button"
          type="button"
          onClick={() => setLanguage(language === "en" ? "te" : "en")}
          aria-label="Change language"
        >
          {language === "en" ? "తెలుగు" : "English"}
        </button>
      </nav>
    </header>
  )
}
