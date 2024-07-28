import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./app/globals.css";
import { I18nextProvider } from 'react-i18next';
import i18n from "./i18n";
import { AuthProvider } from "./context/AuthContext";

const rootElement = document.getElementById("root");
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    //<React.StrictMode> I removed this so that development would be same as production, toaster works differently otherwise.
      <I18nextProvider i18n={i18n}>
        <AuthProvider>
          <App />
        </AuthProvider>
      </I18nextProvider>
    //</React.StrictMode>
  );
}