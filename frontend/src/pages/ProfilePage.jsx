import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import { matchSchemes } from "../services/api"
import { useApp } from "../context/AppContext"

const initial = {
  state: "",
  age: "",
  occupation: "",
  education: "",
  annual_family_income: "",
  gender: "",
  category: "",
  is_farmer: "",
  is_student: "",
  is_unemployed: ""
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
      state: form.state,
      age: form.age ? Number(form.age) : null,
      occupation: form.occupation || null,
      education: form.education || null,
      annual_family_income: form.annual_family_income ? Number(form.annual_family_income) : null,
      gender: form.gender || null,
      category: form.category || null,
      is_farmer: form.is_farmer === "" ? null : form.is_farmer === "yes",
      is_student: form.is_student === "" ? null : form.is_student === "yes",
      is_unemployed: form.is_unemployed === "" ? null : form.is_unemployed === "yes"
    }
    try {
      const response = await matchSchemes(payload, language)
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
          <label>{telugu ? "రాష్ట్రం" : "State"} *
            <input name="state" value={form.state} onChange={update} placeholder="e.g. Telangana" required />
          </label>
          <label>{telugu ? "వయస్సు" : "Age"}
            <input name="age" type="number" min="0" max="120" value={form.age} onChange={update} placeholder="e.g. 24" />
          </label>
          <label>{telugu ? "ఉద్యోగం" : "Occupation"}
            <input name="occupation" value={form.occupation} onChange={update} placeholder="e.g. Farmer / Student" />
          </label>
          <label>{telugu ? "విద్య స్థాయి" : "Education"}
            <input name="education" value={form.education} onChange={update} placeholder="e.g. Graduate" />
          </label>
          <label>{telugu ? "వార్షిక కుటుంబ ఆదాయం" : "Annual family income"}
            <input name="annual_family_income" type="number" min="0" value={form.annual_family_income} onChange={update} placeholder="₹" />
          </label>
          <label>{telugu ? "లింగం" : "Gender"}
            <select name="gender" value={form.gender} onChange={update}>
              <option value="">Prefer not to say</option><option value="male">Male</option><option value="female">Female</option><option value="other">Other</option>
            </select>
          </label>
          <label>{telugu ? "వర్గం" : "Category"}
            <select name="category" value={form.category} onChange={update}>
              <option value="">Not provided</option><option value="general">General</option><option value="obc">OBC</option><option value="sc">SC</option><option value="st">ST</option><option value="ews">EWS</option>
            </select>
          </label>
          <label>{telugu ? "మీరు రైతు?" : "Are you a farmer?"}
            <select name="is_farmer" value={form.is_farmer} onChange={update}><option value="">Not sure</option><option value="yes">Yes</option><option value="no">No</option></select>
          </label>
          <label>{telugu ? "మీరు విద్యార్థి?" : "Are you a student?"}
            <select name="is_student" value={form.is_student} onChange={update}><option value="">Not sure</option><option value="yes">Yes</option><option value="no">No</option></select>
          </label>
          <label>{telugu ? "మీరు నిరుద్యోగి?" : "Are you unemployed?"}
            <select name="is_unemployed" value={form.is_unemployed} onChange={update}><option value="">Not sure</option><option value="yes">Yes</option><option value="no">No</option></select>
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
