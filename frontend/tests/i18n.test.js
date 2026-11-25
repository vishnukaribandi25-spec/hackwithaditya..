import assert from "node:assert/strict"
import test from "node:test"

import {
  describeRule,
  localizeEligibilityText,
  localizedError,
  localizedScheme,
  t,
  validateProfileForm
} from "../src/i18n.js"

test("profile form validation identifies invalid age and income fields", () => {
  assert.deepEqual(validateProfileForm({ age: 121 }), {
    kind: "profile_validation",
    field: "age",
    messageKey: "invalidAge"
  })
  assert.deepEqual(validateProfileForm({ annual_family_income: 1.5 }), {
    kind: "profile_validation",
    field: "annual_family_income",
    messageKey: "invalidIncome"
  })
  assert.equal(validateProfileForm({ age: 50, annual_family_income: 0 }), null)
})

test("API validation errors show the field and localized reason", () => {
  const error = {
    response: {
      status: 422,
      data: {
        detail: [{
          loc: ["body", "age"],
          msg: "Input should be less than or equal to 120"
        }]
      }
    }
  }

  assert.equal(
    localizedError(error, "te"),
    "వయస్సు: 120 కంటే ఎక్కువ ఉండకూడదు."
  )
})

test("HTTP and network failures have distinct Telugu messages", () => {
  assert.match(
    localizedError({ response: { status: 500 } }, "te"),
    /HTTP 500/
  )
  assert.match(localizedError(new Error("offline"), "te"), /కనెక్ట్ కాలేదు/)
})

test("multi-sentence farmer result explanations are localized", () => {
  const explanation = [
    "Applicant is a farmer matches an allowed value.",
    "Applicant belongs to a landholding farmer family matches the stated scheme-specific condition.",
    "Any landholding status provided is self-reported. SchemeSathi does not verify land records, official beneficiary records, or applicable exclusions; e-KYC status has not been checked. Confirm these through official PM-KISAN services."
  ].join(" ")
  const translated = localizeEligibilityText(explanation, "te")

  assert.match(translated, /దరఖాస్తుదారు రైతు/)
  assert.match(translated, /భూమి కలిగిన రైతు కుటుంబానికి/)
  assert.match(translated, /భూ రికార్డులు/)
  assert.doesNotMatch(translated, /Applicant is|Land records/)
})

test("scheme details localize content and retain official identifiers", () => {
  const scheme = localizedScheme({
    id: "pm-kisan-samman-nidhi",
    name: "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
    description: "English description",
    benefits: [],
    eligibility_rules: [],
    required_documents: [],
    application_process: []
  }, "te")

  assert.match(scheme.name_te, /PM-KISAN/)
  assert.match(scheme.description_te, /రైతు/)
  assert.equal(scheme.application_process_te.length, 2)
})

test("every verified scheme record has a Telugu name and description", () => {
  const verifiedIds = [
    "pm-kisan-samman-nidhi",
    "pmay-gramin",
    "pradhan-mantri-matru-vandana-yojana",
    "pm-usp-csss",
    "ntr-bharosa-pension",
    "telangana-rythu-bharosa"
  ]

  for (const id of verifiedIds) {
    const scheme = localizedScheme({
      id,
      name: "English scheme name",
      description: "English scheme description",
      department: "English department",
      benefits: [],
      eligibility_rules: [],
      required_documents: [],
      application_process: []
    }, "te")
    assert.notEqual(scheme.name_te, "English scheme name", `${id} name`)
    assert.notEqual(scheme.description_te, "English scheme description", `${id} description`)
  }
})

test("Rythu Bharosa eligibility verification text is available in Telugu", () => {
  const text = localizeEligibilityText(
    "The official Telangana Rythu Bharosa portal does not publish detailed beneficiary eligibility, exclusions, required documents, or complete application instructions. Verify current beneficiary criteria with the Department of Agriculture before applying.",
    "te"
  )

  assert.match(text, /లబ్ధిదారుల అర్హతలు/)
  assert.match(text, /వ్యవసాయ శాఖతో ధృవీకరించండి/)
  assert.doesNotMatch(text, /public overview|Department of Agriculture/)
})

test("Rythu Bharosa scheme details translate the verified amount and incomplete criteria", () => {
  const scheme = localizedScheme({
    id: "telangana-rythu-bharosa",
    name: "Telangana Rythu Bharosa",
    department: "Department of Agriculture",
    description: "English description",
    benefits: ["English benefit"],
    eligibility_summary: "English eligibility summary",
    required_documents: [],
    application_process: []
  }, "te")

  assert.match(scheme.benefits_te[0], /₹12,000/)
  assert.match(scheme.eligibility_summary_te, /అర్హత/)
})

test("manual-verification rules with null numeric fields show their Telugu explanation", () => {
  const description = describeRule({
    type: "manual_verification",
    label: "Any landholding status provided is self-reported. SchemeSathi does not verify land records, official beneficiary records, or applicable exclusions; e-KYC status has not been checked. Confirm these through official PM-KISAN services.",
    min: null,
    max: null,
    values: null,
    not_values: null,
    attribute: null
  }, "te")

  assert.match(description, /భూ రికార్డులు/)
  assert.doesNotMatch(description, /కనిష్ఠ పరిమితి లేదు/)
})

test("shared labels come from the selected language catalog", () => {
  assert.equal(t("te", "verificationRequired"), "ధృవీకరణ అవసరం")
  assert.equal(t("en", "verificationRequired"), "Verification Required")
})
