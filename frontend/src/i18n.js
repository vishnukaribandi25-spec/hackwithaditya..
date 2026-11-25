const messages = {
  en: {
    documentTitle: "SchemeSathi - Government Scheme Guidance",
    homeAria: "SchemeSathi home",
    schemeGuide: "Scheme Guide",
    profile: "Profile",
    verifiedSchemes: "Verified schemes",
    changeLanguage: "Change language",
    switchLanguageLabel: "తెలుగు",
    heroEyebrow: "Government scheme guide",
    heroTitle: "Find schemes that may fit your life",
    heroDescription: "Discover relevant government schemes, understand why they match and prepare with a clear document checklist.",
    startProfile: "Check my schemes",
    browseVerified: "Browse verified schemes",
    ruleBasedMatching: "✓ Rule-based matching",
    officialSources: "✓ Official sources",
    supportedLanguages: "✓ Telugu & English",
    profileMatching: "Profile-based matching",
    noOfficialDecision: "Not an official decision",
    guidance: "Guidance",
    checkOfficialSources: "Check official sources",
    simpleProfile: "Simple profile",
    profileOnlyNeeded: "Share only the details needed for matching.",
    clearReasons: "Clear reasons",
    seeConditions: "See exactly which conditions match.",
    officialGuidance: "Official guidance",
    documentsAndLinks: "Documents and official application steps.",
    stepOne: "Step 1",
    profileTitle: "Tell us about yourself",
    profileIntro: "Provide only the information needed to check potentially relevant schemes.",
    state: "State",
    statePlaceholder: "e.g. Telangana",
    age: "Age",
    agePlaceholder: "e.g. 24",
    occupation: "Occupation",
    occupationPlaceholder: "e.g. Farmer / Student",
    education: "Education",
    educationPlaceholder: "e.g. Graduate",
    annualIncome: "Annual family income",
    socialCategory: "Social category (optional)",
    notProvided: "Not provided",
    general: "General",
    otherCategory: "Other",
    preferNotToSay: "Prefer not to say",
    socialCategoryHint: "Optional. Used only when a verified scheme rule requires it; it is never assumed.",
    residence: "Household residence",
    residenceHint: "Used only to check the verified rural-household rule.",
    unknownNotProvided: "Unknown / not provided",
    rural: "Rural",
    urban: "Urban",
    puccaHouseQuestion: "Does the household own a pucca house?",
    selfReportedHouse: "Self-reported only; SchemeSathi cannot verify household records.",
    landholdingQuestion: "Part of a landholding farmer family?",
    selfReportedLand: "Self-reported only; this does not verify land records or PM-KISAN eligibility.",
    invalidAge: "Enter a whole number from 0 to 120.",
    invalidIncome: "Enter a non-negative whole number.",
    invalidState: "Enter a state name using 2 to 100 characters.",
    invalidOccupation: "Enter an occupation using 1 to 100 characters.",
    invalidEducation: "Enter an education level using 1 to 100 characters.",
    invalidValue: "The value is invalid.",
    invalidInteger: "Enter a whole number.",
    nonNegative: "Enter a value greater than or equal to zero.",
    maxAge: "Must not exceed 120.",
    chooseRuralOrUrban: "Choose Rural or Urban.",
    conflictingAnswers: "Conflicting answers were provided.",
    booleanRequired: "Choose Yes or No; do not enter text for this answer.",
    unsupportedField: "This field is not supported.",
    sensitiveDataRejected: "Do not enter sensitive personal information in this field.",
    validationError: "Please correct the highlighted profile information.",
    fieldError: "{field}: {message}",
    httpError: "The service returned an error (HTTP {status}). Please try again.",
    serverValidationError: "The service could not validate this profile. Check the highlighted fields.",
    networkError: "Could not connect to SchemeSathi. Check the service address and try again.",
    checking: "Checking…",
    findSchemes: "Find my schemes",
    yourResults: "Your scheme results",
    farmerResults: "Farmer scheme results",
    potentialMatches: "Potential matches",
    editProfile: "Edit profile",
    loadingResults: "Loading scheme results…",
    loadingError: "Unable to load scheme results. Please try again.",
    completeProfile: "Complete your profile to see personalized eligibility results. The catalogue is not used as a fallback.",
    createProfile: "Create profile",
    likelyFarmerSchemes: "Likely Farmer Schemes",
    potentiallyRelevantSchemes: "Potentially relevant schemes",
    needsVerification: "Needs More Information / Verification",
    notApplicable: "Not Applicable to This Profile",
    notApplicableNote: "A known rule failed or no supported condition matched. This is not an official finding or denial.",
    noRecommendations: "None of the verified schemes have a relevant match for the information provided. The schemes below are shown only to explain why they do not apply; this is not an official decision.",
    noEvaluatedSchemes: "No verified schemes could be evaluated for this profile.",
    disclaimer: "Eligibility results are informational, not official decisions. Recommendations include only verified records with a relevant profile match. Not-applicable entries are not eligibility determinations. Mock and unverified records are excluded.",
    potentiallyEligible: "Potentially Eligible",
    verificationRequired: "Verification Required",
    notApplicableBadge: "Not Applicable",
    verifiedSource: "Verified source",
    notVerified: "Not verified",
    matchedDetails: "Matched details",
    failedConditions: "Known failed conditions",
    missingChecks: "Missing information / checks",
    verificationSteps: "Official verification steps",
    viewDetails: "View details",
    officialSource: "Official source",
    sourceUnavailable: "Official source unavailable",
    lastVerified: "Last verified",
    verificationDateUnavailable: "Verification date unavailable",
    verifiedCatalogue: "Verified catalogue",
    governmentSchemeInfo: "Government scheme information",
    catalogueIntro: "This is a source-backed catalogue, not a personalized eligibility result. Create a profile for deterministic matching.",
    loadingCatalogue: "Loading verified scheme records…",
    catalogueError: "Unable to load verified scheme records.",
    noVerifiedSchemes: "No verified scheme records are available.",
    dateUnavailable: "Date unavailable",
    viewSchemeDetails: "View scheme details",
    backToSchemes: "Back to schemes",
    schemeNotFound: "Scheme not found.",
    loading: "Loading…",
    centralGovernment: "Central government",
    stateGovernment: "State government",
    governmentLevelUnavailable: "Government level unavailable",
    notImplementedIn: "not implemented in",
    benefits: "Benefits",
    eligibilityRules: "Eligibility rules",
    requiredDocuments: "Required documents",
    howToApply: "How to apply",
    openApplicationPortal: "Open official application portal",
    source: "Source",
    sourceUrlUnavailable: "No source URL is available for this record.",
    verifiedSourceUnavailable: "Benefits are unavailable in the verified source.",
    documentsUnavailable: "Required documents are unavailable in the verified source.",
    applicationUnavailable: "Application steps are unavailable in the verified source.",
    noBenefitDetails: "No benefit details are listed.",
    noDocumentDetails: "No document details are listed.",
    noApplicationSteps: "No application steps are listed.",
    noMockApplicationLink: "No application link is provided for this mock record.",
    noApplicationLink: "No application link is currently available.",
    mockDisclaimer: "Mock development data only. This is not a government scheme.",
    assistant: "Scheme Assistant",
    askLanguage: "Ask in English or Telugu",
    chatEmpty: "Ask about documents, benefits or application steps.",
    chatPlaceholder: "Ask a question…",
    chatMessage: "Chat message",
    send: "Send",
    thinking: "Thinking…",
    aiUnavailable: "AI is unavailable. Please review the verified scheme details.",
    noSupportedCondition: "No supported eligibility condition matched the supplied profile. This record is not recommended for this profile; this is not an official finding of ineligibility.",
    knownProfileMismatch: "Known profile condition(s) did not match: ",
    ageLabel: "Applicant age",
    incomeLabel: "Annual family income",
    stateAvailability: "State availability",
    farmerCondition: "Applicant is a farmer",
    studentCondition: "Applicant is a student",
    landholdingCondition: "Applicant belongs to a landholding farmer family",
    ruralCondition: "Household resides in a rural area",
    puccaCondition: "Household does not own a pucca house",
    stateMatches: "matches the scheme's state availability.",
    stateExcluded: "is excluded from this scheme.",
    allowedValueMatches: "matches an allowed value.",
    allowedValueFails: "does not match any allowed value.",
    allowedStateFails: "does not match an allowed value.",
    schemeConditionMatches: "matches the stated scheme-specific condition.",
    schemeConditionFails: "does not match the stated scheme-specific condition.",
    notProvidedCondition: "is not provided, so this condition could not be checked.",
    notProvidedRule: "is not provided, so this rule could not be checked.",
    stateAllowedAll: "is allowed for all states.",
    ruleNeedsVerification: "rule needs manual verification.",
    manualVerification: "requires official verification.",
    telangana: "Telangana",
    andhraPradesh: "Andhra Pradesh",
    odisha: "Odisha",
    allIndia: "All India",
    farmer: "farmer",
    student: "student",
    yes: "Yes",
    no: "No",
    detailsNeedVerification: "details need verification"
  },
  te: {
    documentTitle: "SchemeSathi - ప్రభుత్వ పథకాల మార్గదర్శి",
    homeAria: "SchemeSathi హోమ్",
    schemeGuide: "పథకాల మార్గదర్శి",
    profile: "ప్రొఫైల్",
    verifiedSchemes: "ధృవీకరించిన పథకాలు",
    changeLanguage: "భాష మార్చండి",
    switchLanguageLabel: "English",
    heroEyebrow: "ప్రభుత్వ పథకాల మార్గదర్శి",
    heroTitle: "మీకు సరిపోయే పథకాలను కనుగొనండి",
    heroDescription: "సంబంధిత ప్రభుత్వ పథకాలను కనుగొని, అవి ఎందుకు సరిపోతాయో తెలుసుకుని, అవసరమైన పత్రాల జాబితాను సిద్ధం చేసుకోండి.",
    startProfile: "నా పథకాలను చూడండి",
    browseVerified: "ధృవీకరించిన పథకాలను చూడండి",
    ruleBasedMatching: "✓ నియమాల ఆధారిత సరిపోలిక",
    officialSources: "✓ అధికారిక మూలాలు",
    supportedLanguages: "✓ తెలుగు & ఇంగ్లీష్",
    profileMatching: "ప్రొఫైల్ ఆధారిత సరిపోలిక",
    noOfficialDecision: "ఇది అధికారిక నిర్ణయం కాదు",
    guidance: "మార్గదర్శకం",
    checkOfficialSources: "అధికారిక మూలాలను పరిశీలించండి",
    simpleProfile: "సరళమైన ప్రొఫైల్",
    profileOnlyNeeded: "సరిపోలికకు అవసరమైన వివరాలను మాత్రమే ఇవ్వండి.",
    clearReasons: "స్పష్టమైన కారణాలు",
    seeConditions: "ఏ నియమాలు సరిపోతున్నాయో స్పష్టంగా చూడండి.",
    officialGuidance: "అధికారిక మార్గదర్శకం",
    documentsAndLinks: "పత్రాలు మరియు అధికారిక దరఖాస్తు దశలు.",
    stepOne: "దశ 1",
    profileTitle: "మీ గురించి చెప్పండి",
    profileIntro: "సంబంధితంగా ఉండే పథకాలను పరిశీలించడానికి అవసరమైన వివరాలను మాత్రమే ఇవ్వండి.",
    state: "రాష్ట్రం",
    statePlaceholder: "ఉదా: తెలంగాణ",
    age: "వయస్సు",
    agePlaceholder: "ఉదా: 24",
    occupation: "వృత్తి",
    occupationPlaceholder: "ఉదా: రైతు / విద్యార్థి",
    education: "విద్య",
    educationPlaceholder: "ఉదా: పట్టభద్రులు",
    annualIncome: "వార్షిక కుటుంబ ఆదాయం",
    socialCategory: "సామాజిక వర్గం (ఐచ్ఛికం)",
    notProvided: "ఇవ్వలేదు",
    general: "సాధారణ (General)",
    otherCategory: "ఇతర",
    preferNotToSay: "చెప్పదలచుకోలేదు",
    socialCategoryHint: "ఐచ్ఛికం. ధృవీకరించిన పథక నియమం కోరినప్పుడే ఉపయోగిస్తాం; ఊహించము.",
    residence: "కుటుంబ నివాసం",
    residenceHint: "ధృవీకరించిన గ్రామీణ కుటుంబ నియమాన్ని పరిశీలించడానికి మాత్రమే.",
    unknownNotProvided: "తెలియదు / ఇవ్వలేదు",
    rural: "గ్రామీణ",
    urban: "పట్టణ",
    puccaHouseQuestion: "కుటుంబానికి పక్కా ఇల్లు ఉందా?",
    selfReportedHouse: "స్వయంగా తెలిపిన సమాచారం మాత్రమే; కుటుంబ రికార్డులను SchemeSathi ధృవీకరించదు.",
    landholdingQuestion: "భూమి కలిగిన రైతు కుటుంబంలో భాగమా?",
    selfReportedLand: "స్వయంగా తెలిపిన సమాచారం మాత్రమే; భూ రికార్డులు లేదా PM-KISAN అర్హతను ఇది ధృవీకరించదు.",
    invalidAge: "0 నుంచి 120 మధ్య పూర్తి సంఖ్యను నమోదు చేయండి.",
    invalidIncome: "సున్నా లేదా అంతకంటే ఎక్కువ పూర్తి సంఖ్యను నమోదు చేయండి.",
    invalidState: "2 నుంచి 100 అక్షరాల మధ్య రాష్ట్ర పేరును నమోదు చేయండి.",
    invalidOccupation: "1 నుంచి 100 అక్షరాల మధ్య వృత్తిని నమోదు చేయండి.",
    invalidEducation: "1 నుంచి 100 అక్షరాల మధ్య విద్యా స్థాయిని నమోదు చేయండి.",
    invalidValue: "ఈ విలువ చెల్లదు.",
    invalidInteger: "పూర్తి సంఖ్యను నమోదు చేయండి.",
    nonNegative: "సున్నా లేదా అంతకంటే ఎక్కువ విలువను నమోదు చేయండి.",
    maxAge: "120 కంటే ఎక్కువ ఉండకూడదు.",
    chooseRuralOrUrban: "గ్రామీణ లేదా పట్టణాన్ని ఎంచుకోండి.",
    conflictingAnswers: "పరస్పర విరుద్ధమైన సమాధానాలు ఇచ్చారు.",
    booleanRequired: "అవును లేదా కాదు ఎంచుకోండి; ఈ సమాధానానికి వచనాన్ని నమోదు చేయవద్దు.",
    unsupportedField: "ఈ ఫీల్డ్‌కు మద్దతు లేదు.",
    sensitiveDataRejected: "ఈ ఫీల్డ్‌లో సున్నితమైన వ్యక్తిగత సమాచారాన్ని నమోదు చేయవద్దు.",
    validationError: "ప్రొఫైల్‌లో సూచించిన వివరాలను సరిచేయండి.",
    fieldError: "{field}: {message}",
    httpError: "సేవలో లోపం వచ్చింది (HTTP {status}). మళ్లీ ప్రయత్నించండి.",
    serverValidationError: "ఈ ప్రొఫైల్‌ను సేవ ధృవీకరించలేకపోయింది. సూచించిన వివరాలను తనిఖీ చేయండి.",
    networkError: "SchemeSathi సేవకు కనెక్ట్ కాలేదు. సేవ చిరునామాను తనిఖీ చేసి మళ్లీ ప్రయత్నించండి.",
    checking: "పరిశీలిస్తోంది…",
    findSchemes: "నా పథకాలను కనుగొనండి",
    yourResults: "మీ పథక ఫలితాలు",
    farmerResults: "రైతు పథక ఫలితాలు",
    potentialMatches: "సంభావ్య సరిపోలికలు",
    editProfile: "ప్రొఫైల్ మార్చండి",
    loadingResults: "పథక ఫలితాలను లోడ్ చేస్తోంది…",
    loadingError: "పథక ఫలితాలను లోడ్ చేయలేకపోయాం. మళ్లీ ప్రయత్నించండి.",
    completeProfile: "వ్యక్తిగత అర్హత ఫలితాల కోసం ముందుగా ప్రొఫైల్‌ను పూరించండి. పూర్తి జాబితాను ప్రత్యామ్నాయంగా చూపించము.",
    createProfile: "ప్రొఫైల్ ప్రారంభించండి",
    likelyFarmerSchemes: "రైతులకు సంభావ్య పథకాలు",
    potentiallyRelevantSchemes: "సంబంధితంగా ఉండే పథకాలు",
    needsVerification: "మరింత సమాచారం / ధృవీకరణ అవసరం",
    notApplicable: "ఈ ప్రొఫైల్‌కు వర్తించదు",
    notApplicableNote: "తెలిసిన నియమం సరిపోలలేదు లేదా మద్దతు ఉన్న ప్రమాణం సరిపోలలేదు. ఇది అధికారిక తిరస్కరణ కాదు.",
    noRecommendations: "మీరు ఇచ్చిన వివరాలకు సరిపోయే ధృవీకరించిన పథకం లేదు. దిగువ పథకాలు ఎందుకు వర్తించవో వివరించడానికి మాత్రమే చూపబడ్డాయి; ఇది అధికారిక నిర్ణయం కాదు.",
    noEvaluatedSchemes: "ఈ ప్రొఫైల్‌కు పరిశీలించగల ధృవీకరించిన పథకాలు లేవు.",
    disclaimer: "ఈ ఫలితాలు సమాచార మార్గదర్శకం మాత్రమే; అధికారిక నిర్ణయం కావు. సంబంధిత ప్రొఫైల్ సరిపోలిక ఉన్న ధృవీకరించిన పథకాలనే సిఫార్సుల్లో చూపిస్తాం. వర్తించని పథకాల జాబితా అర్హత నిర్ణయం కాదు. మాక్ మరియు ధృవీకరించని రికార్డులు మినహాయించబడ్డాయి.",
    potentiallyEligible: "సంభావ్యంగా సరిపోతుంది",
    verificationRequired: "ధృవీకరణ అవసరం",
    notApplicableBadge: "వర్తించదు",
    verifiedSource: "ధృవీకరించిన మూలం",
    notVerified: "ధృవీకరించలేదు",
    matchedDetails: "సరిపోలిన వివరాలు",
    failedConditions: "సరిపోలని తెలిసిన నియమాలు",
    missingChecks: "ఇంకా తెలియాల్సినవి / తనిఖీలు",
    verificationSteps: "అధికారిక ధృవీకరణ దశలు",
    viewDetails: "వివరాలు చూడండి",
    officialSource: "అధికారిక మూలం",
    sourceUnavailable: "అధికారిక మూలం అందుబాటులో లేదు",
    lastVerified: "చివరిగా ధృవీకరించిన తేదీ",
    verificationDateUnavailable: "ధృవీకరణ తేదీ అందుబాటులో లేదు",
    verifiedCatalogue: "ధృవీకరించిన జాబితా",
    governmentSchemeInfo: "ప్రభుత్వ పథకాల సమాచారం",
    catalogueIntro: "ఇది అధికారిక మూలాల ఆధారిత జాబితా మాత్రమే; వ్యక్తిగత అర్హత ఫలితం కాదు. నియమాధారిత సరిపోలిక కోసం ప్రొఫైల్ పూరించండి.",
    loadingCatalogue: "ధృవీకరించిన పథకాల వివరాలను లోడ్ చేస్తోంది…",
    catalogueError: "ధృవీకరించిన పథకాల వివరాలను లోడ్ చేయలేకపోయాం.",
    noVerifiedSchemes: "ధృవీకరించిన పథకాల రికార్డులు అందుబాటులో లేవు.",
    dateUnavailable: "తేదీ అందుబాటులో లేదు",
    viewSchemeDetails: "పథక వివరాలు చూడండి",
    backToSchemes: "పథకాలకు తిరిగి వెళ్లండి",
    schemeNotFound: "పథకం కనుగొనబడలేదు.",
    loading: "లోడ్ అవుతోంది…",
    centralGovernment: "కేంద్ర ప్రభుత్వం",
    stateGovernment: "రాష్ట్ర ప్రభుత్వం",
    governmentLevelUnavailable: "ప్రభుత్వ స్థాయి అందుబాటులో లేదు",
    notImplementedIn: "అమలులో లేని రాష్ట్రాలు",
    benefits: "ప్రయోజనాలు",
    eligibilityRules: "అర్హత నియమాలు",
    requiredDocuments: "అవసరమైన పత్రాలు",
    howToApply: "ఎలా దరఖాస్తు చేయాలి",
    openApplicationPortal: "అధికారిక దరఖాస్తు పోర్టల్‌ను తెరవండి",
    source: "మూలం",
    sourceUrlUnavailable: "ఈ రికార్డుకు మూల URL అందుబాటులో లేదు.",
    verifiedSourceUnavailable: "ధృవీకరించిన మూలంలో ప్రయోజనాల వివరాలు లేవు.",
    documentsUnavailable: "ధృవీకరించిన మూలంలో అవసరమైన పత్రాల వివరాలు లేవు.",
    applicationUnavailable: "ధృవీకరించిన మూలంలో దరఖాస్తు దశలు లేవు.",
    noBenefitDetails: "ప్రయోజనాల వివరాలు ఇవ్వలేదు.",
    noDocumentDetails: "పత్రాల వివరాలు ఇవ్వలేదు.",
    noApplicationSteps: "దరఖాస్తు దశలు ఇవ్వలేదు.",
    noMockApplicationLink: "ఈ మాక్ రికార్డుకు దరఖాస్తు లింక్ లేదు.",
    noApplicationLink: "ప్రస్తుతం దరఖాస్తు లింక్ అందుబాటులో లేదు.",
    mockDisclaimer: "ఇది అభివృద్ధి కోసం ఉన్న మాక్ డేటా మాత్రమే; ప్రభుత్వ పథకం కాదు.",
    assistant: "పథకాల సహాయకుడు",
    askLanguage: "తెలుగు లేదా ఇంగ్లీష్‌లో అడగండి",
    chatEmpty: "పత్రాలు, ప్రయోజనాలు లేదా దరఖాస్తు దశల గురించి అడగండి.",
    chatPlaceholder: "మీ ప్రశ్న రాయండి…",
    chatMessage: "చాట్ సందేశం",
    send: "పంపండి",
    thinking: "సమాధానం సిద్ధం చేస్తోంది…",
    aiUnavailable: "AI సేవ అందుబాటులో లేదు. ధృవీకరించిన పథక వివరాలను పరిశీలించండి.",
    noSupportedCondition: "మీ ప్రొఫైల్‌కు మద్దతు ఉన్న అర్హత నియమం సరిపోలలేదు. ఈ ప్రొఫైల్‌కు ఈ రికార్డును సిఫార్సు చేయము; ఇది అధికారిక అనర్హత నిర్ణయం కాదు.",
    knownProfileMismatch: "తెలిసిన ప్రొఫైల్ నియమాలు సరిపోలలేదు: ",
    ageLabel: "దరఖాస్తుదారు వయస్సు",
    incomeLabel: "వార్షిక కుటుంబ ఆదాయం",
    stateAvailability: "రాష్ట్రంలో పథకం అమలు",
    farmerCondition: "దరఖాస్తుదారు రైతు",
    studentCondition: "దరఖాస్తుదారు విద్యార్థి",
    landholdingCondition: "దరఖాస్తుదారు భూమి కలిగిన రైతు కుటుంబానికి చెందినవారు",
    ruralCondition: "కుటుంబం గ్రామీణ ప్రాంతంలో నివసిస్తుంది",
    puccaCondition: "కుటుంబానికి పక్కా ఇల్లు లేదు",
    stateMatches: "ఈ పథకం రాష్ట్ర లభ్యతకు సరిపోతుంది.",
    stateExcluded: "ఈ పథకం ఈ రాష్ట్రంలో అమలులో లేదు.",
    allowedValueMatches: "అనుమతించిన విలువతో సరిపోతుంది.",
    allowedValueFails: "అనుమతించిన విలువలతో సరిపోలలేదు.",
    allowedStateFails: "అనుమతించిన రాష్ట్రంతో సరిపోలలేదు.",
    schemeConditionMatches: "పథకానికి సంబంధించిన పేర్కొన్న నియమంతో సరిపోతుంది.",
    schemeConditionFails: "పథకానికి సంబంధించిన పేర్కొన్న నియమంతో సరిపోలలేదు.",
    notProvidedCondition: "ఇవ్వలేదు; అందువల్ల ఈ నియమాన్ని పరిశీలించలేకపోయాం.",
    notProvidedRule: "ఇవ్వలేదు; అందువల్ల ఈ నియమాన్ని పరిశీలించలేకపోయాం.",
    stateAllowedAll: "అన్ని రాష్ట్రాలకు వర్తిస్తుంది.",
    ruleNeedsVerification: "నియమానికి మానవ ధృవీకరణ అవసరం.",
    manualVerification: "అధికారిక ధృవీకరణ అవసరం.",
    telangana: "తెలంగాణ",
    andhraPradesh: "ఆంధ్రప్రదేశ్",
    odisha: "ఒడిశా",
    allIndia: "భారతదేశమంతటా",
    farmer: "రైతు",
    student: "విద్యార్థి",
    yes: "అవును",
    no: "కాదు",
    detailsNeedVerification: "వివరాలకు ధృవీకరణ అవసరం"
  }
}

