import { useTranslation } from "react-i18next";
import { useNavigate, NavigateFunction } from "react-router-dom";
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from "./auth";

const BASE_URL = "http://localhost:8000/api/";

async function apiRequest(
  endpoint: string,
  options: RequestInit = {},
  navigate: NavigateFunction,
  t: (key: string) => string
) {
  const url = `${BASE_URL}${endpoint}`;
  const accessToken = getAccessToken();

  const fetchWithToken = async (token?: string | null) => {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    return await fetch(url, {
      ...options,
      headers,
      credentials: "include",
    });
  };

  let response = await fetchWithToken(accessToken);

  if (response.status === 401) {
    const refreshToken = getRefreshToken();
    if (refreshToken) {
      try {
        const refreshResponse = await fetch(
          `${BASE_URL}authentication/refresh/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ refresh_token: refreshToken }),
            credentials: "include",
          }
        );

        if (!refreshResponse.ok) {
          throw new Error("Failed to refresh token");
        }

        const refreshData = await refreshResponse.json();
        setTokens(refreshData.access_token, refreshToken);
        response = await fetchWithToken(refreshData.access_token);
      } catch (refreshError) {
        clearTokens();
        navigate("/login");
        throw new Error(t("Session expired. Please log in again."));
      }
    } else {
      clearTokens();
      navigate("/login");
      throw new Error(t("Session expired. Please log in again."));
    }
  }

  const text = await response.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(t("Something went wrong."));
  }

  if (!response.ok) {
    const errorMessage = data.detail || t("Something went wrong.");
    throw new Error(errorMessage);
  }

  return data;
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

export function useApiRequest() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return async function (
    endpoint: string,
    options: RequestInit = {}
  ) {
    return await apiRequest(endpoint, options, navigate, t);
  };
}
