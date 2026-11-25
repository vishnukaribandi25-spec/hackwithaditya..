import axios from "axios"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  timeout: 30000
})

export const health = () => api.get("/health")
export const listSchemes = () => api.get("/schemes")
export const getScheme = (id) => api.get(`/schemes/${id}`)
export const matchSchemes = (profile) => api.post("/eligibility/match", profile)
export const sendChat = (message, language, schemeContext) =>
  api.post("/chat", { message, language, scheme_context: schemeContext })
