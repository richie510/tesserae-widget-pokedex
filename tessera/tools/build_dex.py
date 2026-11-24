#!/usr/bin/env python3
"""Build the small per-Pokémon files the Tessera screensaver reads: tessera/dex/<number>.json.

    python3 tessera/tools/build_dex.py                  # downloads PokéAPI's CSV files from GitHub
    python3 tessera/tools/build_dex.py --csv <folder>   # or reads them from a folder you already have

Why: PokéAPI's own answers are far too large for a Tessera fetch (a /pokemon answer is about 500 KB with every move;
a fetch takes at most 64 KB), and a fetch's texts are cut at 48 bytes. So this script reads PokéAPI's data once (the
CSV files its database is built from, in the PokeAPI/pokeapi repository) and writes one file of about 400 bytes per
Pokémon, with the dex entry split into lines of at most 48 bytes. The screen asks for one of them by its number.

The files only change when PokéAPI adds Pokémon or fixes an entry: run this again then, and commit tessera/dex/.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

CSV_URL = "https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/{name}.csv"
FILES = ["pokemon", "pokemon_stats", "pokemon_types", "type_names", "pokemon_species_names",
         "pokemon_species_flavor_text"]
ENGLISH = "9"
LAST = 1025            # the National Dex as the screensaver's pools know it
LINE_BYTES = 48        # a fetch's text field is cut at 48 bytes (plugin_fetch.TEXT_BYTES)
LINES = 4              # dex0 .. dex3 in the manifest's map
OUT = Path(__file__).resolve().parents[1] / "dex"

# Signs the screen's fonts lack (they would show as squares), in words or letters they have.
SIGNS = {"♀": " F", "♂": " M", "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "−": "-", "…": "...",
         "­": "", " ": " "}


def read(name: str, folder: Path | None) -> list[dict[str, str]]:
    if folder:
        text = (folder / f"{name}.csv").read_text(encoding="utf-8")
    else:
        with urllib.request.urlopen(CSV_URL.format(name=name), timeout=60) as response:
            text = response.read().decode("utf-8")
    return list(csv.DictReader(io.StringIO(text)))


def clean(text: str) -> str:
    for sign, words in SIGNS.items():
        text = text.replace(sign, words)
    text = re.sub(r"\s+", " ", text).strip()
    # The old games wrote POKéMON in capitals.
    return re.sub(r"POK[ÉéE]MON", "Pokémon", text)


def lines(text: str) -> list[str]:
    """The entry in lines of at most LINE_BYTES of UTF-8, broken between words; at most LINES of them."""
    out: list[str] = []
    line = ""
    for word in text.split(" "):
        joined = f"{line} {word}" if line else word
        if len(joined.encode()) <= LINE_BYTES:
            line = joined
            continue
        if line:
            out.append(line)
        line = word
        while len(line.encode()) > LINE_BYTES:   # a word longer than a line (never seen, but safe)
            cut = line.encode()[:LINE_BYTES].decode(errors="ignore")
            out.append(cut)
            line = line[len(cut):]
    if line:
        out.append(line)
    if len(out) > LINES:
        out = out[:LINES]
        last = out[-1]
        while len((last + "...").encode()) > LINE_BYTES and " " in last:
            last = last.rsplit(" ", 1)[0]
        out[-1] = last.rstrip(".,;") + "..."
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--csv", type=Path, help="a folder with PokéAPI's CSV files")
    args = parser.parse_args()
    tables = {name: read(name, args.csv) for name in FILES}

    forms = {r["id"]: r for r in tables["pokemon"] if r["is_default"] == "1" and int(r["id"]) <= LAST}
    stats: dict[str, dict[int, int]] = {}
    for r in tables["pokemon_stats"]:
        stats.setdefault(r["pokemon_id"], {})[int(r["stat_id"])] = int(r["base_stat"])
    type_name = {r["type_id"]: r["name"] for r in tables["type_names"] if r["local_language_id"] == ENGLISH}
    types: dict[str, list[tuple[int, str]]] = {}
    for r in tables["pokemon_types"]:
        types.setdefault(r["pokemon_id"], []).append((int(r["slot"]), type_name.get(r["type_id"], "")))
    names = {r["pokemon_species_id"]: r for r in tables["pokemon_species_names"] if r["local_language_id"] == ENGLISH}
    # The first English entry, from the oldest game: the one the Tesserae widget shows too.
    flavor: dict[str, tuple[int, str]] = {}
    for r in tables["pokemon_species_flavor_text"]:
        if r["language_id"] != ENGLISH:
            continue
        version = int(r["version_id"])
        if r["species_id"] not in flavor or version < flavor[r["species_id"]][0]:
            flavor[r["species_id"]] = (version, r["flavor_text"])

    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    for number in range(1, LAST + 1):
        form = forms.get(str(number))
        if not form:
            print(f"#{number}: not in PokéAPI's data", file=sys.stderr)
            continue
        species = form["species_id"]
        named = names.get(species, {})
        kinds = [name.upper() for _, name in sorted(types.get(str(number), []))]
        base = stats.get(str(number), {})
        entry = {
            "n": number,
            "name": clean(named.get("name") or form["identifier"].replace("-", " ").title()),
            "genus": clean(named.get("genus") or ""),
            "type1": kinds[0] if kinds else "",
            "type2": kinds[1] if len(kinds) > 1 else "",
            # hp, attack, defense, special attack, special defense, speed: PokéAPI's stat ids 1 to 6.
            "stats": [base.get(i, 0) for i in range(1, 7)],
            "height": round(int(form["height"] or 0) / 10, 1),
            "weight": round(int(form["weight"] or 0) / 10, 1),
            "dex": lines(clean(flavor.get(species, (0, ""))[1])),
        }
        path = OUT / f"{number}.json"
        path.write_text(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        written += 1
    print(f"wrote {written} files to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
