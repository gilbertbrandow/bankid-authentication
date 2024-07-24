import BankIDLogo from "../../components/icons/BankIDLogo";
import { Button } from "../../components/ui/button";
import { useNavigate } from "react-router-dom";
import { LockOpen } from "lucide-react";
import { useTheme } from "../../components/theme-provider";
import { useTranslation } from "react-i18next";

const Login = () => {
  const navigate = useNavigate();

  const { t } = useTranslation();
  const { theme } = useTheme();

  const isDarkMode = theme === "dark";
  const buttonBgColor = isDarkMode ? "bg-primary" : "bg-[#193E4F]";
  const logoColor = isDarkMode ? "#193E4F" : "#ffffff";


  return (
    <div className="mx-auto grid w-[400px] gap-4">
      <h1 className="text-3xl font-bold mb-4 text-center">
        {t("Sign in to")} Auth
        <span className="align-super text-sm"> ©</span>
      </h1>
      <Button
        className={`w-full flex items-center gap-2 justify-center ${buttonBgColor}`}
        onClick={() => navigate("/bankid-login")}
      >
        <BankIDLogo color={logoColor} size={2} />
        {t("Login with mobile BankID")}
      </Button>
      <Button
        variant="outline"
        className="w-full items-center gap-2 justify-center"
        onClick={() => navigate("/bankid-same-device-login")}
      >
        <BankIDLogo color="#000" size={2} />
        {t("Login with BankID on this device")}
      </Button>
      <Button
        variant="outline"
        className="w-full"
        onClick={() => navigate("/email-login")}
      >
        <LockOpen className="h-4 w-4 mr-4" />
        {t("Login with Email & Password")}
      </Button>
    </div>
  );
};

export default Login;