const fieldLabels = {
  state: "state",
  age: "age",
  occupation: "occupation",
  education_level: "education",
  annual_family_income: "annualIncome",
  social_category: "socialCategory",
  gender: "occupation",
  additional_attributes: "residence"
}

const schemeTranslations = {
  "mock-education-support": {
    name: "విద్యా సహాయం (MOCK DEVELOPMENT RECORD - Education Support)",
    department: "మాక్ విభాగం (అభివృద్ధి ప్రయోజనాల కోసం మాత్రమే)",
    description: "SchemeSathi API అభివృద్ధి మరియు పరీక్ష కోసం కల్పిత నమూనా రికార్డు. ఇది ప్రభుత్వ పథకం కాదు.",
    benefits: ["మాక్ ప్రయోజన నమూనా; ఇది నిజమైన ప్రయోజనం కాదు."],
    eligibility_summary: "ఇది పరీక్ష కోసం మాత్రమే ఉన్న కల్పిత రికార్డు.",
    required_documents: ["మాక్ పత్ర నమూనా; ఇది నిజమైన పత్రాల జాబితా కాదు."]
  },
  "mock-agriculture-support": {
    name: "వ్యవసాయ సహాయం (MOCK DEVELOPMENT RECORD - Agriculture Support)",
    department: "మాక్ విభాగం (అభివృద్ధి ప్రయోజనాల కోసం మాత్రమే)",
    description: "SchemeSathi API అభివృద్ధి మరియు పరీక్ష కోసం కల్పిత నమూనా రికార్డు. ఇది ప్రభుత్వ పథకం కాదు.",
    benefits: ["మాక్ ప్రయోజన నమూనా; ఇది నిజమైన ప్రయోజనం కాదు."],
    eligibility_summary: "ఇది పరీక్ష కోసం మాత్రమే ఉన్న కల్పిత రికార్డు.",
    required_documents: ["మాక్ పత్ర నమూనా; ఇది నిజమైన పత్రాల జాబితా కాదు."]
  },
  "pm-kisan-samman-nidhi": {
    name: "ప్రధాన మంత్రి కిసాన్ సమ్మాన్ నిధి (Pradhan Mantri Kisan Samman Nidhi, PM-KISAN)",
    department: "వ్యవసాయ మరియు రైతు సంక్షేమ శాఖ, భారత ప్రభుత్వం (Department of Agriculture and Farmers Welfare, Government of India)",
    description: "వ్యవసాయ మరియు రైతు సంక్షేమ శాఖ నిర్వహించే కేంద్ర రైతు మద్దతు కార్యక్రమం. నమోదు చేసుకున్న రైతుల వాయిదాలు మరియు తప్పనిసరి e-KYC వివరాలను అధికారిక పోర్టల్‌లో చూడవచ్చు.",
    benefits: ["అధికారిక పోర్టల్ PM-KISAN వాయిదాలను చూపిస్తుంది; పరిశీలించిన పేజీలో ప్రయోజన మొత్తం పేర్కొనలేదు."],
    eligibility_summary: "పరిశీలించిన అధికారిక పోర్టల్ ప్రకారం, భూమి యాజమాన్యం మరియు ఒకే కుటుంబంలో పలువురు సభ్యుల కేసులు భౌతిక తనిఖీకి లోబడి ఉండే మినహాయింపు సమస్యలు కావచ్చు. పూర్తి అర్హత ప్రమాణాలు మరియు మొత్తాన్ని అధికారిక పోర్టల్‌లో తనిఖీ చేయాలి.",
    application_process: [
      "నమోదు చేసుకున్న రైతులు అధికారిక పోర్టల్, PM-KISAN మొబైల్ యాప్, కామన్ సర్వీస్ సెంటర్ బయోమెట్రిక్ విధానం లేదా రాష్ట్ర అధీకృత వినియోగదారు ద్వారా తప్పనిసరి e-KYC పూర్తి చేయాలి.",
      "అధికారిక Know Your Status సేవలో స్థితిని తనిఖీ చేసి, అక్కడ ఇచ్చిన ధృవీకరణ సూచనలను అనుసరించండి."
    ]
  },
  "pmay-gramin": {
    name: "ప్రధాన మంత్రి ఆవాస్ యోజన - గ్రామీణ (Pradhan Mantri Awaas Yojana - Gramin, PMAY-G)",
    department: "గ్రామీణాభివృద్ధి మంత్రిత్వ శాఖ, భారత ప్రభుత్వం (Ministry of Rural Development, Government of India)",
    description: "భారత ప్రభుత్వ గ్రామీణ గృహ పథకం. అధికారిక పౌర పోర్టల్‌లో కుటుంబ అర్హత ప్రశ్నావళి, దరఖాస్తు స్థితి మరియు మంజూరు/చెల్లింపు వివరాలు ఉన్నాయి.",
    benefits: ["మంజూరైన ఇళ్ల ద్వారా గ్రామీణ గృహ సహాయం అందిస్తుంది; పరిశీలించిన పోర్టల్‌లో సహాయ మొత్తం పేర్కొనలేదు."],
    eligibility_summary: "అధికారిక ప్రశ్నావళి కుటుంబ దుర్బలత, గ్రామీణ నివాసం, ఇంటి పరిస్థితి, కుటుంబ ఆస్తులు, కిసాన్ క్రెడిట్ కార్డు పరిమితులు, ప్రభుత్వ ఉద్యోగం, నమోదిత సంస్థలు, నెలవారీ ఆదాయం, పన్ను స్థితి మరియు సాగునీటి/వర్షాధార భూమిని పరిశీలిస్తుంది. తుది కుటుంబ ఎంపిక అధికారిక ప్రక్రియ ద్వారానే జరుగుతుంది.",
    application_process: [
      "కుటుంబ పరిస్థితులను పరిశీలించడానికి అధికారిక Check Eligibility ప్రశ్నావళిని ఉపయోగించండి.",
      "ధృవీకరణ మరియు శాశ్వత నిరీక్షణ జాబితా స్థితి కోసం Track Your Application సేవను ఉపయోగించండి.",
      "మంజూరు మరియు వాయిదా వివరాల కోసం View Sanction and Payment సేవను ఉపయోగించండి."
    ]
  },
  "pradhan-mantri-matru-vandana-yojana": {
    name: "ప్రధాన మంత్రి మాతృ వందన యోజన (Pradhan Mantri Matru Vandana Yojana, PMMVY)",
    department: "మహిళా మరియు శిశు అభివృద్ధి మంత్రిత్వ శాఖ, భారత ప్రభుత్వం (Ministry of Women and Child Development, Government of India)",
    description: "అర్హులైన గర్భిణీ మరియు పాలిచ్చే మహిళలకు ఆర్థిక సహాయం అందించే పథకం. ఇందులో కొంత వేతన నష్టం పరిహారం మరియు తల్లి-శిశు ఆరోగ్య సహాయం ఉన్నాయి.",
    benefits: [
      "మొదటి బిడ్డకు రెండు విడతల్లో ₹5,000: గర్భధారణ నమోదు మరియు అవసరమైన గర్భపూర్వ పరీక్షల తర్వాత ₹3,000; జనన నమోదు మరియు 14 వారాలకు మొదటి టీకా చక్రం పూర్తయ్యాక ₹2,000.",
      "రెండవ బిడ్డ ఆడపిల్ల అయితే, జనన నమోదు మరియు 14 వారాలకు మొదటి టీకా చక్రం పూర్తయ్యాక ఒక విడతలో ₹6,000."
    ],
    eligibility_summary: "అధికారిక FAQలో SC/ST మహిళలు, కనీసం 40% వైకల్యం ఉన్న మహిళలు, BPL లేదా NFSA రేషన్ కార్డు కలిగినవారు, PM-JAY లబ్ధిదారులు, e-Shram కార్డు కలిగినవారు, PM-KISAN పొందే మహిళా రైతులు, MGNREGA జాబ్ కార్డు కలిగినవారు, వార్షిక కుటుంబ ఆదాయం ₹8 లక్షల కంటే తక్కువ ఉన్నవారు మరియు గర్భిణీ/పాలిచ్చే AWW, AWH, ASHA కార్యకర్తలు అర్హత వర్గాలుగా పేర్కొనబడ్డారు. ప్రసవ సమయానికి వయస్సు 18 సంవత్సరాల 7 నెలల నుంచి 55 కంటే తక్కువగా ఉండాలి; ప్రసవం తర్వాత 270 రోజుల్లో నమోదు చేయాలి. FAQ ప్రకారం తెలంగాణ మరియు ఒడిశాలో ఈ పథకం అమలులో లేదు.",
    required_documents: [
      "ఆధార్ కార్డు (అధికారిక పథక పోర్టల్‌లో అవసరం; SchemeSathi దీనిని సేకరించదు)",
      "ఆధార్‌కు అనుసంధానమైన బ్యాంకు లేదా పోస్టాఫీసు ఖాతా వివరాలు (SchemeSathi సేకరించదు)",
      "అర్హత వర్గానికి సంబంధించిన ఆధారం",
      "MCP/RCHI కార్డు",
      "చివరి రుతుస్రావం (LMP) మరియు గర్భపూర్వ పరీక్ష (ANC) తేదీలు",
      "శిశువు జనన ధృవీకరణ పత్రం మరియు టీకాల వివరాలు",
      "దరఖాస్తు/చెల్లింపు స్థితి కోసం మొబైల్ నంబరు (SchemeSathi సేకరించదు)"
    ],
    application_process: [
      "అర్హురాలైన మహిళ అధికారిక PMMVY పోర్టల్‌లో స్వయంగా నమోదు చేసుకోవచ్చు లేదా అంగన్‌వాడీ కార్యకర్త/ASHA ద్వారా దరఖాస్తు సహాయం పొందవచ్చు.",
      "మొదటి బిడ్డకు గర్భధారణ నమోదు మరియు కనీసం రెండు గర్భపూర్వ పరీక్షలు అవసరం; తర్వాత జనన నమోదు చేసి మొదటి టీకా చక్రాన్ని పూర్తి చేయాలి.",
      "రెండవ బిడ్డ ఆడపిల్ల అయితే గర్భధారణ నమోదు మరియు కనీసం రెండు గర్భపూర్వ పరీక్షలు అవసరం; తర్వాత జనన నమోదు చేసి మొదటి టీకా చక్రాన్ని పూర్తి చేయాలి.",
      "ప్రసవం తర్వాత 270 రోజుల వరకు నమోదు చేసుకోవచ్చని అధికారిక FAQ చెబుతుంది."
    ]
  },
  "pm-usp-csss": {
    name: "కళాశాల మరియు విశ్వవిద్యాలయ విద్యార్థుల PM-USP కేంద్ర స్కాలర్‌షిప్ పథకం (PM-USP Central Sector Scheme of Scholarship for College and University Students, CSSS)",
    department: "సమీక్షించిన అధికారిక పథక నోటీసులో గుర్తించబడలేదు",
    description: "కళాశాల మరియు విశ్వవిద్యాలయ విద్యార్థుల కోసం కేంద్ర స్కాలర్‌షిప్ పథకం. ఈ రికార్డు ధృవీకరించిన సమయంలో కొత్త దరఖాస్తులు తెరిచి ఉన్నాయని National Scholarship Portal ప్రకటించింది.",
    benefits: ["స్కాలర్‌షిప్ సహాయం; పరిశీలించిన అధికారిక ప్రకటనలో మొత్తం లేదా అవార్డు నిబంధనలు పేర్కొనలేదు."],
    eligibility_summary: "పరిశీలించిన అధికారిక పోర్టల్ ప్రకటనలో ఈ పథకానికి సంబంధించిన పూర్తి అర్హత ప్రమాణాలు లేవు. ప్రస్తుత CSSS మార్గదర్శకాలు మరియు దరఖాస్తు కాలాన్ని National Scholarship Portalలో తనిఖీ చేయండి.",
    application_process: [
      "National Scholarship Portalలో అవసరమైన One Time Registration (OTR) పూర్తి చేయండి.",
      "CSSS దరఖాస్తు కాలాన్ని తనిఖీ చేసి National Scholarship Portal ద్వారా దరఖాస్తు సమర్పించండి."
    ]
  },
  "ntr-bharosa-pension": {
    name: "NTR భరోసా పెన్షన్ పథకం (NTR Bharosa Pension Scheme)",
    department: "ఆంధ్రప్రదేశ్ ప్రభుత్వం (సమీక్షించిన పేజీలో నిర్దిష్ట శాఖ గుర్తించబడలేదు)",
    description: "ఆంధ్రప్రదేశ్ సామాజిక భద్రతా పెన్షన్లు. వృద్ధులు, వితంతువులు, ఒంటరి మహిళలు, వైకల్యం ఉన్నవారు మరియు పేర్కొన్న దీర్ఘకాలిక ఆరోగ్య సమస్యలు ఉన్నవారు వంటి వర్గాలు ఇందులో ఉన్నాయి.",
    benefits: [
      "వృద్ధులు, వితంతువులు, ఒంటరి మహిళలు, మత్స్యకారులు, చేనేత కార్మికులు మరియు ఇతర పేర్కొన్న వర్గాలకు నెలకు ₹4,000 అని అధికారిక పేజీ చెబుతుంది.",
      "వైకల్యం మరియు బహుళ వైకల్యం/కుష్ఠు వర్గాలకు నెలకు ₹6,000 అని అధికారిక పేజీ చెబుతుంది.",
      "పేర్కొన్న దీర్ఘకాలిక వ్యాధుల వర్గాలకు నెలకు ₹10,000 అని అధికారిక పేజీ చెబుతుంది."
    ],
    eligibility_summary: "అధికారిక పేజీ పెన్షన్ వర్గాలను పేర్కొంటుంది; కానీ ప్రతి వర్గానికి పూర్తి వయస్సు, ఆదాయం లేదా పత్రాల ప్రమాణాలు ఇవ్వలేదు. తీవ్రమైన వైకల్యం ఉన్నవారికి చూపిన మొత్తాల్లోనూ వ్యత్యాసం ఉంది; ప్రస్తుత మొత్తం మరియు అర్హతను ఆంధ్రప్రదేశ్ పోర్టల్‌లో ధృవీకరించండి."
  },
  "telangana-rythu-bharosa": {
    name: "తెలంగాణ రైతు భరోసా (Telangana Rythu Bharosa)",
    department: "వ్యవసాయ శాఖ, తెలంగాణ ప్రభుత్వం (Department of Agriculture, Government of Telangana)",
    description: "తెలంగాణ రైతులకు మద్దతు ఇచ్చే పథకం. అధికారిక పోర్టల్ ప్రకారం, రైతులకు సకాలంలో ఆర్థిక సహాయం మరియు వ్యవసాయ వనరుల ప్రాప్యత కల్పించడం దీని ఉద్దేశం.",
    benefits: ["2026 జూలైలో తెలంగాణ ప్రభుత్వ ప్రకటన ప్రకారం రైతు భరోసా సహాయాన్ని ఎకరానికి ₹12,000కు పెంచారు."],
    eligibility_summary: "అధికారిక పోర్టల్ రైతులను లక్ష్య వర్గంగా పేర్కొంటుంది; కానీ పూర్తి లబ్ధిదారుల అర్హతలు లేదా మినహాయింపులను ప్రచురించలేదు. ప్రస్తుత అర్హతను వ్యవసాయ శాఖతో ధృవీకరించాలి."
  }
}

