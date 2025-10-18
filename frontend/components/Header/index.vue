<script setup lang="ts"></script>

<template>
  <section class="w-full bg-white !py-4 lg:!py-6">
    <nav class="flex w-full items-center justify-between">
      <NuxtLink to="/#main-section">
        <!-- <img src="/public/header.svg" alt="logo" class="w-[133px]" /> -->
      </NuxtLink>

      <div class="flex items-center gap-2">
        <UButton
          icon="i-heroicons-arrow-right"
          variant="outline"
          color="black"
          trailing
          :label="$t('landing.hero.cta')"
          target="_blank"
        />
        <LanguagePicker />
      </div>
    </nav>
  </section>
</template>
