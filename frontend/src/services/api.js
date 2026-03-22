/**
 * api.js — Centralized API service layer for CommuteIQ frontend.
 */

const BASE_URL = 'http://localhost:5000/api';

function getToken() {
  return localStorage.getItem('commuteiq_token');
}

function authHeaders() {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function request(method, path, body = null) {
  const options = { method, headers: authHeaders() };
  if (body) options.body = JSON.stringify(body);

  let res;
  try {
    res = await fetch(`${BASE_URL}${path}`, options);
  } catch (err) {
    throw new Error(
      'Cannot reach backend. Make sure Flask is running:\n  cd backend\n  python app.py'
    );
  }

  const contentType = res.headers.get('content-type') || '';
  if (!contentType.includes('application/json')) {
    const text = await res.text();
    throw new Error(
      `Server error (${res.status}). Is Flask running on port 5000? ` +
      `Details: ${text.slice(0, 150)}`
    );
  }

  const json = await res.json();
  if (!res.ok) throw new Error(json.error || `HTTP ${res.status}`);
  return json;
}

export const authAPI = {
  signup: (username, email, password) =>
    request('POST', '/signup', { username, email, password }),
  login: (email, password) =>
    request('POST', '/login', { email, password }),
  me: () => request('GET', '/me'),
};

export const journeyAPI = {
  planJourney: (source, destination, time, preference, user_mode = 'normal') =>
    request('POST', '/plan_journey', { source, destination, time, preference, user_mode }),
  simulateAlert: (routes, disruption_type = null) =>
    request('POST', '/simulate_alert', { routes, disruption_type }),
  getExplanation: (selected_route, alternatives) =>
    request('POST', '/route_explanation', { selected_route, alternatives }),
  getHeatmap: () => request('GET', '/heatmap_data'),
};

export const costAPI = {
  getCostOptions: (source, destination, distance) =>
    request('POST', '/cost_options', { source, destination, distance }),
};

export const prefsAPI = {
  get: () => request('GET', '/user_preferences'),
  save: (data) => request('POST', '/user_preferences', data),
};