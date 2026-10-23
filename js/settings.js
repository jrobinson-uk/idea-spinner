// Per-viewer preferences, saved in localStorage when it's available.
// Each deck can use its own key so the two sites keep separate settings.

const DEFAULT_KEY = "idea-spinner:settings";
const DEFAULTS = { sound: false };

export function loadSettings(key = DEFAULT_KEY) {
  try {
    const saved = JSON.parse(localStorage.getItem(key) || "{}");
    return { ...DEFAULTS, ...saved };
  } catch {
    return { ...DEFAULTS };
  }
}

export function saveSettings(settings, key = DEFAULT_KEY) {
  try {
    localStorage.setItem(key, JSON.stringify(settings));
  } catch {
    // Private mode or blocked storage: settings just won't persist.
  }
}