const exactTranslations = {
  "Any landholding status provided is self-reported. SchemeSathi does not verify land records, official beneficiary records, or applicable exclusions; e-KYC status has not been checked. Confirm these through official PM-KISAN services.":
    "భూమి కలిగిన రైతు కుటుంబ స్థితి గురించి ఇచ్చిన సమాచారం స్వయంగా తెలిపినదే. SchemeSathi భూ రికార్డులు, అధికారిక లబ్ధిదారుల రికార్డులు లేదా వర్తించే మినహాయింపులను ధృవీకరించదు; e-KYC స్థితిని తనిఖీ చేయలేదు. అధికారిక PM-KISAN సేవల ద్వారా వీటిని ధృవీకరించండి.",
  "Any landholding status provided is self-reported.":
    "భూమి కలిగిన రైతు కుటుంబ స్థితి గురించి ఇచ్చిన సమాచారం స్వయంగా తెలిపినదే.",
  "SchemeSathi does not verify land records, official beneficiary records, or applicable exclusions; e-KYC status has not been checked.":
    "SchemeSathi భూ రికార్డులు, అధికారిక లబ్ధిదారుల రికార్డులు లేదా వర్తించే మినహాయింపులను ధృవీకరించదు; e-KYC స్థితిని తనిఖీ చేయలేదు.",
  "Confirm these through official PM-KISAN services.":
    "అధికారిక PM-KISAN సేవల ద్వారా వీటిని ధృవీకరించండి.",
  "For registered farmers, complete mandatory e-KYC using the official portal, PM-KISAN mobile application, a Common Service Centre biometric option, or State Authorized User login.":
    "నమోదు చేసుకున్న రైతులు అధికారిక పోర్టల్, PM-KISAN మొబైల్ యాప్, కామన్ సర్వీస్ సెంటర్ బయోమెట్రిక్ విధానం లేదా రాష్ట్ర అధీకృత వినియోగదారు ద్వారా తప్పనిసరి e-KYC పూర్తి చేయాలి.",
  "Use the official Know Your Status service to check status and follow any verification instructions.":
    "అధికారిక Know Your Status సేవలో స్థితిని తనిఖీ చేసి, అక్కడ ఇచ్చిన ధృవీకరణ సూచనలను అనుసరించండి.",
  "The full household questionnaire and official selection criteria require verification":
    "పూర్తి కుటుంబ ప్రశ్నావళి మరియు అధికారిక ఎంపిక ప్రమాణాలను ధృవీకరించాలి.",
  "The qualifying category, childbirth timing, and supporting evidence require official verification":
    "అర్హత వర్గం, ప్రసవ సమయం మరియు ఆధార పత్రాలను అధికారికంగా ధృవీకరించాలి.",
  "Scheme-specific academic, income, and selection criteria require verification":
    "పథకానికి సంబంధించిన విద్యా, ఆదాయ మరియు ఎంపిక ప్రమాణాలను ధృవీకరించాలి.",
  "Pension-category and category-specific qualification criteria require official verification":
    "పెన్షన్ వర్గం మరియు దానికి సంబంధించిన అర్హత ప్రమాణాలను అధికారికంగా ధృవీకరించాలి.",
  "The official Telangana Rythu Bharosa portal does not publish detailed beneficiary eligibility, exclusions, required documents, or complete application instructions. Verify current beneficiary criteria with the Department of Agriculture before applying.":
    "తెలంగాణ రైతు భరోసా అధికారిక పోర్టల్‌లో పూర్తి లబ్ధిదారుల అర్హతలు, మినహాయింపులు, అవసరమైన పత్రాలు లేదా దరఖాస్తు సూచనలు లేవు. దరఖాస్తు చేసే ముందు ప్రస్తుత అర్హతను వ్యవసాయ శాఖతో ధృవీకరించండి.",
  "The official Telangana Rythu Bharosa portal does not publish detailed beneficiary eligibility, exclusions, required documents, or complete application instructions.":
    "తెలంగాణ రైతు భరోసా అధికారిక పోర్టల్‌లో పూర్తి లబ్ధిదారుల అర్హతలు, మినహాయింపులు, అవసరమైన పత్రాలు లేదా దరఖాస్తు సూచనలు లేవు.",
  "Verify current beneficiary criteria with the Department of Agriculture before applying.":
    "దరఖాస్తు చేసే ముందు ప్రస్తుత అర్హతను వ్యవసాయ శాఖతో ధృవీకరించండి.",
  "No eligibility rules are available to assess this scheme.":
    "ఈ పథకాన్ని అంచనా వేయడానికి అర్హత నియమాలు అందుబాటులో లేవు.",
  "Eligibility results are informational, not official decisions. Recommendations include only verified records with a relevant profile match. Not-applicable entries are not eligibility determinations. Mock and unverified records are excluded.":
    messages.te.disclaimer,
  "No supported eligibility condition matched the supplied profile. This record is not recommended for this profile; this is not an official finding of ineligibility.":
    messages.te.noSupportedCondition
}

