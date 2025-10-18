<script setup lang="ts"></script>

<template>
  <Header />
  <main class="w-full bg-white font-medium">
    <Suspense>
      <slot />
    </Suspense>
  </main>
  <Footer />
</template>
