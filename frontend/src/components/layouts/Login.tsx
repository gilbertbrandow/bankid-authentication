import React, { ReactNode, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Avatar, AvatarImage, AvatarFallback } from "../ui/avatar";
import { Outlet } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import Logo from "../icons/Logo";
import { Button } from "../ui/button";
import { ThemeToggle } from "../ui/theme-toggle";
import { LanguageSwitcher } from "../ui/language-switcher";
import { useTranslation } from "react-i18next";
import { checkTokenValidity } from "../../lib/api";
import SystemStatusBadge from "../ui/SystemStatusBadge";

interface LoginLayoutProps {
  children?: ReactNode;
}

const LoginLayout: React.FC<LoginLayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();

  useEffect(() => {
    const verifyToken = async () => {
      const isValid = await checkTokenValidity();
      if (isValid) {
        navigate("/permissions");
      }
    };

    verifyToken();
  }, [navigate]);

  return (
    <div className="flex h-screen">
      <div className="relative w-2/5 h-full flex items-center justify-center py-12">
        <header className="absolute top-0 w-full flex justify-between items-center pr-4 pl-4 pt-4">
          <Button
            variant="ghost"
            className="py-8"
            onClick={() => navigate("login")}
          >
            <Logo color="--primary" size={32} />
          </Button>
          <div className="flex items-right gap-2">
            {location.pathname !== "/login" && (
              <Button
                variant="ghost"
                className="pl-2 pr-2 flex items-center gap-1"
                onClick={() => navigate(-1)}
              >
                <ArrowLeft className="h-4 w-4" />
                {t("Back")}
              </Button>
            )}
            <LanguageSwitcher />
            <ThemeToggle />
          </div>
        </header>
        <Outlet />
        <footer className="absolute bottom-0 w-full text-sm text-muted-foreground pb-8 px-6">
          <hr
            className="border-1 mb-3"
            style={{ borderColor: "hsl(var(--border))" }}
          />
          <div className="flex justify-between items-center">
          <span>
              {" "}
              {t("Copyright")} © {new Date().getFullYear()}{" | "}
            <Button
              variant="link"
              className="font-normal text-muted-foreground text-sm p-0 mt-0"
              onClick={() => navigate("login-support")}
            >
              {t("Support")}
            </Button>
            </span>
            <SystemStatusBadge colorName="--status-green" message="All systems operational"/>
          </div>
        </footer>
      </div>
      <div className="relative w-3/5 h-full p-4">
        <video
          src="/painting.mp4"
          autoPlay
          loop
          muted
          className="object-cover w-full h-full rounded-lg"
        />
        <div className="absolute bottom-8 left-8 bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg text-white pl-2 pr-4 py-2 rounded-lg flex items-center gap-2">
          <Avatar className="h-8 w-8">
            <AvatarImage src="/yaroslav-shuraev.jpeg" alt="Yaroslav Shuraev" />
            <AvatarFallback>YS</AvatarFallback>
          </Avatar>
          <span>
            {t("Video by")}{" "}
            <a
              target="_blank"
              href="https://www.pexels.com/@yaroslav-shuraev/"
              className="underline"
            >
              Yaroslav Sharaev
            </a>
          </span>
        </div>
      </div>
    </div>
  );
};

export default LoginLayout;