const ruleLabels = {
  "Applicant is a farmer": "farmerCondition",
  "Applicant is a student": "studentCondition",
  "Applicant belongs to a landholding farmer family": "landholdingCondition",
  "Household resides in a rural area": "ruralCondition",
  "Household does not own a pucca house": "puccaCondition",
  "State availability": "stateAvailability",
  "Applicant age": "ageLabel",
  "Annual family income": "incomeLabel"
}

const attributeLabels = {
  resides_in_rural_area: "residence",
  household_owns_pucca_house: "puccaHouseQuestion",
  pm_kisan_landholding_farmer_family: "landholdingQuestion"
}

const localizedValues = {
  "Andhra Pradesh": "andhraPradesh",
  Telangana: "telangana",
  Odisha: "odisha",
  "All India": "allIndia",
  farmer: "farmer",
  student: "student",
  true: "yes",
  false: "no"
}

export function t(language, key, values = {}) {
  const locale = language === "te" ? "te" : "en"
  const template = messages[locale][key] || messages.en[key] || key
  return template.replace(/\{(\w+)\}/g, (match, name) =>
    values[name] === undefined ? match : String(values[name])
  )
}

export function localizedScheme(scheme, language) {
  const translated = language === "te" ? schemeTranslations[scheme.id] : null
  if (!translated) return scheme
  return {
    ...scheme,
    name_te: translated.name || scheme.name,
    department_te: translated.department || scheme.department,
    description_te: translated.description || scheme.description,
    benefits_te: translated.benefits || scheme.benefits,
    eligibility_summary_te: translated.eligibility_summary || scheme.eligibility_summary,
    required_documents_te: translated.required_documents || scheme.required_documents,
    application_process_te: translated.application_process || scheme.application_process
  }
}

