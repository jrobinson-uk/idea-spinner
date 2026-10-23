# Idea Spinner: BBC micro:bit built-ins

A version of the Idea Spinner that only uses what's built into the BBC micro:bit. Three cards land on a built-in **Input / Sensor**, a built-in **Output** and an **Extra material**, and learners pitch a project that uses all three.

It runs from the same code as the main site (`../js`, `../css`). Only the deck and the pictures are different.

- **Deck:** [`data/ingredients.json`](data/ingredients.json)
- **V2-only features** are tagged `v2`. They show a "V2" badge, and the **V1 micro:bit only** setting hides them.
- **Pictures:** each built-in feature stacks a board drawing (`img/board.svg`) with a highlight layer (`img/highlights/<id>.svg`), using the `layers` field in the deck. The extra materials reuse the main site's illustrations.

## Rebuilding the pictures

```bash
python3 tools/make_microbit_art.py
```

This makes the board variants from `img/source/microbit-drawing-2.svg` and redraws every highlight. To add a feature, add a highlight to the `H` dictionary in [`tools/make_microbit_art.py`](../tools/make_microbit_art.py) and a line to the deck.

## Using the micro:bit brand

This page follows the [micro:bit brand guidelines](https://microbit.org/brand-guidelines/) for non-commercial educational use.

- **Naming:** the first mention is "BBC micro:bit", then "the micro:bit". The name isn't used as a product name.
- **Board artwork:** only the front of the board is used, with the green fringe, a gold edge connector and no serial number. The back view isn't used because it carries the BBC logo.
- **No characters:** the board isn't given a face or turned into a character.
- **Not affiliated:** the page says it isn't made by or affiliated with the Micro:bit Educational Foundation.

## Licence

- **micro:bit board drawing** (`img/source/`, `img/board*.svg`): © [Micro:bit Educational Foundation](https://microbit.org), from [microbit-svg](https://github.com/microbit-foundation/microbit-svg), licensed [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). The board variants change which layers are shown and the canvas size.
- **Highlight layers** (`img/highlights/`): adaptations made for this page, also licensed [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) so they can be shared alongside the board drawing. Because of this licence, these pictures can't be used commercially.
- **Code and other illustrations:** see the main [README](../README.md).
