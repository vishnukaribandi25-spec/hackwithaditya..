import React, { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import SchemeCard from "../components/SchemeCard"
import { listSchemes } from "../services/api"
import { useApp } from "../context/AppContext"

export default function ResultsPage() {
  const { language, matches } = useApp()
  const [schemes, setSchemes] = useState([])
  const telugu = language === "te"
  useEffect(() => {
    if (!matches.matches) {
      listSchemes().then((response) => setSchemes(response.data)).catch(() => setSchemes([]))
    }
  }, [matches])
  return (
    <main className="page">
      <div className="results-heading">
        <div>
          <span className="eyebrow">{telugu ? "మీ పథక ఫలితాలు" : "Your scheme results"}</span>
          <h1>{telugu ? "సంభావ్య సరిపోలికలు" : "Potential matches"}</h1>
        </div>
        <Link className="button secondary" to="/profile">{telugu ? "ప్రొఫైల్ మార్చండి" : "Edit profile"}</Link>
      </div>
      {!matches.matches ? (
        <>
          {schemes.length === 0 ? (
            <div className="empty-state"><p>Loading schemes…</p></div>
          ) : (
            <div className="results-grid">
              {schemes.map((scheme) => (
                <SchemeCard
                  key={scheme.id}
                  match={{
                    scheme,
                    status: "needs_verification",
                    explanation: telugu
                      ? "పరిశీలించడానికి మీ ప్రొఫైల్ పూర్తి చేయండి."
                      : "Complete your profile to verify this match."
                  }}
                />
              ))}
            </div>
          )}
        </>
      ) : (
        <>
          <p className="disclaimer">{matches.disclaimer}</p>
          <div className="results-grid">
            {matches.matches.map((match) => <SchemeCard key={match.scheme.id} match={match} />)}
          </div>
        </>
      )}
    </main>
  )
}
