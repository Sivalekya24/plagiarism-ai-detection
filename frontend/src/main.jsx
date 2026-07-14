import React from "react";
import ReactDOM from "react-dom/client";
import { Toaster } from "react-hot-toast";
import App from "./App.jsx";
import AdminApp from "./AdminApp.jsx";
import "./index.css";

const isAdminRoute = window.location.pathname.startsWith("/admin");

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Toaster
      position="bottom-center"
      toastOptions={{
        style: {
          background: "#f1f5f9",
          color: "#0f172a",
          fontSize: "14px",
          fontWeight: 500,
          borderRadius: "9999px",
          padding: "8px 16px",
        },
      }}
    />
    {isAdminRoute ? <AdminApp /> : <App />}
  </React.StrictMode>
);
