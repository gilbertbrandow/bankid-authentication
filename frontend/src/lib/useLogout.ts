import { useApiRequest } from "./api";
import { clearTokens } from "./auth";
import { useNavigate } from "react-router-dom";

export const useLogout = () => {
  const apiRequest = useApiRequest();
  const navigate = useNavigate();

  const logout = async () => {
    try {
      await apiRequest("authentication/logout/", {
        method: "POST",
      });
      clearTokens();
      navigate("/login");
    } catch (error: any) {
      console.error(error);
    }
  };

  return logout;
};
