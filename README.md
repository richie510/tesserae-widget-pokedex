# Pokédex — Tesserae widget

A Pokédex entry card for [Tesserae](https://github.com/dmellok/tesserae-widgets) e-ink dashboards, powered by [PokéAPI](https://pokeapi.co): real base stats, types, genus, dex flavor text, and the classic pixel sprite (or official artwork).

## Modes

- **Random every refresh** — a new Pokémon on every render; pair it with a schedule for a rotating dex.
- **Pokémon of the day** — stable per calendar day.
- **Fixed pick** — lock to a name or dex number.

The **pool** option bounds random/daily rolls: original Kanto 151 (default), Gen I–II, Gen I–III, or all 1025.

The **Dex text** option sets how much of the Pokédex entry shows: **Two lines** (default), **Full entry**, which takes room from the sprite and stats so the whole entry fits, or **Hidden**.

## Themes

- **House style** — clean Spectra card that follows your dashboard theme.
- **Pokédex (classic red)** — the red device: lens and LEDs, cream screen bezel, red stat bars, dex text on a green-on-black sub-screen.
- **Game Boy (mono green)** — DMG green palette with a grayscale sprite; dithers cleanly on mono e-ink panels.

## Fragments

- `sprite` — just the sprite on a tile with name + number.
- `stats` — the six base-stat bars.

## Data

Fetches from `pokeapi.co` server-side with a long-lived per-Pokémon cache (dex data is effectively static). Sprites are hotlinked from the PokeAPI sprites repo. No account or API key needed.

## Install

Install from the Tesserae widget marketplace (`pokedex`), or drop the `pokedex/` folder into your Tesserae plugins directory.

## Tessera screensaver

`tessera/pokedex/` is the same Pokédex as a plugin for [Tessera](https://github.com/MaxGramser/tessera-plugins), the
ESP32 touch screens for Home Assistant: a screensaver step of its own that shows a Pokémon's dex entry while an entity
you choose (a toggle helper, a switch) is on, and gives way to the next step when it is off. Add it in Tessera with the
link `https://github.com/richie510/tesserae-widget-pokedex/tree/main/tessera/pokedex`; its
[README](tessera/pokedex/README.md) has the steps. Its data is in `tessera/dex/`, written by `tessera/tools/build_dex.py`.
