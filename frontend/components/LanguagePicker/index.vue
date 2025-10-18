<script setup>
import { useI18n } from "vue-i18n";

const i18n = useI18n();
const items = ref(["Backlog", "Todo", "In Progress", "Done"]);
const value = ref("Backlog");

const metadata = computed(() => {
  if (i18n.locale.value === "ru") {
    return {
      title: "Dastan 16 Pro Max",
      description: "",
      keywords: "",
      robots: "index, follow",
    };
  } else if (i18n.locale.value === "kz") {
    return {
      title: "Dastan 16 Pro Max",
      description: "",
      keywords: "",
      language: "kz",
      robots: "index, follow",
    };
  } else {
    return {
      title: "Dastan 16 Pro Max",
      description: "",
      keywords: "",
      language: "en",
      robots: "index, follow",
    };
  }
});
const langs = [
  {
    id: "KZ",
    value: "kz",
    name: "Қазақша",
  },
  {
    id: "RU",
    value: "ru",
    name: "Русский",
  },
  {
    id: "EN",
    value: "en",
    name: "English",
  },
];

watch(
  () => i18n.locale.value,
  (locale) => {
    document.documentElement.lang = locale;
    useCookie("locale").value = locale;

    useHead({
      title: metadata.value.title,
      meta: [
        { name: "description", content: metadata.value.description },
        { name: "keywords", content: metadata.value.keywords },
        { name: "language", content: metadata.value.language },
        { name: "robots", content: metadata.value.robots },
      ],
    });
  }
);
</script>

<template>
  <USelectMenu
    v-model="$i18n.locale"
    :items="langs"
    value-attribute="value"
    option-attribute="id"
    size="lg"
    :ui-menu="{
      width: 'w-32',
      padding: 'px-2 py-2',
      ring: 'ring-black',
    }"
  >
    <template #default>
      <UButton color="black" variant="outline" :label="$i18n.locale" />
    </template>
    <template #option="{ option: language }">
      <p>{{ language.name }}</p>
    </template>
  </USelectMenu>
</template>
