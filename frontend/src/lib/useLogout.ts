import { useApiRequest } from "./api";
import { clearTokens } from "./auth";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

export const useLogout = () => {
  const apiRequest = useApiRequest();
  const navigate = useNavigate();
  const { t } = useTranslation(); 

  const logout = async () => {
    try {
      await apiRequest("authentication/logout/", {
        method: "POST",
      });
      clearTokens();
      navigate("/login", {
        state: {
          message: t("You successfully logged out."),
        },
      });
    } catch (error: any) {
      console.error(error);
    }
  };

  return logout;
};
