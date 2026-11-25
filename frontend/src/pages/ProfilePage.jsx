import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import { matchSchemes } from "../services/api"
import { useApp } from "../context/AppContext"

const initial = {
  state: "",
  age: "",
  occupation: "",
  education_level: "",
  annual_family_income: ""
}

export default function ProfilePage() {
  const { language, setProfile, setMatches } = useApp()
  const [form, setForm] = useState(initial)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const navigate = useNavigate()
  const telugu = language === "te"

  function update(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function submit(event) {
    event.preventDefault()
    setLoading(true)
    setError("")
    const payload = {
      state: form.state || null,
      age: form.age ? Number(form.age) : null,
      occupation: form.occupation || null,
      education_level: form.education_level || null,
      annual_family_income: form.annual_family_income ? Number(form.annual_family_income) : null
    }
    try {
      const response = await matchSchemes(payload)
      setProfile(payload)
      setMatches(response.data)
      navigate("/schemes")
    } catch (requestError) {
      setError(requestError.response?.data?.detail?.[0]?.msg || "Unable to find matches. Please check the form.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page narrow-page">
      <div className="page-heading">
        <span className="eyebrow">{telugu ? "దశ 1" : "Step 1"}</span>
        <h1>{telugu ? "మీ ప్రొఫైల్" : "Tell us about yourself"}</h1>
        <p>{telugu ? "కేవలం అవసరమైన వివరాలను పూరించండి." : "Provide only the information needed to check potentially relevant schemes."}</p>
      </div>
      <form className="profile-form" onSubmit={submit}>
        <div className="form-grid">
          <label>{telugu ? "రాష్ట్రం" : "State"}
            <input name="state" value={form.state} onChange={update} placeholder="e.g. Telangana" />
          </label>
          <label>{telugu ? "వయస్సు" : "Age"}
            <input name="age" type="number" min="0" max="120" value={form.age} onChange={update} placeholder="e.g. 24" />
          </label>
          <label>{telugu ? "ఉద్యోగం" : "Occupation"}
            <input name="occupation" value={form.occupation} onChange={update} placeholder="e.g. Farmer / Student" />
          </label>
          <label>{telugu ? "విద్య స్థాయి" : "Education"}
            <input name="education_level" value={form.education_level} onChange={update} placeholder="e.g. Graduate" />
          </label>
          <label>{telugu ? "వార్షిక కుటుంబ ఆదాయం" : "Annual family income"}
            <input name="annual_family_income" type="number" min="0" value={form.annual_family_income} onChange={update} placeholder="₹" />
          </label>
        </div>
        {error && <p className="form-error">{error}</p>}
        <button className="button primary form-submit" type="submit" disabled={loading}>
          {loading ? "Checking…" : telugu ? "పథకాలను కనుగొనండి" : "Find my schemes"}
        </button>
      </form>
    </main>
  )
}
