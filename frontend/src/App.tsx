import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ThemeProvider } from "./components/theme-provider";
import LoginLayout from "./components/layouts/Login";
import EmailLogin from "./pages/Authentication/EmailLogin";
import RecoverPassword from "./pages/Authentication/RecoverPassword";
import Login from "./pages/Authentication/Login";
import BankIDLogin from "./pages/Authentication/BankIDLogin";
import BankIDSameDeviceLogin from "./pages/Authentication/BankIDSameDeviceLogin";
import DefaultLayout from "./components/layouts/Default";
import Permissions from "./pages/Permissions";
import { I18nextProvider } from "react-i18next";
import i18n from "./i18n";
import { Suspense } from "react";
import { Toaster } from "./components/ui/sonner";

const Loading = () => <div>Loading...</div>;

const App = () => {
  return (
    <ThemeProvider defaultTheme="light" storageKey="application-ui-theme">
      <I18nextProvider i18n={i18n}>
        <div vaul-drawer-wrapper="">
          <div className="relative flex min-h-screen flex-col bg-background">
            <Suspense fallback={<Loading />}>
              <Router>
                <Routes>
                  <Route element={<LoginLayout />}>
                    <Route path="login" element={<Login />} />
                    <Route path="email-login" element={<EmailLogin />} />
                    <Route path="bankid-login" element={<BankIDLogin />} />
                    <Route
                      path="bankid-same-device-login"
                      element={<BankIDSameDeviceLogin />}
                    />
                    <Route
                      path="recover-password"
                      element={<RecoverPassword />}
                    />
                  </Route>
                  <Route element={<DefaultLayout />}>
                    <Route path="permissions" element={<Permissions />} />
                  </Route>
                </Routes>
              </Router>
              <Toaster richColors />
            </Suspense>
          </div>
        </div>
      </I18nextProvider>
    </ThemeProvider>
  );
};

export default App;
