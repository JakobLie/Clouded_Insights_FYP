"use client";
import { createContext, useContext, useState } from "react";

const SetupContext = createContext(null);

export function SetupProvider({ children }) {
  const [salesTarget, setSalesTarget] = useState(null);
  const [budget, setBudget] = useState(null);

  const value = { salesTarget, setSalesTarget, budget, setBudget };
  return <SetupContext.Provider value={value}>{children}</SetupContext.Provider>;
}

export function useSetup() {
  const context = useContext(SetupContext);
  if (!context) throw new Error("useSetup must be used within <SetupProvider>");
  return context;
}
