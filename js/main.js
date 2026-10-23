import { pick, poolFor, fillerStrip, excludedTags } from "./picker.js";
import { Reel, artFor, setBadges } from "./reel.js";
import { loadSettings, saveSettings } from "./settings.js";

const STOP_TIMES = [1500, 2000, 2500, 3000];
const NUMBER_WORDS = ["", "one", "both", "all three", "all four", "all five", "all six"];

const $ = (sel, root = document) => root.querySelector(sel);

const mixButton = $("#mix");
const mixHint = $("#mix-hint");
const prompt = $("#prompt");
const announcer = $("#announcer");
const settingsDialog = $("#settings");

let deck = [];
let wheels = [];
let reels = {};
let current = {};
const locked = new Set();
let options = [];
let storageKey;
let settings = {};
let spinning = false;

// --- Sound (Web Audio, generated, no files) -----------------------------------

let audio;
function tone(freq, duration, volume = 0.05, type = "sine") {
  if (!settings.sound) return;
  try {
    audio ??= new AudioContext();
    const osc = audio.createOscillator();
    const gain = audio.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(volume, audio.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + duration);
    osc.connect(gain).connect(audio.destination);
    osc.start();
    osc.stop(audio.currentTime + duration);
  } catch {
    // Audio not available; carry on silently.
  }
}
const tick = () => tone(900, 0.03, 0.02, "triangle");
const chime = (i) => tone([523, 659, 784, 1047][i] ?? 1047, 0.35, 0.06);

// --- Setup --------------------------------------------------------------------

async function init() {
  const data = await fetch("data/ingredients.json").then((r) => r.json());
  deck = data.ingredients;
  wheels = data.wheels;
  options = data.options ?? [];
  storageKey = data.storageKey;
  settings = loadSettings(storageKey);
  setBadges(data.badges);

  buildCards();
  prompt.textContent = promptText();

  current = pick(deck, wheels, locked, {}, filter());
  for (const wheel of wheels) reels[wheel.id].show(current[wheel.id]);

  mixButton.addEventListener("click", mix);
  document.addEventListener("keydown", (e) => {
    if (e.code !== "Space" || e.repeat || settingsDialog.open) return;
    if (e.target.closest?.("button, input, a, dialog")) return; // let focused controls handle it
    e.preventDefault();
    mix();
  });

  setupSettings();
  updateMixState();
}

function buildCards() {
  const container = $("#cards");
  const template = $("#card-template");
  container.style.setProperty("--card-count", wheels.length);
  for (const wheel of wheels) {
    const card = template.content.firstElementChild.cloneNode(true);
    card.dataset.wheel = wheel.id;
    card.setAttribute("aria-labelledby", `label-${wheel.id}`);
    const heading = $("h2", card);
    heading.id = `label-${wheel.id}`;
    heading.textContent = wheel.label;
    const lock = $(".lock", card);
    lock.setAttribute("aria-label", `Lock ${wheel.label}`);
    lock.addEventListener("click", () => toggleLock(wheel.id, card, lock));
    container.append(card);
    reels[wheel.id] = new Reel($(".reel", card));
  }
}

/** Which ingredients are in play, given the deck's options and the viewer's settings. */
function filter() {
  return { excludeTags: excludedTags(options, settings) };
}

function promptText() {
  const all = NUMBER_WORDS[wheels.length] ?? "all of them";
  return `Pitch a project that uses ${all}!`;
}

function toggleLock(wheelId, card, lockButton) {
  if (spinning) return;
  const isLocked = !locked.has(wheelId);
  isLocked ? locked.add(wheelId) : locked.delete(wheelId);
  card.classList.toggle("locked", isLocked);
  lockButton.setAttribute("aria-pressed", String(isLocked));
  const label = wheels.find((w) => w.id === wheelId).label;
  lockButton.setAttribute("aria-label", `${isLocked ? "Unlock" : "Lock"} ${label}`);
  updateMixState();
}

function updateMixState() {
  const allLocked = locked.size === wheels.length;
  mixButton.disabled = spinning || allLocked;
  mixHint.hidden = !allLocked;
}

