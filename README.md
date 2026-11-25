# SchemeSathi

SchemeSathi is a full-stack, multilingual government scheme discovery and eligibility guidance prototype. The backend provides health, scheme data, profile validation, deterministic eligibility, and optional AI explanations. It is an independent informational project and is not affiliated with any government.

## Stack

- Frontend: React, Vite, Tailwind CSS, React Router, Axios
- Backend: Python, FastAPI, Pydantic
- AI: Google Gen AI Python SDK for optional English/Telugu explanations
- Data: JSON

## Run locally

### Backend

```powershell
cd C:\Users\VISHNU\Downloads\adityahack\schemesathi\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uvicorn app.main:app --reload --port 8000 --env-file .env
```

The API listens at `http://127.0.0.1:8000`. Health check: `http://127.0.0.1:8000/api/health`.
Interactive API documentation: `http://127.0.0.1:8000/docs`.

### Configure Gemini (optional)

The eligibility API works without Gemini; when the key is absent or the AI service
fails, deterministic eligibility results are returned without an AI explanation.
To enable explanations, edit `backend\.env`. If it does not exist yet, open
PowerShell in the backend folder and create it from the example first:

```powershell
Copy-Item .env.example .env
notepad .env
```

If `.env` already exists, do not overwrite it; just open it and add/update:

```env
GEMINI_API_KEY=your_google_genai_api_key
GEMINI_MODEL=gemini-flash-latest
```

Keep the key only in `backend\.env`; it is ignored by Git. Never put it in source
code or commit it. Start/restart the backend with `--env-file .env` to load it.
`POST /api/eligibility/check?language=en` (or `language=te`) returns optional
`ai_explanation` text only for schemes marked verified and containing source
metadata. Gemini explains the deterministic result and cannot alter its status.
The catalog now includes six records sourced from official government portals;
individual unavailable fields are identified in the returned `unavailable_fields`.

### Frontend

```powershell
cd C:\Users\VISHNU\Downloads\adityahack\schemesathi\frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

The frontend uses the same-origin `/api` path by default. Vite proxies it to
`http://127.0.0.1:8000`, which also lets a browser opened through a frontend
devtunnel reach the local backend without making the browser call its own
`localhost`. Set `API_PROXY_TARGET` when the backend listens elsewhere during
development. For a separately hosted backend, set `VITE_API_URL` to a
browser-reachable API base URL; do not use a private `localhost` URL for
remote users.

## Test

```powershell
cd C:\Users\VISHNU\Downloads\adityahack\schemesathi\backend
.\venv\Scripts\python.exe -m pytest -q
```

## API

- `GET /api/health`
- `GET /api/schemes?state=Telangana&category=education`
- `GET /api/schemes/{scheme_id}`
- `POST /api/profile/validate`
- `POST /api/eligibility/match`
- `POST /api/eligibility/check`
- `POST /api/chat`

The scheme catalog contains six official-source records and two clearly labelled mock development records. Mock records have `null` source and application URLs; do not use them as real government guidance. A `state` of `All India` may include `state_exclusions` where a central programme is not implemented.

The profile validation endpoint keeps profile data in request memory only and rejects unknown fields and sensitive additional-attribute keys.

`POST /api/eligibility/match` returns a `matches` list for relevant verified
schemes and a separate `not_applicable` list for verified records that fail a
known rule or have no supported profile match. The latter is not an official
finding of ineligibility. Mock and unverified records never appear in either
list. Each result includes `scheme_name`, `status`, matched/failed/missing
conditions, `verification_required`, source/date metadata, `is_mock`, and
official verification steps. `POST /api/eligibility/check` returns all
deterministic status groups and keeps `mock_records` and `unverified_records`
separate. Gemini only adds optional explanations in that endpoint.

The profile form retains the submitted profile while navigating between results
and scheme details. Optional `social_category` values are `General`, `SC`, `ST`,
`OBC`, `Other`, and `Prefer not to say`. Category is used only when a scheme has
an explicit category rule. Missing or declined category information remains
unknown and never defaults to General.

