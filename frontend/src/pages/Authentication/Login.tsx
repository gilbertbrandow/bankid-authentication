import BankIDLogo from "../../components/icons/BankIDLogo";
import { Button } from "../../components/ui/button";
import SignUpDrawer from "../../components/SignUpDrawer";
import { useNavigate, useLocation } from "react-router-dom";
import { User } from "lucide-react";
import { useTheme } from "../../components/theme-provider";
import { useTranslation } from "react-i18next";
import { useEffect } from "react";
import { toast } from "sonner";

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const { theme } = useTheme();

  useEffect(() => {
    if (location.state?.error) {
      toast.error("Error", {
        description: location.state.error,
      });
      navigate(location.pathname, { replace: true, state: {} });
    } else if (location.state?.message) {
      toast.info(t("Message"), {
        description: location.state.message,
      });
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location, navigate]);

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
        <User className="h-5 w-5 mr-4" />
        {t("Login with Email & Password")}
      </Button>
      <span className="mt-2 text-xs flex justify-center items-center text-muted-foreground text-center">
        {t("Don't have an account?")}
        <SignUpDrawer />
      </span>
    </div>
  );
};

export default Login;
