import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import { matchSchemes } from "../services/api"
import { useApp } from "../context/AppContext"
import { localizedError, t, validateProfileForm } from "../i18n"

const initial = {
  state: "",
  age: "",
  occupation: "",
  education_level: "",
  annual_family_income: "",
  social_category: "",
  residence: "",
  household_owns_pucca_house: "",
  pm_kisan_landholding_farmer_family: ""
}

export default function ProfilePage() {
  const { language, profile, setProfile, setMatches } = useApp()
  const [form, setForm] = useState(() => {
    const attributes = profile?.additional_attributes || {}
    const savedResidence = attributes.resides_in_rural_area === true
      ? "rural"
      : attributes.resides_in_rural_area === false
        ? "urban"
        : typeof attributes.residence_type === "string"
          ? attributes.residence_type.trim().toLowerCase()
          : ""
    const savedHouse = attributes.household_owns_pucca_house
      ?? attributes.owns_pucca_house
    const savedLandholding = attributes.pm_kisan_landholding_farmer_family
      ?? attributes.landholding_farmer_family
    return {
      ...initial,
      state: profile?.state || "",
      age: profile?.age == null ? "" : String(profile.age),
      occupation: profile?.occupation || "",
      education_level: profile?.education_level || "",
      annual_family_income: profile?.annual_family_income == null
        ? ""
        : String(profile.annual_family_income),
      social_category: profile?.social_category || "",
      residence: savedResidence,
      household_owns_pucca_house: savedHouse === true
        ? "yes"
        : savedHouse === false
          ? "no"
          : "",
      pm_kisan_landholding_farmer_family: savedLandholding === true
        ? "yes"
        : savedLandholding === false
          ? "no"
          : ""
    }
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  function update(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
    setMatches(null)
    setError(null)
  }

  async function submit(event) {
    event.preventDefault()
    const additionalAttributes = { ...(profile?.additional_attributes || {}) }
    delete additionalAttributes.resides_in_rural_area
    delete additionalAttributes.household_owns_pucca_house
    delete additionalAttributes.pm_kisan_landholding_farmer_family
    delete additionalAttributes.residence_type
    delete additionalAttributes.owns_pucca_house
    delete additionalAttributes.landholding_farmer_family

    if (form.residence) {
      additionalAttributes.resides_in_rural_area = form.residence === "rural"
    }
    if (form.residence === "rural" && form.household_owns_pucca_house) {
      additionalAttributes.household_owns_pucca_house =
        form.household_owns_pucca_house === "yes"
    }
    if (
      form.occupation.trim().replace(/\s+/g, " ").toLowerCase() === "farmer"
      && form.pm_kisan_landholding_farmer_family
    ) {
      additionalAttributes.pm_kisan_landholding_farmer_family =
        form.pm_kisan_landholding_farmer_family === "yes"
    }

    const payload = {
      state: form.state.trim() || null,
      age: form.age ? Number(form.age) : null,
      occupation: form.occupation.trim() || null,
      education_level: form.education_level.trim() || null,
      annual_family_income: form.annual_family_income ? Number(form.annual_family_income) : null,
      social_category: form.social_category || null,
      additional_attributes: additionalAttributes
    }

    setMatches(null)
    setError(null)
    const validationError = validateProfileForm(payload)
    if (validationError) {
      setError(validationError)
      return
    }

    setLoading(true)
    setProfile(payload)
    try {
      const response = await matchSchemes(payload)
      setMatches(response.data)
      navigate("/schemes")
    } catch (requestError) {
      setError(requestError)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page narrow-page">
      <div className="page-heading">
        <span className="eyebrow">{t(language, "stepOne")}</span>
        <h1>{t(language, "profileTitle")}</h1>
        <p>{t(language, "profileIntro")}</p>
      </div>
      <form className="profile-form" onSubmit={submit} noValidate>
        <div className="form-grid">
          <label>{t(language, "state")}
            <input name="state" value={form.state} onChange={update} placeholder={t(language, "statePlaceholder")} disabled={loading} />
          </label>
          <label>{t(language, "age")}
            <input name="age" type="number" min="0" max="120" step="1" value={form.age} onChange={update} placeholder={t(language, "agePlaceholder")} disabled={loading} />
          </label>
          <label>{t(language, "occupation")}
            <input name="occupation" value={form.occupation} onChange={update} placeholder={t(language, "occupationPlaceholder")} disabled={loading} />
          </label>
          <label>{t(language, "education")}
            <input name="education_level" value={form.education_level} onChange={update} placeholder={t(language, "educationPlaceholder")} disabled={loading} />
          </label>
          <label>{t(language, "annualIncome")}
            <input name="annual_family_income" type="number" min="0" step="1" value={form.annual_family_income} onChange={update} placeholder="₹" disabled={loading} />
          </label>
          <label>
            {t(language, "socialCategory")}
            <select name="social_category" value={form.social_category} onChange={update} disabled={loading}>
              <option value="">{t(language, "notProvided")}</option>
              <option value="General">{t(language, "general")}</option>
              <option value="SC">SC</option>
              <option value="ST">ST</option>
              <option value="OBC">OBC</option>
              <option value="Other">{t(language, "otherCategory")}</option>
              <option value="Prefer not to say">{t(language, "preferNotToSay")}</option>
            </select>
            <small>{t(language, "socialCategoryHint")}</small>
          </label>
          <label>
            {t(language, "residence")}
            <select name="residence" value={form.residence} onChange={update} disabled={loading}>
                <option value="">{t(language, "unknownNotProvided")}</option>
                <option value="rural">{t(language, "rural")}</option>
                <option value="urban">{t(language, "urban")}</option>
            </select>
            <small>{t(language, "residenceHint")}</small>
          </label>
          {form.residence === "rural" && (
            <label>
                {t(language, "puccaHouseQuestion")}
                <select
                  name="household_owns_pucca_house"
                  value={form.household_owns_pucca_house}
                  onChange={update}
                  disabled={loading}
                >
                  <option value="">{t(language, "unknownNotProvided")}</option>
                  <option value="yes">{t(language, "yes")}</option>
                  <option value="no">{t(language, "no")}</option>
                </select>
                <small>{t(language, "selfReportedHouse")}</small>
            </label>
          )}
          {form.occupation.trim().replace(/\s+/g, " ").toLowerCase() === "farmer" && (
            <label>
                {t(language, "landholdingQuestion")}
                <select
                  name="pm_kisan_landholding_farmer_family"
                  value={form.pm_kisan_landholding_farmer_family}
                  onChange={update}
                  disabled={loading}
                >
                  <option value="">{t(language, "unknownNotProvided")}</option>
                  <option value="yes">{t(language, "yes")}</option>
                  <option value="no">{t(language, "no")}</option>
                </select>
                <small>{t(language, "selfReportedLand")}</small>
            </label>
          )}
        </div>
        {error && <p className="form-error">{localizedError(error, language)}</p>}
        <button className="button primary form-submit" type="submit" disabled={loading}>
          {loading ? t(language, "checking") : t(language, "findSchemes")}
        </button>
      </form>
    </main>
  )
}