The profile boundary trims and normalizes known state, occupation, education,
and category aliases. For example, `telangana`/`Telangana` and `farmer`/`Farmer`
are matched consistently, and `highschool`, `high_school`, and `High School`
normalize to `secondary`. Unknown values are preserved rather than converted to
a supported category. The eligibility endpoint accepts the profile form's
canonical additional-attribute keys and the known aliases `residence_type`,
`owns_pucca_house`, and `landholding_farmer_family`; boolean conditions must be
JSON booleans. Conflicting aliases and invalid values return field-specific
validation errors.

The form also exposes optional PMAY-G and PM-KISAN profile attributes only when
relevant: rural residence, household pucca-house ownership, and self-reported
landholding farmer-family status. These are sent under `additional_attributes`.
The landholding answer is self-reported, not proof of land ownership or
beneficiary status. SchemeSathi does not check land records, official beneficiary
records, government exclusions, or e-KYC status.

The `/schemes` route is personalized and never falls back to the full catalogue.
Use `/catalog` to browse source-backed verified scheme information; mock and
unverified records are filtered out there.

### Multilingual chat

`POST /api/chat` accepts an English or Telugu message and an optional validated
profile. It classifies scheme-finding, eligibility, benefits, documents,
application-process, and general scheme questions. Only records marked verified
with a source URL and verification date are used. Eligibility questions always
go through the deterministic Python engine; unknown or incomplete criteria
produce `needs_verification`, and Gemini is not used to calculate or rewrite
eligibility status. Application instructions are taken only from each scheme's
`application_process` data; otherwise the response states that they are unavailable.

Sample request:

```json
{
  "message": "What documents are required for NTR Bharosa Pension Scheme?",
  "language": "en",
  "profile": {
    "state": "Telangana",
    "age": 24
  }
}
```

When a named scheme is not found in the verified catalog, the response says so
instead of substituting an unrelated record. When a requested field is not
verified, it is listed in `missing_information`; for the example above, the
NTR Bharosa record explicitly reports that its document checklist is unavailable.

## Eligibility evaluation

The Python engine evaluates each scheme's structured `eligibility_rules`. It supports `state`, `age`, `annual_family_income`, `occupation`, `education_level`, `gender`, `social_category`, and explicit `attribute` rules against `additional_attributes`. Numeric minimum and maximum bounds are inclusive. Age or income rules with inverted bounds need verification instead of being treated as passed.

Each result separates passed rules (`matched_conditions`), failed rules (`failed_conditions`), and rules that cannot be checked (`missing_information`). Any failed rule makes the status `not_eligible`; otherwise missing or unsupported rules make it `needs_verification`; only all-passed rules make it `potentially_eligible`. No rules also means `needs_verification`. The engine does not use Gemini.

`POST /api/eligibility/check` returns separate `potentially_eligible`, `not_eligible`, and `needs_verification` arrays, plus separate `mock_records` and `unverified_records`. Every result includes matched/failed/missing conditions and source metadata. An empty scheme catalog returns empty arrays. The state rule supports exclusions with `not_values`; for example, PMMVY is unavailable in Telangana and Odisha. Scheme-specific rules not fully represented by the profile model are explicitly left for verification.

Sample request:

```json
{
  "state": "Andhra Pradesh",
  "age": 48,
  "occupation": "Farmer",
  "education_level": "Primary",
  "annual_family_income": 150000,
  "social_category": "General"
}
```

`POST /api/eligibility/match` farmer request example:

```json
{
  "state": "Andhra Pradesh",
  "age": 48,
  "occupation": "Farmer",
  "education_level": "Primary",
  "annual_family_income": 150000,
  "social_category": "General",
  "additional_attributes": {
    "resides_in_rural_area": true,
    "household_owns_pucca_house": false,
    "pm_kisan_landholding_farmer_family": true
  }
}
```

For this profile, PM-KISAN and PMAY-G remain `needs_verification`. Mock records
are excluded from `matches` and `not_applicable`; those arrays contain only
source-backed verified records. The landholding answer is self-reported.
PM-KISAN remains `needs_verification` until land records, scheme exclusions,
and e-KYC are checked through official services. The result includes the
official portal steps and source date; it is not an approval or guarantee.

