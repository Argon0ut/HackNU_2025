import type { Specialization } from "~/types/specialists";

export function getLangValue(
  language: string,
  prefix: string = "name",
): string {
  switch (language) {
    case "ru":
      return `${prefix}_ru`;
    case "en":
      return `${prefix}_en`;
    default:
      return `${prefix}_kz`;
  }
}

export const useLocalizeProperty = () => {
  const { locale } = useI18n();
  const localizeProperty = (prefix: string): string => {
    return getLangValue(locale.value, prefix);
  };
  return { localizeProperty };
};

export const validatePhone = (phone: string) => {
  if (!phone.length) {
    return {
      valid: false,

      error: "This field is required.",
    };
  }

  if (
    !phone.match(/^[+][(]?[0-9]{1,3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,7}$/gm)
  ) {
    return {
      valid: false,
      error: "Please, enter a valid international phone number.",
    };
  }

  return { valid: true, error: null };
};

export const validateEmail = (email: string) => {
  if (!email.length) {
    return { valid: false, error: "This field is required" };
  }
  if (!email.match(/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/)) {
    return { valid: false, error: "Please, enter a valid email." };
  }
  return { valid: true, error: null };
};

export const getUserAgent = () => {
  return navigator.userAgent;
};
export const getLowestPrice = (specializations: any[]) => {
  const prices = specializations.map((spec) => parseFloat(spec.price));
  const lowestPriceNumber = Math.min(...prices);
  return lowestPriceNumber;
};
export function throttle<T extends (...args: any[]) => void>(
  func: T,
  wait: number,
): T {
  let lastCallTime: number | null = null;
  let timeoutId: ReturnType<typeof setTimeout> | null = null;

  return function (this: any, ...args: Parameters<T>) {
    const now = Date.now();

    if (lastCallTime === null || now - lastCallTime >= wait) {
      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }
      lastCallTime = now;
      func.apply(this, args);
    } else if (!timeoutId) {
      timeoutId = setTimeout(
        () => {
          lastCallTime = Date.now();
          timeoutId = null;
          func.apply(this, args);
        },
        wait - (now - lastCallTime),
      );
    }
  } as T;
}
