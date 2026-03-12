import { create } from "zustand";
import { API } from "../api/client";

type AuthState = {
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (payload: any) => Promise<void>;
  logout: () => void;
};

export const useAuth = create<AuthState>((set) => ({
  token: localStorage.getItem("token"),
  login: async (email, password) => {
    const form = new FormData();
    form.append("username", email);
    form.append("password", password);
    const { data } = await API.post("/auth/login", form);
    localStorage.setItem("token", data.access_token);
    set({ token: data.access_token });
  },
  register: async (payload) => {
    const { data } = await API.post("/auth/register", payload);
    localStorage.setItem("token", data.access_token);
    set({ token: data.access_token });
  },
  logout: () => {
    localStorage.removeItem("token");
    set({ token: null });
  }
}));