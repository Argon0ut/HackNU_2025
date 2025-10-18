<script setup lang="ts">
import { useI18n } from "vue-i18n";

const i18n = useI18n();

const setLocaleFromStorage = () => {
  const locale = useCookie("locale").value;
  if (locale) {
    i18n.locale.value = locale;
  }
};

setLocaleFromStorage();
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
