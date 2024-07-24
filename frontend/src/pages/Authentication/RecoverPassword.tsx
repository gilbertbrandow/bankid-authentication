import { Label } from "@radix-ui/react-label";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { useTranslation } from "react-i18next";

const RecoverPassword = () => {
  const { t } = useTranslation();

  return (
    <div className="mx-auto grid w-[400px] gap-4">
      <div className="grid gap-4">
        <div className="grid gap-2">
          <Label htmlFor="email">{t("Email")}</Label>
          <Input id="email" type="email" placeholder="m@example.com" required />
        </div>
        <Button type="submit" variant="outline" className="w-full">
          {t("Send link to reset password")}
        </Button>
      </div>
    </div>
  );
};

export default RecoverPassword;
