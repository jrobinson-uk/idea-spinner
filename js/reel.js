// One spinning card: a window with a vertical strip of tiles that scrolls and lands on a target.

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

export function imageFor(item) {
  return `img/ingredients/${item.id}.svg`;
}

function tile(item) {
  const el = document.createElement("div");
  el.className = "tile";
  el.innerHTML = `
    <img class="tile-img" alt="" draggable="false">
    <p class="tile-name"></p>
    <p class="tile-hint"></p>`;
  el.querySelector(".tile-img").src = imageFor(item);
  el.querySelector(".tile-name").textContent = item.name;
  el.querySelector(".tile-hint").textContent = item.hint;
  return el;
}

export class Reel {
  /** @param {HTMLElement} windowEl the clipping element that holds the strip */
  constructor(windowEl) {
    this.windowEl = windowEl;
    this.strip = windowEl.querySelector(".strip");
    this.item = null;
  }

  /** Show an item immediately, with no animation. */
  show(item) {
    this.item = item;
    this.strip.getAnimations().forEach((a) => a.cancel());
    this.strip.replaceChildren(tile(item));
    this.strip.style.transform = "";
  }

  /**
   * Scroll through `filler` and land on `target`.
   * @param {object} target ingredient to land on
   * @param {object[]} filler items to pass on the way
   * @param {number} duration ms
   * @param {function} onTick called each time a new tile passes (for sound)
   */
  async spin(target, filler, duration, onTick = () => {}) {
    if (reducedMotion.matches) return this.fade(target);

    const items = [this.item ?? filler[0], ...filler, target];
    this.strip.replaceChildren(...items.map(tile));
    this.windowEl.classList.add("spinning");
    this.windowEl.setAttribute("aria-hidden", "true");

    const n = items.length;
    const end = `translateY(${(-(n - 1) / n) * 100}%)`;
    const anim = this.strip.animate(
      [{ transform: "translateY(0)" }, { transform: end }],
      { duration, easing: "cubic-bezier(0.15, 0.6, 0.2, 1)", fill: "forwards" }
    );

    let last = 0;
    const watch = () => {
      if (anim.playState !== "running") return;
      const progress = this.positionIndex(n);
      if (progress !== last) {
        last = progress;
        onTick();
      }
      requestAnimationFrame(watch);
    };
    requestAnimationFrame(watch);

    await anim.finished;
    this.windowEl.classList.remove("spinning");
    this.windowEl.removeAttribute("aria-hidden");
    this.show(target);
    this.settle();
  }

  /** Which tile is currently at the top of the window. */
  positionIndex(n) {
    const matrix = new DOMMatrixReadOnly(getComputedStyle(this.strip).transform);
    const tileHeight = this.strip.getBoundingClientRect().height / n;
    return tileHeight ? Math.round(-matrix.m42 / tileHeight) : 0;
  }

  async fade(target) {
    const out = this.strip.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 200, fill: "forwards" });
    await out.finished;
    this.show(target);
    await this.strip.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300 }).finished;
  }

  settle() {
    const card = this.windowEl.closest(".card");
    card.classList.remove("landed");
    void card.offsetWidth; // restart the animation
    card.classList.add("landed");
  }
}
