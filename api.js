import axios from "axios";

export const API_BASE = "http://127.0.0.1:8000/api";

export function getLogs() {
  return axios.get(`${API_BASE}/logs`);
}
