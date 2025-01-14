import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

// Attach token in request headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
