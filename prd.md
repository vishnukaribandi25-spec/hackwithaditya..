# SchemeSathi
## Product Requirements Document (PRD)

**Version:** 1.0  
**Product type:** AI-powered multilingual government scheme discovery and application guidance platform  
**Hackathon track:** AI for Bharat  
**Backend:** Python + FastAPI  
**Frontend:** React + Vite  
**Primary users:** Indian citizens who struggle to discover government schemes and understand their eligibility or application process.

---

## 1. Problem Statement

India has multiple central and state government welfare schemes. However, many citizens struggle to:

- Discover schemes relevant to their circumstances.
- Understand eligibility requirements written in complex language.
- Identify the documents required to apply.
- Find the correct official application portal.
- Access this information in their preferred language.

Existing information is often distributed across different government websites and portals.

**Problem:** Citizens need a simple, multilingual platform that helps them discover potentially relevant government schemes and understand how to apply.

## 2. Proposed Solution

SchemeSathi is a multilingual, AI-assisted government scheme discovery and application guidance platform.

Users can enter their personal circumstances through text or voice. The platform identifies potentially relevant schemes using structured eligibility rules and explains:

1. Why a scheme may be relevant.
2. Which eligibility conditions are satisfied.
3. Which conditions are not satisfied or still need verification.
4. What documents are required.
5. Where and how to apply through official channels.

The platform provides guidance, not government approval or guaranteed eligibility.

## 3. Target Users

- Students looking for scholarships.
- Farmers looking for agricultural assistance.
- Women looking for applicable welfare schemes.
- Unemployed individuals looking for relevant support.
- Low-income households looking for government benefits.
- Citizens who prefer interacting in their regional language.

## 4. Product Goals

### Primary goals

- Make government scheme discovery easier.
- Provide transparent eligibility matching.
- Explain scheme information in simple language.
- Provide personalized document checklists.
- Support Telugu and English initially, with Hindi as an additional target if time permits.
- Support optional voice-based interaction.

### Success criteria for the prototype

- A user can complete a profile and receive scheme matches.
- The matching engine can explain why each result matched.
- Each displayed scheme has a source and a last-verified date.
- Users can view document requirements and an official application link.
- The main workflow works without voice or an AI API being available.

## 5. Core Features and Priority

### P0 — Must have

**A. User profile**

Collect only the information needed for scheme matching:

- State
- Age or age range
- Occupation
- Education level, when relevant
- Annual family income, when relevant
- Other scheme-specific conditions, only when necessary

Do not collect Aadhaar numbers, bank account details, OTPs, or unnecessary sensitive information.

**B. Scheme discovery**

Display schemes based on the user's profile.

Each scheme card should show:

- Scheme name
- Department or issuing authority
- Short description
- Benefits
- Eligibility summary
- Potential match status
- Official source
- Last verified date

**C. Eligibility matching engine**

Use Python rules to compare the user profile against structured scheme conditions.

Possible statuses:

- Potentially eligible
- Not eligible based on known information
- Needs additional verification

Show the reasons behind every result.

**D. Document checklist**

Display documents required by the selected scheme.

**E. Official application guidance**

Provide the official application link and simple steps to apply.

### P1 — Important

**F. Multilingual interaction**

- Telugu
- English
- Hindi, if feasible

Users should be able to ask questions in their preferred supported language.

**G. AI-powered explanation**

Use an AI model to simplify verified scheme information and explain eligibility results. The model must not invent eligibility rules, benefits, documents, or application links.

### P2 — Optional enhancement

**H. Voice-to-voice interaction**

A turn-based voice workflow:

1. User speaks.
2. Speech is converted into text.
3. The system processes the request.
4. The response is generated in the selected language.
5. Text-to-speech reads the response aloud.

Text input and output must remain available as a fallback.

---

## 6. User Journey

1. User opens SchemeSathi.
2. User selects Telugu or English.
3. User enters profile information