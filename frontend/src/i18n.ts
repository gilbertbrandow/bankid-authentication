import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import HttpApi from "i18next-http-backend";

i18n
  .use(HttpApi)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    backend: {
      loadPath: (lng: string) =>
        lng === "en" ? undefined : `/locales/translation.${lng}.json`,
    },
    fallbackLng: "en",
    debug: false,
    detection: {
      order: ["queryString", "cookie", "localStorage", "navigator", "htmlTag"],
      caches: ["cookie"],
    },
    interpolation: {
      escapeValue: false,
    },
    react: {
      useSuspense: true,
    },
    nsSeparator: false,
    keySeparator: false,
    saveMissing: true,
    missingKeyHandler: (lng, ns, key, fallbackValue) => {
      if (i18n.language !== "en") {
        console.warn(`Missing translation for key: ${key} in language: ${i18n.language}`);
      }
    },
  });

export default i18n;
