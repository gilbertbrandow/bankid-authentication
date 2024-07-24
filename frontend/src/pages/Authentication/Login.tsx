import BankIDLogo from "../../components/icons/BankIDLogo";
import { Button } from "../../components/ui/button";
import { useNavigate } from "react-router-dom";
import { LockOpen } from "lucide-react";

const Login = () => {
  const navigate = useNavigate();

  return (
    <div className="mx-auto grid w-[400px] gap-4">
      <h1 className="text-3xl font-bold mb-4 text-center">
        Sign in to Waves
        <span className="align-super text-sm"> ©</span>
      </h1>
      <Button
        className="w-full bg-[#193E4F] text-white flex items-center gap-2 justify-center"
        onClick={() => navigate("/bankid-login")}
      >
        <BankIDLogo color="#ffffff" size={2} />
        Login with mobile BankID
      </Button>
      <Button
        variant="outline"
        className="w-full items-center gap-2 justify-center"
        onClick={() => navigate("/bankid-same-device-login")}
      >
        <BankIDLogo color="#000" size={2} />
        Login with BankID on this device
      </Button>
      <Button
        variant="outline"
        className="w-full"
        onClick={() => navigate("/email-login")}
      >
        <LockOpen className="h-4 w-4 mr-4" />
        Login with Email & Password
      </Button>
    </div>
  );
};

export default Login;
