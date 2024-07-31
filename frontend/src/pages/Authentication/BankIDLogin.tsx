import React, { useEffect, useState, useRef } from "react";
import { Button } from "../../components/ui/button";
import { useNavigate } from "react-router-dom";
import BankIDLogo from "../../components/icons/BankIDLogo";
import { useTheme } from "../../components/theme-provider";
import { useTranslation } from "react-i18next";
import { useApiRequest } from "../../lib/api";
import { useAuth } from "../../context/AuthContext";
import { AlertDestructive } from "../../components/ui/AlertDestructive";
import { AlertCircle } from "lucide-react";
import Spinner from "../../components/icons/Spinner";

const BankIDLogin = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const { t } = useTranslation();
  const apiRequest = useApiRequest();
  const { setAuthTokens } = useAuth();
  const [qrCode, setQrCode] = useState("/qr-code-placeholder.png");

  const [message, setMessage] = useState(
    t(
      "Launch the BankID-app on your phone and press scan QR-code. Point the camera to the QR-code above this message."
    )
  );

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const initiateBankID = async () => {
    setError("");
    setLoading(true);

    try {
      const response = await apiRequest("authentication/bankid/initiate/", {
        method: "POST",
      });

      fetchQrCode(response.orderRef);

      setLoading(false);

      let intervalId = setInterval(async () => {
        try {
          await pollAuthentication(response.orderRef);
          await fetchQrCode(response.orderRef);
        } catch (error: any) {
          setError(error.message);
          clearInterval(intervalId);
        }
      }, 1000);
    } catch (error: any) {
      setError(error.message);
    }
  };

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    initiateBankID();

    return () => clearInterval(intervalId);
  }, []);

  const fetchQrCode = async (orderRef: string) => {
    try {
      const response = await apiRequest(
        `authentication/bankid/qr/${orderRef}/`,
        {
          method: "GET",
        }
      );
      setQrCode(response);
    } catch (error: any) {
      setError(error.message);
    }
  };

  const pollAuthentication = async (orderRef: string) => {
    try {
      const response = await apiRequest(
        `authentication/bankid/poll/${orderRef}/`,
        {
          method: "GET",
        }
      );

      if (response.message === "Please start the BankID app.") return;
      if (!response.message) {
        setAuthTokens(response.access_token, response.refresh_token);
        navigate("/permissions");
      }

      setMessage(response.message);
    } catch (error: any) {
      setError(error.message);
      throw error;
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-full">
      <h1 className="text-3xl font-bold mb-2 text-center inline-flex items-center">
        {t("Scan")} (<BankIDLogo size={3.5} color="#000" />) {t("QR Code")}
      </h1>
      <div className="relative w-[300px]">
        <img
          src={qrCode}
          alt="BankID QR Code"
          style={{ filter: theme === "dark" ? "invert(1)" : "" }}
        />
        {(error || loading) && (
          <div className="absolute w-[100%] h-[100%] inset-0 flex flex-col items-center justify-center bg-opacity-80 backdrop-blur-sm" style={{ backgroundColor: 'var(--background)' }}>
            {error ? (
              <>
                <AlertCircle size={32} />
                <Button
                  variant="link"
                  onClick={initiateBankID}
                  className="mt-2 text-sm underline"
                >
                  {t("Try Again.")}
                </Button>
              </>
            ) : (
              loading && <Spinner size={2} />
            )}
          </div>
        )}
      </div>
      {error ? (
        <div className="max-w-[300px] mt-4 mb-2">
          <AlertDestructive title="Error" description={error} />
        </div>
      ) : (
        <p className="mb-8 mt-4 text-sm text-muted-foreground text-center max-w-[280px]">
          {message}
        </p>
      )}
      <Button variant="ghost" onClick={() => navigate(-1)}>
        {t("Cancel authentication")}
      </Button>
    </div>
  );
};

export default BankIDLogin;