function localizeRuleLabel(value, language) {
  const typeLabels = {
    state: "stateAvailability",
    occupation: "occupation",
    education_level: "education",
    age: "ageLabel",
    annual_family_income: "incomeLabel",
    income: "incomeLabel",
    gender: "socialCategory"
  }
  if (typeLabels[value]) return t(language, typeLabels[value])
  const key = ruleLabels[value]
  return key ? t(language, key) : value
}

function localizeValue(value, language) {
  const key = localizedValues[String(value)]
  return key ? t(language, key) : String(value)
}

export function localizeEligibilityText(text, language) {
  if (!text || language !== "te") return text
  if (exactTranslations[text]) return exactTranslations[text]

  const prefix = "Known profile condition(s) did not match: "
  if (text.startsWith(prefix)) {
    return `${t(language, "knownProfileMismatch")}${localizeEligibilityText(text.slice(prefix.length), language)}`
  }
  if (text === messages.en.noSupportedCondition) {
    return t(language, "noSupportedCondition")
  }
  const sentences = text.match(/[^.]+(?:\.|$)/g) || []
  if (sentences.length > 1) {
    return sentences
      .map((sentence) => localizeEligibilityText(sentence.trim(), language))
      .join(" ")
  }

  const conditionPhrases = [
    ["Applicant is a farmer", "farmerCondition"],
    ["Applicant is a student", "studentCondition"],
    ["Applicant belongs to a landholding farmer family", "landholdingCondition"],
    ["Household resides in a rural area", "ruralCondition"],
    ["Household does not own a pucca house", "puccaCondition"],
    ["State availability", "stateAvailability"],
    ["Applicant age", "ageLabel"],
    ["Annual family income", "incomeLabel"]
  ]
  for (const [source, key] of conditionPhrases) {
    if (text === source) return t(language, key)
    if (!text.startsWith(`${source} `)) continue
    const suffix = text.slice(source.length + 1)
    const suffixTranslations = {
      "matches an allowed value.": "allowedValueMatches",
      "does not match any allowed value.": "allowedValueFails",
      "does not match an allowed value.": "allowedStateFails",
      "matches the stated scheme-specific condition.": "schemeConditionMatches",
      "does not match the stated scheme-specific condition.": "schemeConditionFails",
      "is not provided, so this condition could not be checked.": "notProvidedCondition",
      "is not provided, so this rule could not be checked.": "notProvidedRule",
      "matches the scheme's state availability.": "stateMatches",
      "is excluded from this scheme.": "stateExcluded",
      "is allowed for all states.": "stateAllowedAll"
    }
    if (suffixTranslations[suffix]) {
      return `${t(language, key)} ${t(language, suffixTranslations[suffix])}`
    }
  }
  return exactTranslations[text] || text
}

