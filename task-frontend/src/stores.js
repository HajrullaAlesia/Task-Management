import { writable } from "svelte/store";

export const tasks = writable([]);

export const user = writable(null);

export const login = (userData) => {
  user.set(userData);
  localStorage.setItem("user", JSON.stringify(user));
};

export const logout = () => {
  user.set(null);
  localStorage.removeItem("user");
};

// during reload
const storedUser = localStorage.getItem("user");
if (storedUser && storedUser !== "undefined") {
  try {
    user.set(JSON.parse(storedUser));
  } catch (e) {
    console.error("Failed to parse user from localStorage:", e);
    localStorage.removeItem("user");
  }
}
