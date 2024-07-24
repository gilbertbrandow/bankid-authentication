const BASE_URL = 'http://localhost:8000/api/';

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const url = `${BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw {
        status: response.status,
        message: errorData.detail || 'An error occurred',
      };
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
}