export function describeRule(rule, language) {
  const locale = language === "te" ? "te" : "en"
  const label = localizeRuleLabel(
    rule.label || rule.type.replaceAll("_", " "),
    language
  )
  const values = (items) => items.map((value) => localizeValue(value, language)).join(", ")
  if (rule.values && rule.not_values) {
    return locale === "te"
      ? `${label}: ${values(rule.values)} (మినహా ${values(rule.not_values)})`
      : `${label}: ${values(rule.values)} except ${values(rule.not_values)}`
  }
  if (rule.not_values) {
    return locale === "te"
      ? `${label}: ${values(rule.not_values)} కాకుండా`
      : `${label}: not ${values(rule.not_values)}`
  }
  if (rule.values) return `${label}: ${values(rule.values)}`
  if (rule.min != null || rule.max != null) {
    const minimum = rule.min ?? (locale === "te" ? "కనిష్ఠ పరిమితి లేదు" : "no minimum")
    const maximum = rule.max ?? (locale === "te" ? "గరిష్ఠ పరిమితి లేదు" : "no maximum")
    return `${label}: ${minimum} ${locale === "te" ? "నుంచి" : "to"} ${maximum}`
  }
  if (rule.attribute) {
    const attributeKey = attributeLabels[rule.attribute]
    const localizedAttribute = attributeKey
      ? t(language, attributeKey)
      : rule.attribute
    const operators = {
      equals: locale === "te" ? "సమానం" : "equals",
      not_equals: locale === "te" ? "సమానం కాదు" : "does not equal",
      in: locale === "te" ? "వీటిలో ఒకటి" : "is one of",
      not_in: locale === "te" ? "వీటిలో లేదు" : "is not one of"
    }
    const value = rule.value === undefined ? "" : localizeValue(rule.value, language)
    return `${label}: ${localizedAttribute} ${operators[rule.operator] || (locale === "te" ? "విలువ" : "is")} ${value}`
  }
  if (rule.type === "manual_verification" && rule.label) {
    return localizeEligibilityText(rule.label, language)
  }
  return `${label}: ${t(language, "detailsNeedVerification")}`
}

