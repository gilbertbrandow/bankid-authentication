import { useTranslation } from "react-i18next";
import { useNavigate, NavigateFunction } from "react-router-dom";
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from "./auth";

const BASE_URL = "http://localhost:8000/api/";

async function fetchWithHeaders(
  url: string | Request,
  token?: string | null,
  options: RequestInit = {}
) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    "X-CSRFToken": getCookie("csrftoken"),
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const fetchOptions: RequestInit = {
    ...options,
    headers,
    credentials: "include",
  };

  if (url instanceof Request) {
    return await fetch(url, fetchOptions);
  }

  return await fetch(url, fetchOptions);
}

function getCookie(name: string): string {
  let cookieValue = "";
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function refreshAccessToken(refreshToken: string): Promise<Response> {
  return await fetch(`${BASE_URL}authentication/refresh-token/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
    credentials: "include",
  });
}

export async function checkTokenValidity(): Promise<boolean> {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    clearTokens();
    return false;
  }

  try {
    const refreshResponse = await refreshAccessToken(refreshToken);

    if (!refreshResponse.ok) {
      clearTokens();
      return false;
    }

    const refreshData = await refreshResponse.json();
    setTokens(refreshData.access_token, refreshToken);
    return true;
  } catch (error) {
    clearTokens();
    return false;
  }
}

async function handle401(
  originalRequest: Request,
  navigate: NavigateFunction,
  t: (key: string) => string
): Promise<any> {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    return handleSessionExpired(navigate, t, null);
  }

  try {
    const refreshResponse = await refreshAccessToken(refreshToken);

    if (!refreshResponse.ok) {
      return handleSessionExpired(navigate, t, null);
    }

    const refreshData = await refreshResponse.json();

    setTokens(refreshData.access_token, refreshToken);

    const response = await fetchWithHeaders(
      originalRequest,
      getAccessToken(),
      {}
    );
    return await handleResponse(response, originalRequest, navigate, t);
  } catch (refreshError) {
    return handleSessionExpired(navigate, t, null);
  }
}

async function handle403(response: Response, t: (key: string) => string) {
  const errorData = await parseResponse(response, t);
  throw new Error(
    errorData.detail || t("You do not have permission to perform this action.")
  );
}

async function parseResponse(
  response: Response,
  t: (key: string) => string
): Promise<any> {
  const contentType = response.headers.get("content-type");

  if (!contentType) return;
  else if (contentType && contentType.includes("application/json")) {
    try {
      const text = await response.text();
      return text ? JSON.parse(text) : {};
    } catch (error) {
      throw new Error(t("Failed to parse JSON response"));
    }
  } else if (contentType && contentType.includes("image/png")) {
    try {
      const blob = await response.blob();
      return URL.createObjectURL(blob);
    } catch (error) {
      throw new Error("Failed to parse image response");
    }
  } else {
    throw new Error("Unsupported content type");
  }
}

async function handleResponse(
  response: Response,
  originalRequest: Request,
  navigate: NavigateFunction,
  t: (key: string) => string
): Promise<any> {
  if (response.ok) {
    return await parseResponse(response, t);
  }

  switch (response.status) {
    case 401:
      return await handle401(originalRequest, navigate, t);
    case 403:
      return await handle403(response, t);
    case 204:
      return;
    default:
      const errorData = await parseResponse(response, t);
      throw new Error(errorData.detail || t("Something went wrong."));
  }
}

function handleSessionExpired(
  navigate: NavigateFunction,
  t: (key: string) => string,
  errorMessage: string | null
): void {
  clearTokens();
  navigate("/login", {
    state: {
      error: errorMessage ?? t("Session expired. Please log in again."),
    },
  });
  return;
}

async function apiRequest(
  endpoint: string,
  options: RequestInit = {},
  navigate: NavigateFunction,
  t: (key: string) => string
) {
  const request = new Request(`${BASE_URL}${endpoint}`, options);
  const response = await fetchWithHeaders(request, getAccessToken(), options);
  return await handleResponse(response, request, navigate, t);
}

export function useApiRequest() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return async function (endpoint: string, options: RequestInit = {}) {
    return await apiRequest(endpoint, options, navigate, t);
  };
}
