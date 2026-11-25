import React, { useEffect } from "react"
import { Navigate, Route, Routes } from "react-router-dom"
import Header from "./components/Header"
import LandingPage from "./pages/LandingPage"
import ProfilePage from "./pages/ProfilePage"
import ResultsPage from "./pages/ResultsPage"
import SchemeCatalogPage from "./pages/SchemeCatalogPage"
import SchemeDetailPage from "./pages/SchemeDetailPage"
import { useApp } from "./context/AppContext"
import { t } from "./i18n"

export default function App() {
  const { language } = useApp()

  useEffect(() => {
    document.title = t(language, "documentTitle")
  }, [language])

  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/schemes" element={<ResultsPage />} />
        <Route path="/catalog" element={<SchemeCatalogPage />} />
        <Route path="/schemes/:id" element={<SchemeDetailPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  )
}
