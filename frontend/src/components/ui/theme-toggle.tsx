import { Sun } from "lucide-react";
import { Button } from "./button";
import { useTheme } from "../theme-provider";
import MoonIcon from "../icons/MoonIcon";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  return (
    <Button variant="ghost" size="icon" onClick={toggleTheme}>
      {theme === "light" ? (
        <Sun className="h-[1.5rem] w-[1.5rem]" />
      ) : (
        <MoonIcon size={1.5} className="transition-all" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}