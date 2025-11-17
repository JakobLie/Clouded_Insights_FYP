"use client";

import { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext(null);
export const useAuth = () => useContext(AuthContext);

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // { id, name, email }

  // Rehydrate from sessionStorage (simple prototype persistence)
  useEffect(() => {
    const raw = sessionStorage.getItem("user");
    if (raw) setUser(JSON.parse(raw));
  }, []);

  useEffect(() => {
    if (user) sessionStorage.setItem("user", JSON.stringify(user));
    else sessionStorage.removeItem("user");
  }, [user]);

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, setUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
