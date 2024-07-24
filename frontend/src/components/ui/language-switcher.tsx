import { useTranslation } from "react-i18next";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "./dropdown-menu";
import { Button } from "../../components/ui/button";
import Flag from "../icons/Flag";

export function LanguageSwitcher() {
  const { i18n, t } = useTranslation();

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };

  const currentLang = i18n.language === "sv" ? "sv" : "en";

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          className="p-2 flex items-center gap-2 hover:cursor-pointer"
        >
          <Flag country={currentLang} className="w-6 h-6" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem
          onClick={() => changeLanguage("en")}
          className="hover:cursor-pointer"
        >
          <Flag country="en" className="w-6 h-6 mr-2" />
          {t("English")}
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() => changeLanguage("sv")}
          className="hover:cursor-pointer"
        >
          <Flag country="sv" className="w-6 h-6 mr-2" />
          {t("Swedish")}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
