import React, { createContext, useContext, useMemo, useState } from "react"

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [language, setLanguage] = useState("en")
  const [profile, setProfile] = useState(null)
  const [matches, setMatches] = useState([])

  const value = useMemo(
    () => ({ language, setLanguage, profile, setProfile, matches, setMatches }),
    [language, profile, matches]
  )

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  return useContext(AppContext)
}
