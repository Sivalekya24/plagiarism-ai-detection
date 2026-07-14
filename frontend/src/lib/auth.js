/* =====================================================================
   Admin auth token storage.

   sessionStorage (not localStorage) on purpose: the token dies when the
   admin closes the tab/browser instead of sitting around indefinitely.
   This is UI convenience only — the real access control is the backend
   checking this token (as a Bearer header) on every /repository/* and
   /code/documents|statistics|document/* call. Never trust the frontend
   alone to gate the admin panel.
===================================================================== */

const TOKEN_KEY = "verity_admin_token";

export function getAdminToken() {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function setAdminToken(token) {
  sessionStorage.setItem(TOKEN_KEY, token);
}

export function clearAdminToken() {
  sessionStorage.removeItem(TOKEN_KEY);
}

export function isAdminAuthenticated() {
  return Boolean(getAdminToken());
}
