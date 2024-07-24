import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginLayout from "./components/layouts/Login";
import EmailLogin from "./pages/Authentication/EmailLogin";
import RecoverPassword from "./pages/Authentication/RecoverPassword";
import Login from "./pages/Authentication/Login";
import BankIDLogin from "./pages/Authentication/BankIDLogin";
import BankIDSameDeviceLogin from "./pages/Authentication/BankIDSameDeviceLogin";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginLayout />}>
          <Route path="login" element={<Login />} />
          <Route path="email-login" element={<EmailLogin />} />
          <Route path="bankid-login" element={<BankIDLogin />} />
          <Route path="bankid-same-device-login" element={<BankIDSameDeviceLogin />} />
          <Route path="recover-password" element={<RecoverPassword />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
