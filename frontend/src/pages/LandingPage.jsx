import React from "react"
import { Link } from "react-router-dom"
import { useApp } from "../context/AppContext"

export default function LandingPage() {
  const { language } = useApp()
  const telugu = language === "te"
  return (
    <main>
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">{telugu ? "ప్రభుత్వ పథక మార్గదర్శి" : "Government scheme guide"}</span>
          <h1>{telugu ? "మీకు సరైన పథకాన్ని కనుగొనండి" : "Find schemes that may fit your life"}</h1>
          <p>
            {telugu
              ? "మీ ప్రొఫైల్ ఆధారంగా పథకాలను కనుగొని, पात्रత కారణాలు మరియు అవసరమైన పత్రాలను స్పష్టంగా చూడండి."
              : "Discover relevant government schemes, understand why they match and prepare with a clear document checklist."}
          </p>
          <div className="hero-actions">
            <Link className="button primary" to="/profile">
              {telugu ? "ప్రొఫైల్ ప్రారంభించండి" : "Check my schemes"}
            </Link>
            <Link className="button text" to="/schemes">
              {telugu ? "పథకాలను చూడండి" : "Browse schemes"}
            </Link>
          </div>
          <div className="trust-row">
            <span>✓ Rule-based matching</span>
            <span>✓ Official sources</span>
            <span>✓ Telugu & English</span>
          </div>
        </div>
        <div className="hero-visual" aria-hidden="true">
          <div className="visual-card main-card">
            <span className="visual-label">Top match</span>
            <strong>PM-KISAN</strong>
            <div className="visual-status">Potentially eligible</div>
            <div className="visual-lines"><i /><i /><i /></div>
          </div>
          <div className="visual-card mini-card">
            <span>Documents</span>
            <strong>4 items ready</strong>
          </div>
        </div>
      </section>
      <section className="feature-grid">
        <article><span>01</span><h2>{telugu ? "సరళమైన ప్రొఫైల్" : "Simple profile"}</h2><p>{telugu ? "అవసరమైన వివరాలు మాత్రమే." : "Share only the details needed for matching."}</p></article>
        <article><span>02</span><h2>{telugu ? "స్పష్టమైన ఫలితం" : "Clear reasons"}</h2><p>{telugu ? "ప్రతి పథకం ఎందుకు సరిపోతుందో తెలుసుకోండి." : "See exactly which conditions match."}</p></article>
        <article><span>03</span><h2>{telugu ? "అధికారిక మార్గం" : "Official guidance"}</h2><p>{telugu ? "పత్రాలు మరియు దరఖాస్తు లింకులు." : "Documents and official application steps."}</p></article>
      </section>
    </main>
  )
}
