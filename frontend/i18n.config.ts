export const messages = {
  en: {},
  kz: {},
  ru: {}
};

export default defineI18nConfig(() => ({
  globalInjection: true,
  legacy: false,
  locale: "en",
  fallbackLocale: "en",
  messages,
}));
