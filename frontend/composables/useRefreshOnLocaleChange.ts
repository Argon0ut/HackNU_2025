import { useI18n } from "vue-i18n";

export async function useRefreshOnLocaleChange(refresh: () => void) {
  const i18n = useI18n();

  watch(i18n.locale, () => nextTick(refresh));
}
