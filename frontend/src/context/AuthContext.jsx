import { createContext, useContext, useEffect, useState } from "react";
import * as api from "../lib/api";

const USER_KEY = "viewcast_user";

const AuthContext = createContext(null);

function loadStoredUser() {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(loadStoredUser);
  const [token, setTokenState] = useState(api.getToken);

  function persist(nextToken, nextUser) {
    api.setToken(nextToken);
    if (nextUser) localStorage.setItem(USER_KEY, JSON.stringify(nextUser));
    else localStorage.removeItem(USER_KEY);
    setTokenState(nextToken);
    setUser(nextUser);
  }

  async function login(email, password) {
    const result = await api.login({ email, password });
    persist(result.access_token, result.user);
    return result.user;
  }

  async function signup(fullName, email, password) {
    const result = await api.signup({ fullName, email, password });
    persist(result.access_token, result.user);
    return result.user;
  }

  function logout() {
    persist(null, null);
  }

  function setUserData(nextUser) {
    localStorage.setItem(USER_KEY, JSON.stringify(nextUser));
    setUser(nextUser);
  }

  // Keep the stored user fresh (subscriber counts etc.) once per load.
  useEffect(() => {
    if (!token) return;
    api
      .me()
      .then((freshUser) => {
        localStorage.setItem(USER_KEY, JSON.stringify(freshUser));
        setUser(freshUser);
      })
      .catch(() => {
        // Token expired/invalid — drop the stale session.
        persist(null, null);
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const value = {
    user,
    token,
    isAuthenticated: Boolean(token),
    login,
    signup,
    logout,
    setUserData,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
