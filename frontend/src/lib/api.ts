// utils/api.ts
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from "./auth";
import { NavigateFunction } from "react-router-dom";

const BASE_URL = "http://localhost:8000/api/";

export async function apiRequest(
  endpoint: string,
  options: RequestInit = {},
  navigate?: NavigateFunction
) {
  const url = `${BASE_URL}${endpoint}`;
  const accessToken = getAccessToken();

  const fetchWithToken = async (token?: string | null) => {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    return await fetch(url, {
      ...options,
      headers,
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
            },
            body: JSON.stringify({ refresh_token: refreshToken }),
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
        if (navigate) {
          navigate("/login");
        }
        throw new Error("Session expired. Please log in again.");
      }
    } else {
      clearTokens();
      if (navigate) {
        navigate("/login");
      }
      throw new Error("Session expired. Please log in again.");
    }
  }

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  return await response.json();
}
