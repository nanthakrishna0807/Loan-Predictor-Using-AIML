import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000/api",
  withCredentials: true,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token") || localStorage.getItem("loan_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const login = async (data) => {
  const res = await api.post("/auth/login", data);
  if (res.data && res.data.data && res.data.data.token) {
    localStorage.setItem("token", res.data.data.token);
    localStorage.setItem("loan_token", res.data.data.token);
  }
  return res.data;
};

export const register = async (data) => {
  const res = await api.post("/auth/register", data);
  if (res.data && res.data.data && res.data.data.token) {
    localStorage.setItem("token", res.data.data.token);
    localStorage.setItem("loan_token", res.data.data.token);
  }
  return res.data;
};

export const predictLoan = async (formData) => {
  const res = await api.post("/loan/predict", formData);
  return res.data;
};

export const calculateEMI = async (data) => {
  const res = await api.post("/loan/calculate-emi", data);
  return res.data;
};

export const getHistory = async () => {
  const res = await api.get("/loan/history");
  return res.data;
};

export default api;
