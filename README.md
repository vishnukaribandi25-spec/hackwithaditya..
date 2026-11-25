# SchemeSathi

SchemeSathi is a full-stack, multilingual government scheme discovery and eligibility guidance prototype. The backend provides health, scheme data, profile validation, deterministic eligibility, and optional AI explanations.

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
The current catalog contains only mock records, so it will not call Gemini until
officially sourced scheme records are added and verified.

### Frontend

```powershell
cd C:\Users\VISHNU\Downloads\adityahack\schemesathi\frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

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

The current scheme catalog contains clearly marked mock development records. Their source and application URLs are `null`; do not use them as real government guidance.

The profile validation endpoint keeps profile data in request memory only and rejects unknown fields and sensitive additional-attribute keys.

## Eligibility evaluation

The Python engine evaluates each scheme's structured `eligibility_rules`. It supports `state`, `age`, `annual_family_income`, `occupation`, `education_level`, `gender`, and explicit `attribute` rules against `additional_attributes`. Numeric minimum and maximum bounds are inclusive. Age or income rules with inverted bounds need verification instead of being treated as passed.

Each result separates passed rules (`matched_conditions`), failed rules (`failed_conditions`), and rules that cannot be checked (`missing_information`). Any failed rule makes the status `not_eligible`; otherwise missing or unsupported rules make it `needs_verification`; only all-passed rules make it `potentially_eligible`. No rules also means `needs_verification`. The engine does not use Gemini.

`POST /api/eligibility/check` returns separate `potentially_eligible`, `not_eligible`, and `needs_verification` arrays. Every result includes matched/failed/missing conditions and source metadata. An empty scheme catalog returns these three empty arrays.

Sample request:

```json
{
  "state": "Telangana",
  "education_level": "graduate"
}
```

Sample response (current development catalog):

```json
{
  "potentially_eligible": [
    {
      "scheme_id": "mock-education-support",
      "scheme_name": "MOCK DEVELOPMENT RECORD - Education Support",
      "status": "potentially_eligible",
      "matched_conditions": [
        "State matches an allowed value.",
        "Education level matches an allowed value."
      ],
      "failed_conditions": [],
      "missing_information": [],
      "explanation_reasons": [
        "State matches an allowed value.",
        "Education level matches an allowed value."
      ],
      "source_metadata": {
        "source_url": null,
        "application_url": null,
        "last_verified": null,
        "verification_status": "mock"
      }
    }
  ],
  "not_eligible": [
    {
      "scheme_id": "mock-agriculture-support",
      "scheme_name": "MOCK DEVELOPMENT RECORD - Agriculture Support",
      "status": "not_eligible",
      "matched_conditions": [],
      "failed_conditions": [
        "State does not match any allowed value."
      ],
      "missing_information": [
        "Occupation is not provided, so this rule could not be checked."
      ],
      "explanation_reasons": [
        "State does not match any allowed value.",
        "Occupation is not provided, so this rule could not be checked."
      ],
      "source_metadata": {
        "source_url": null,
        "application_url": null,
        "last_verified": null,
        "verification_status": "mock"
      }
    }
  ],
  "needs_verification": [],
  "disclaimer": "Eligibility results are informational, not official decisions or approval. Mock development records are not government schemes."
}
```

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

## Privacy and guidance

The current scheme catalog is mock development data; real scheme information must be verified against official government sources before use.
