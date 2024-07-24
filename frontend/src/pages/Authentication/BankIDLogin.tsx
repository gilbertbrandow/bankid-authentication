import { Button } from "../../components/ui/button";
import { useNavigate } from "react-router-dom";
import BankIDLogo from "../../components/icons/BankIDLogo";
import { useTheme } from "../../components/theme-provider";
import { useTranslation } from "react-i18next";

const BankIDLogin = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const { t } = useTranslation();

  return (
    <div className="flex flex-col items-center justify-center h-full">
      <h1 className="text-3xl font-bold mb-2 text-center inline-flex items-center">
        {t("Scan")} (<BankIDLogo size={3.5} color="#000" />) {t("QR Code")}
      </h1>
      <div className="max-w-[320px]">
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/4/41/QR_Code_Example.svg"
          alt="BankID QR Code"
          style={{ filter: theme === "dark" ? "invert(1)" : "" }}
        />
      </div>
      <p className="mb-8 mt-4 text-sm text-muted-foreground text-center max-w-[260px]">
        Starta BankID-appen i din mobil och tryck på Skanna QR-kod. Rikta
        kameran mot QR-koden här ovanför.
      </p>
      <Button variant="ghost" onClick={() => navigate(-1)}>
        {t("Cancel authentication")}
      </Button>
    </div>
  );
};

export default BankIDLogin;
