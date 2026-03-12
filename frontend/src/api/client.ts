import axios from "axios";

// Cambia esta URL por la de tu backend en Render al desplegar
export const API = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000" });

API.interceptors.request.use(cfg => {
  const token = localStorage.getItem("token");
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});