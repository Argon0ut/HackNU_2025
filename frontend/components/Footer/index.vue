<template>
  <footer
    class="bg-black px-[20px] pb-[24px] pt-[40px] text-white lg:px-[72px] lg:pb-[48px] lg:pt-[72px]"
  >
    <div class="mx-auto w-full max-w-[1280px]">
      <NuxtLink to="/#main-section">
        <!-- <img src="/public/footer.svg" alt="logo" class="w-[120px]" /> -->
      </NuxtLink>
      <p
        class="mt-2 text-lg font-light tracking-wider text-white lg:text-[22px]"
      >
        {{ $t("landing.hero.subtext") }}
      </p>

      <p class="mt-10 text-center text-[#4B5563]">
        {{ $t("landing.allrights") }}
      </p>
    </div>
  </footer>
</template>
