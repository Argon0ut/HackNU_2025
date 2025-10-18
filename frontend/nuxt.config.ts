import tailwindcss from "@tailwindcss/vite";

// @ts-ignore
export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    '@nuxtjs/google-fonts',
    '@nuxtjs/i18n',
    '@pinia/nuxt',
    '@nuxt/image'
  ],
  devtools: { enabled: true },
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  css: ['~/assets/css/main.css'],
  i18n: {
    locales: [
      {
        code: 'en',
        file: 'en.json',  
        name: 'English'
      },
      {
        code: 'ru',
        file: 'ru.json', 
        name: 'Русский'
      },
      {
        code: 'kz',
        file: 'kz.json', 
        name: 'Қазақша'
      }
    ],
  
    lazy: true,
    langDir: 'locales', 
    defaultLocale: 'en'
  }
})