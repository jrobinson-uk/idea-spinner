import { pick, poolFor, fillerStrip } from "./picker.js";
import { Reel, imageFor } from "./reel.js";
import { loadSettings, saveSettings } from "./settings.js";

const STOP_TIMES = [1600, 2200, 2800];

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
let settings = loadSettings();
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
const chime = (i) => tone([523, 659, 784][i] ?? 784, 0.35, 0.06);

// --- Setup --------------------------------------------------------------------

async function init() {
  const data = await fetch("data/ingredients.json").then((r) => r.json());
  deck = data.ingredients;
  wheels = data.wheels;

  for (const wheel of wheels) {
    const card = $(`.card[data-wheel="${wheel.id}"]`);
    reels[wheel.id] = new Reel($(".reel", card));
    const lock = $(".lock", card);
    lock.addEventListener("click", () => toggleLock(wheel.id, card, lock));
  }

  current = pick(deck, wheels, locked, {}, settings);
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

  const next = pick(deck, wheels, locked, current, settings);
  const toSpin = wheels.filter((w) => !locked.has(w.id));

  await Promise.all(
    toSpin.map((wheel, i) => {
      const pool = poolFor(deck, wheel.id, settings);
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
    " Pitch a project that uses all three!";
}

// --- Settings -----------------------------------------------------------------

function setupSettings() {
  const aiToggle = $("#opt-ai");
  const soundToggle = $("#opt-sound");
  aiToggle.checked = settings.includeAI;
  soundToggle.checked = settings.sound;

  $("#open-settings").addEventListener("click", () => {
    renderDeck();
    settingsDialog.showModal();
  });
  $("#close-settings").addEventListener("click", () => settingsDialog.close());
  settingsDialog.addEventListener("click", (e) => {
    if (e.target === settingsDialog) settingsDialog.close(); // click on backdrop
  });

  aiToggle.addEventListener("change", () => {
    settings.includeAI = aiToggle.checked;
    saveSettings(settings);
    renderDeck();
  });
  soundToggle.addEventListener("change", () => {
    settings.sound = soundToggle.checked;
    saveSettings(settings);
    if (settings.sound) chime(0);
  });
}

function renderDeck() {
  const container = $("#deck");
  container.replaceChildren(
    ...wheels.map((wheel) => {
      const section = document.createElement("section");
      section.className = `deck-group deck-${wheel.id}`;
      const heading = document.createElement("h3");
      heading.textContent = wheel.label;
      const list = document.createElement("ul");
      for (const item of deck.filter((i) => i.wheel === wheel.id)) {
        const li = document.createElement("li");
        const off = item.tags.includes("ai") && !settings.includeAI;
        li.className = off ? "off" : "";
        li.innerHTML = `<img alt="" src="${imageFor(item)}"><span></span>`;
        li.querySelector("span").textContent = item.name + (off ? " (off)" : "");
        list.append(li);
      }
      section.append(heading, list);
      return section;
    })
  );
}

init();