function validationReason(message, language) {
  const cleanMessage = message.replace(/^Value error,\s*/, "")
  if (language !== "te") return cleanMessage
  if (cleanMessage.includes("must be a JSON boolean")) return t(language, "booleanRequired")
  if (cleanMessage.includes("residence_type must be 'rural' or 'urban'")) return t(language, "chooseRuralOrUrban")
  if (cleanMessage.includes("conflicts with")) return t(language, "conflictingAnswers")
  if (
    cleanMessage.includes("sensitive information")
    || cleanMessage.includes("Aadhaar")
    || cleanMessage.includes("OTP")
    || cleanMessage.includes("bank")
  ) return t(language, "sensitiveDataRejected")
  if (cleanMessage.includes("greater than or equal to 0")) return t(language, "nonNegative")
  if (cleanMessage.includes("less than or equal to 120")) return t(language, "maxAge")
  if (cleanMessage.includes("valid integer")) return t(language, "invalidInteger")
  if (cleanMessage.includes("extra inputs are not permitted")) return t(language, "unsupportedField")
  return t(language, "invalidValue")
}

function localizedFieldError(field, message, language) {
  const key = fieldLabels[field] || "profile"
  return t(language, "fieldError", {
    field: t(language, key),
    message: validationReason(message, language)
  })
}

