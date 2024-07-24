import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginLayout from "./components/layouts/Login";
import EmailLogin from "./pages/EmailLogin";
import Login from "./pages/Login";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginLayout />}>
          <Route path="login" element={<Login />} />
          <Route path="email-login" element={<EmailLogin />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
