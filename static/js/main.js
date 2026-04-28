// Core API URL
const API_BASE = '/api';

// Utility for fetching JSON
async function fetchAPI(endpoint, options = {}) {
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, config);
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

// Show a simple toast/alert (Mock implementation for demo)
function showToast(message, type = 'success') {
  alert(`[${type.toUpperCase()}] ${message}`);
}
