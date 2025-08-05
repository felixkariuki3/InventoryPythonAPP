import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000", // or wherever your FastAPI backend is running
});

export const startProduction = (orderId) =>
  API.post("/production/start", { order_id: orderId });

export const completeProduction = (orderId, completed_quantity) =>
  API.post("/production/complete", { order_id: orderId, completed_quantity });

