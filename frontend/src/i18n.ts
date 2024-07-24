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
      loadPath: (lng: string) => lng === 'en' ? null : `/locales/translation.${lng}.json`,
    },
    fallbackLng: "en",
    debug: true,
    detection: {
      order: ["queryString", "cookie", "localStorage", "navigator", "htmlTag"],
      caches: ["cookie"],
    },
    interpolation: {
      escapeValue: false,
    },
    react: {
      useSuspense: false,
    },
  });

i18n.on('missingKey', function(lngs, namespace, key, res) {
  if (lngs[0] !== 'en') {
    console.warn(`Missing translation for key: ${key} in language: ${lngs[0]}`);
  }
});

export default i18n;
