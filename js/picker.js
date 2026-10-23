// Pure picking logic: no DOM, so it can be tested on its own.

/** Uniform random float in [0, 1) using the crypto API. */
export function cryptoRandom() {
  const buf = new Uint32Array(1);
  crypto.getRandomValues(buf);
  return buf[0] / 2 ** 32;
}

/** Small seeded generator (mulberry32) for repeatable tests. */
export function seededRandom(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 2 ** 32;
  };
}

/** Ingredients allowed on a wheel. `filter.excludeTags` lists tags to leave out, e.g. ["ai"]. */
export function poolFor(deck, wheelId, filter = {}) {
  const excluded = filter.excludeTags ?? [];
  return deck.filter(
    (item) => item.wheel === wheelId && !(item.tags ?? []).some((tag) => excluded.includes(tag))
  );
}

/**
 * Which tags to leave out, from the deck's options and the viewer's settings.
 * An option normally includes its tag only when switched on (e.g. "Include AI");
 * with `hides: true` it removes its tag when switched on (e.g. "V1 only" hides "v2").
 */
export function excludedTags(options = [], settings = {}) {
  return options
    .filter((opt) => {
      const on = settings[opt.id] ?? opt.default ?? false;
      return opt.hides ? on : !on;
    })
    .map((opt) => opt.tag);
}

export function choose(list, random = cryptoRandom) {
  return list[Math.floor(random() * list.length)];
}

/**
 * Pick a new combination.
 * - Locked wheels keep their current item.
 * - Unlocked wheels avoid the item they're showing now, so a re-spin always changes something.
 * - No item appears on two wheels at once.
 *
 * @param {object[]} deck      all ingredients
 * @param {object[]} wheels    [{id, label}]
 * @param {Set<string>} locked wheel ids that are locked
 * @param {object} current     {wheelId: ingredient} currently shown (may be empty)
 * @param {object} filter      {excludeTags}
 * @param {function} random    () => [0, 1)
 * @returns {object} {wheelId: ingredient}
 */
export function pick(deck, wheels, locked, current = {}, filter = {}, random = cryptoRandom) {
  const result = {};
  const used = new Set();

  for (const wheel of wheels) {
    if (locked.has(wheel.id) && current[wheel.id]) {
      result[wheel.id] = current[wheel.id];
      used.add(current[wheel.id].id);
    }
  }

  for (const wheel of wheels) {
    if (result[wheel.id]) continue;
    const pool = poolFor(deck, wheel.id, filter);
    const fresh = pool.filter(
      (item) => !used.has(item.id) && item.id !== current[wheel.id]?.id
    );
    // Fall back gracefully if a tiny deck leaves nothing fresh.
    const options = fresh.length ? fresh : pool.filter((item) => !used.has(item.id));
    const chosen = choose(options.length ? options : pool, random);
    result[wheel.id] = chosen;
    used.add(chosen.id);
  }

  return result;
}

/** Random filler items for a spinning strip (repeats are fine, but not back-to-back). */
export function fillerStrip(pool, length, random = cryptoRandom) {
  const strip = [];
  for (let i = 0; i < length; i++) {
    let item = choose(pool, random);
    if (pool.length > 1) {
      while (item === strip[strip.length - 1]) item = choose(pool, random);
    }
    strip.push(item);
  }
  return strip;
}