export function validateProfileForm(profile) {
  const length = (value) => typeof value === "string" ? value.trim().length : 0
  if (profile.age !== null && profile.age !== undefined && profile.age !== "") {
    if (!Number.isSafeInteger(profile.age) || profile.age < 0 || profile.age > 120) {
      return { kind: "profile_validation", field: "age", messageKey: "invalidAge" }
    }
  }
  if (
    profile.annual_family_income !== null
    && profile.annual_family_income !== undefined
    && profile.annual_family_income !== ""
    && (!Number.isSafeInteger(profile.annual_family_income) || profile.annual_family_income < 0)
  ) {
    return { kind: "profile_validation", field: "annual_family_income", messageKey: "invalidIncome" }
  }
  if (length(profile.state) > 0 && (length(profile.state) < 2 || length(profile.state) > 100)) {
    return { kind: "profile_validation", field: "state", messageKey: "invalidState" }
  }
  if (length(profile.occupation) > 0 && length(profile.occupation) > 100) {
    return { kind: "profile_validation", field: "occupation", messageKey: "invalidOccupation" }
  }
  if (length(profile.education_level) > 0 && length(profile.education_level) > 100) {
    return { kind: "profile_validation", field: "education_level", messageKey: "invalidEducation" }
  }
  return null
}

export function localizedError(error, language) {
  if (error?.kind === "scheme_not_found") return t(language, "schemeNotFound")
  if (error?.kind === "profile_validation") {
    const field = t(language, fieldLabels[error.field] || "profile")
    return t(language, "fieldError", {
      field,
      message: t(language, error.messageKey)
    })
  }

  const response = error?.response
  const details = response?.data?.detail
  if (Array.isArray(details) && details.length) {
    const formatted = details.map((detail) => {
      const field = [...(detail.loc || [])].reverse().find((part) => fieldLabels[part])
      return localizedFieldError(field || "additional_attributes", detail.msg || "", language)
    })
    return [...new Set(formatted)].join(language === "te" ? "；" : "; ")
  }
  if (response?.status === 422) return t(language, "serverValidationError")
  if (response?.status) return t(language, "httpError", { status: response.status })
  return t(language, "networkError")
}

export function localizedState(value, language) {
  if (language !== "te") return value
  const key = localizedValues[String(value)]
  return key ? t(language, key) : value
}
