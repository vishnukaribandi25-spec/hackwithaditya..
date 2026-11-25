import React from "react"
import { Navigate, Route, Routes } from "react-router-dom"
import Header from "./components/Header"
import LandingPage from "./pages/LandingPage"
import ProfilePage from "./pages/ProfilePage"
import ResultsPage from "./pages/ResultsPage"
import SchemeDetailPage from "./pages/SchemeDetailPage"

export default function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/schemes" element={<ResultsPage />} />
        <Route path="/schemes/:id" element={<SchemeDetailPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  )
}