Rule examples (development-only, not official eligibility criteria):

```json
[
  {"type": "state", "values": ["Telangana"]},
  {"type": "age", "min": 18, "max": 60},
  {"type": "annual_family_income", "max": 300000},
  {"type": "occupation", "values": ["student"]},
  {"type": "education_level", "values": ["undergraduate"]},
  {"type": "attribute", "attribute": "first_generation_student", "operator": "equals", "value": true}
]
```

## Verified dataset sources

The six records below were checked against official government sources on
2026-11-25. Fields that those sources did not establish are represented as empty
lists or are named in `unavailable_fields`; they are not inferred.

| Scheme | Official source | Official application/information portal |
| --- | --- | --- |
| Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | [PM-KISAN portal](https://pmkisan.gov.in/homenew.aspx) | [pmkisan.gov.in](https://pmkisan.gov.in/) |
| Pradhan Mantri Awaas Yojana - Gramin (PMAY-G) | [Official eligibility questionnaire](https://pmayg.dord.gov.in/netiayHome/questions.html) | [PMAY-G citizen services](https://pmayg.dord.gov.in/netiayHome/home.aspx) |
| Pradhan Mantri Matru Vandana Yojana (PMMVY) | [Official PMMVY FAQ](https://pmmvy.wcd.gov.in/Home/FrequentlyAskedQuestions) | [pmmvy.wcd.gov.in](https://pmmvy.wcd.gov.in/) |
| PM-USP Central Sector Scheme of Scholarship for College and University Students (CSSS) | [National Scholarship Portal](https://scholarships.gov.in/) | [NSP One Time Registration](https://scholarships.gov.in/otrapplication/#/login-page) |
| NTR Bharosa Pension Scheme (Andhra Pradesh) | [Andhra Pradesh Social Security Pensions portal](https://sspensions.ap.gov.in/SSP) | [Andhra Pradesh Social Security Pensions portal](https://sspensions.ap.gov.in/SSP) |
| Telangana Rythu Bharosa | [Telangana government July 2026 release](https://www.telangana.gov.in/news/press-releases/2026/07/honble-cm-sri-a-revanth-reddy-participated-in-rythu-ashirvada-sabha-releases-rythu-bharosa-funds-to-farmers-issues-e-pattadar-passbooks-addresses-gathering-at-jagannadhapuram-chintakani/) | [Telangana Rythu Bharosa portal](https://rythubharosa.telangana.gov.in/) |

The Rythu Bharosa portal identifies farmers as its audience. A July 2026
Telangana government release states the assistance was increased to ₹12,000
per acre. The official portal does not publish detailed beneficiary criteria,
exclusions, a document checklist, or full application instructions. The scheme
is shown only as `needs_verification`; no land, income, or other threshold is
inferred.

The Telangana ePASS portal lists post-matric scholarship services and Kalyana
Lakshmi/Shaadi Mubarak, and the Telangana State Portal describes Maha Lakshmi.
The public pages reviewed did not establish the current complete eligibility
rules and application requirements for those programs, so they were not added
as recommendations. No current Telangana unemployment-allowance or pension
record with sufficiently detailed official eligibility rules was verified in
this audit; the Andhra Pradesh NTR Bharosa record is not applicable in
Telangana.

The official NTR Bharosa page showed inconsistent amounts for the fully disabled
category during verification; that amount is explicitly unavailable pending
confirmation. PM-KISAN's reviewed page did not state the benefit amount, and
CSSS's reviewed notice did not include its detailed eligibility rules or award
amount. Those records remain conservative: the eligibility engine returns
`needs_verification` unless a known condition already fails.

Some official scheme portals require sensitive information during application.
SchemeSathi does not collect Aadhaar, OTP, bank-account, or similar sensitive
details. Users should only submit information directly to the official portal
after independently confirming its requirements. Eligibility guidance is not an
official decision, approval, or guarantee of benefits.
