<script setup lang="ts">
import { useI18n } from "vue-i18n";

const i18n = useI18n();

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
    value: "kz",
    label: "kz",
  },
  {
    value: "ru",
    label: "ru",
  },
  {
    value: "en",
    label: "en",
  },
];

// Set initial language on client side only
onMounted(() => {
  if (document) {
    document.documentElement.lang = i18n.locale.value;
  }
});

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
  <div>
    <USelect
      v-model="$i18n.locale"
      :items="langs"
      value-attribute="id"
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
    </USelect>

    {{ $t("welcome") }}
  </div>
</template>
