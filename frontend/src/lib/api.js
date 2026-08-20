const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const TOKEN_KEY = "viewcast_token";

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

async function parseErrorDetail(response) {
  try {
    const body = await response.json();
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail)) {
      return body.detail.map((d) => d.msg).join(", ");
    }
  } catch {
    // response wasn't JSON — fall through to the generic message
  }
  return `Request failed (${response.status})`;
}

/**
 * Core fetch wrapper: attaches the bearer token, and throws ApiError with a
 * readable message on non-2xx responses so callers can just `try { } catch`.
 */
async function request(path, { method = "GET", json, form, auth = true } = {}) {
  const headers = {};
  const init = { method, headers };

  if (json !== undefined) {
    headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(json);
  } else if (form !== undefined) {
    init.body = form; // FormData — let the browser set the multipart boundary
  }

  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${path}`, init);

  if (!response.ok) {
    const message = await parseErrorDetail(response);
    throw new ApiError(message, response.status);
  }

  if (response.status === 204) return null;
  return response.json();
}

// ---- Auth ---------------------------------------------------------------

export function signup({ fullName, email, password }) {
  return request("/auth/signup", {
    method: "POST",
    auth: false,
    json: { full_name: fullName, email, password },
  });
}

export function login({ email, password }) {
  // The backend's /auth/login is an OAuth2PasswordRequestForm endpoint, so it
  // wants x-www-form-urlencoded with a "username" field (we pass the email).
  const form = new URLSearchParams();
  form.set("username", email);
  form.set("password", password);
  return request("/auth/login", { method: "POST", auth: false, form });
}

export function me() {
  return request("/auth/me");
}

// ---- Dashboard ------------------------------------------------------------

export function getDashboardSummary() {
  return request("/dashboard/summary");
}

// ---- Predictions ----------------------------------------------------------

export function createPrediction(formData) {
  return request("/predictions", { method: "POST", form: formData });
}

export function listPredictions() {
  return request("/predictions");
}

export function getPrediction(id) {
  return request(`/predictions/${id}`);
}

export function deletePrediction(id) {
  return request(`/predictions/${id}`, { method: "DELETE" });
}

export function fileUrl(path) {
  if (!path) return null;
  return `${API_URL}${path}`;
}
