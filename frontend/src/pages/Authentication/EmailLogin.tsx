import { Label } from "@radix-ui/react-label";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

const EmailLogin = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  return (
    <div className="mx-auto grid w-[400px] gap-4">
      <div className="grid gap-4">
        <div className="grid gap-2">
          <Label htmlFor="email">{t("Email")}</Label>
          <Input id="email" type="email" placeholder="m@example.com" required />
        </div>
        <div className="grid gap-2">
          <div className="flex items-center">
            <Label htmlFor="password">{t("Password")}</Label>
            <Button
              variant="link"
              className="ml-auto pl-2 pr-0 text-muted-foreground hover:text-current flex items-center gap-2 inline-block text-xs underline"
              onClick={() => navigate("/recover-password")}
            >
              {t("Forgot your password?")}
            </Button>
          </div>
          <Input id="password" type="password" placeholder="*******" required />
        </div>
        <Button type="submit" className="w-full">
          {t("Login")}
        </Button>
      </div>
    </div>
  );
};

export default EmailLogin;
