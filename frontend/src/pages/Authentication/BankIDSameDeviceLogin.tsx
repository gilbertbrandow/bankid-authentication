import { Button } from "../../components/ui/button";
import { useNavigate } from "react-router-dom";
import BankIDLogo from "../../components/icons/BankIDLogo";
import Spinner from "../../components/icons/Spinner";
import { useTranslation } from "react-i18next";

const BankIDSameDeviceLogin = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  return (
    <div className="flex flex-col items-center justify-center h-full">
      <h1 className="text-3xl font-bold mb-8 text-center inline-flex items-center">
        {t("Searching for")} (<BankIDLogo size={3.5} color="#000" />
        )...
      </h1>
      <Spinner size={3} />
      <Button className="mt-8" variant="ghost" onClick={() => navigate(-1)}>
        {t("Cancel authentication")}
      </Button>
    </div>
  );
};

export default BankIDSameDeviceLogin;
