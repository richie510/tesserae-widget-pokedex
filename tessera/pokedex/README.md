# Pokédex

A screensaver step of its own for Tessera, built the way the Night clock is: it shows one Pokémon's dex entry over the
glass while the entity you choose for it is on (an input_boolean, a switch or a binary_sensor), and gives way to the
next step of the screensaver's order when that entity is off. So one switch in Home Assistant turns it on and off.

Each entry has the Pokémon's painted artwork (or its classic pixel sprite), its number, name and kind, its types, its
six base stats as bars, its height and weight, and the few lines the Pokédex says about it. It takes a new Pokémon
every few minutes, one a day, or always the same one, from the original 151 up to all 1025.

It is the Tessera version of the [Tesserae Pokédex widget](../../pokedex/) in this repository, with the same data.

## Set up

1. In Home Assistant, make the switch: Settings, Devices and services, Helpers, Create helper, Toggle. Call it
   something like `Tab5 Pokédex` (that makes `input_boolean.tab5_pokedex`). Any switch or binary_sensor works too.
2. Add the plugin to a screen in Tessera: on the Plugins page choose **Add with a link** and give it
   `https://github.com/richie510/tesserae-widget-pokedex/tree/main/tessera/pokedex`, or copy this folder to Home
   Assistant's config as `/config/tessera-plugins/pokedex/`, beside the `esphome` folder, and add it from there. The
   screen builds once.
3. Open the screen's Settings, the **Screensaver** card, and turn on **Show in standby** if it is off.
4. Choose **Add from plugins** and add the **Pokédex** step. Choose its entity (the toggle from step 1) and drag the step
   where you want it in the order: first, to show it whenever the toggle is on.
5. In the step's drawer, choose how often a new Pokémon comes, which pool it comes from, artwork or pixel sprite, and
   whether to show the dex text.

Turn the toggle off and the screensaver goes on to the next step, as it does when the Night clock's entity is off.

## Good to know

- The step shows only on a screen in standby, as every screensaver step does. The screen moves it a millimetre every
  minute so nothing stands on the same pixels all night.
- A screen without pictures (the CYD) shows the words and the stats without the artwork.
- Entries are fetched once per Pokémon and kept by Tessera for a month: after a while most come from its cache.
- **Pokémon of the day** is the same Pokémon all day on every screen, and changes at midnight.

## What leaves your home

The Tessera app in Home Assistant fetches, from `raw.githubusercontent.com` (GitHub):

- the entry of the Pokémon on the glass, from `tessera/dex/<number>.json` in this repository;
- its picture, from PokéAPI's sprites repository (`PokeAPI/sprites`).

Each ask names only the Pokémon's number. Nothing about your home, your screens or your entities is sent. GitHub's own
privacy statement applies to those requests: https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement

## Where the data comes from

Pokémon data and sprites come from [PokéAPI](https://pokeapi.co). PokéAPI's answers are too large for a Tessera fetch,
so `tessera/tools/build_dex.py` reads PokéAPI's own CSV files once and writes one small file per Pokémon to
`tessera/dex/`. Run it again when PokéAPI adds Pokémon. Pokémon and its names are trademarks of Nintendo, Creatures and
Game Freak; this plugin is a fan project and not affiliated with them.