// --- Mixing -------------------------------------------------------------------

async function mix() {
  if (spinning || locked.size === wheels.length) return;
  spinning = true;
  updateMixState();
  prompt.classList.remove("show");
  announcer.textContent = "";
  document.body.classList.add("is-spinning");

  const next = pick(deck, wheels, locked, current, filter());
  const toSpin = wheels.filter((w) => !locked.has(w.id));

  await Promise.all(
    toSpin.map((wheel, i) => {
      const pool = poolFor(deck, wheel.id, filter());
      const duration = STOP_TIMES[i] ?? STOP_TIMES.at(-1);
      const length = Math.round(duration / 80);
      return reels[wheel.id]
        .spin(next[wheel.id], fillerStrip(pool, length), duration, i === 0 ? tick : () => {})
        .then(() => chime(i));
    })
  );

  current = next;
  spinning = false;
  document.body.classList.remove("is-spinning");
  updateMixState();
  prompt.classList.add("show");
  announcer.textContent =
    wheels.map((w) => `${w.label}: ${current[w.id].name}.`).join(" ") +
    " " + promptText();
}

// --- Settings -----------------------------------------------------------------

function setupSettings() {
  const soundToggle = $("#opt-sound");
  soundToggle.checked = settings.sound;

  // One switch per deck option (e.g. "Include AI ingredients"), above the sound switch.
  for (const opt of options) {
    const label = document.createElement("label");
    label.className = "toggle";
    label.innerHTML = `
      <input type="checkbox">
      <span class="switch" aria-hidden="true"></span>
      <span><strong></strong><br><small></small></span>`;
    $("strong", label).textContent = opt.label;
    $("small", label).textContent = opt.hint ?? "";
    const input = $("input", label);
    input.checked = settings[opt.id] ?? opt.default ?? false;
    input.addEventListener("change", () => {
      settings[opt.id] = input.checked;
      saveSettings(settings, storageKey);
      replaceExcluded();
      renderDeck();
    });
    soundToggle.closest(".toggle").before(label);
  }

  $("#open-settings").addEventListener("click", () => {
    renderDeck();
    settingsDialog.showModal();
  });
  $("#close-settings").addEventListener("click", () => settingsDialog.close());
  settingsDialog.addEventListener("click", (e) => {
    if (e.target === settingsDialog) settingsDialog.close(); // click on backdrop
  });

  soundToggle.addEventListener("change", () => {
    settings.sound = soundToggle.checked;
    saveSettings(settings, storageKey);
    if (settings.sound) chime(0);
  });
}

/** After an option changes, swap out any card showing an ingredient that's now left out. */
function replaceExcluded() {
  if (spinning) return; // the next mix will use the new setting
  const excluded = filter().excludeTags;
  const isOut = (item) => (item.tags ?? []).some((tag) => excluded.includes(tag));
  const keep = new Set(wheels.filter((w) => !isOut(current[w.id])).map((w) => w.id));
  if (keep.size === wheels.length) return;
  const next = pick(deck, wheels, keep, current, filter());
  for (const wheel of wheels) {
    if (keep.has(wheel.id)) continue;
    reels[wheel.id].show(next[wheel.id]);
  }
  current = next;
}

function renderDeck() {
  const container = $("#deck");
  const excluded = filter().excludeTags;
  container.replaceChildren(
    ...wheels.map((wheel) => {
      const section = document.createElement("section");
      section.className = "deck-group";
      section.dataset.wheel = wheel.id;
      const heading = document.createElement("h3");
      heading.textContent = wheel.label;
      const list = document.createElement("ul");
      for (const item of deck.filter((i) => i.wheel === wheel.id)) {
        const li = document.createElement("li");
        const off = (item.tags ?? []).some((tag) => excluded.includes(tag));
        li.className = off ? "off" : "";
        const name = document.createElement("span");
        name.textContent = item.name + (off ? " (off)" : "");
        li.append(artFor(item, "deck-img"), name);
        list.append(li);
      }
      section.append(heading, list);
      return section;
    })
  );
}

init();
