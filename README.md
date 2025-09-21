# FFXIV Football Pyramid Builder

Create custom English-style football pyramids inspired by Final Fantasy XIV regions. The
command line tool included in this repository focuses on fast iteration so you can spin
up a structure, review the clubs, tweak the tiers, and re-roll ideas in just a few
commands.

## Features

- Three curated themes (`eorzea`, `far_east`, `garlemald`) with lore-friendly division
  titles, locations, and inspirations.
- Instant pyramid generation from a single command: specify the number of teams per level
  and receive a ready-to-use JSON description.
- Built-in preview mode to quickly inspect a concept without writing files.
- Resample command that reuses metadata from an existing pyramid to experiment with new
  seeds, level sizes, or themes in seconds.
- Human-readable JSON output that can be version controlled or edited manually for
  bespoke tweaks.

## Getting started

1. Ensure you are using Python 3.10+ (the repo is configured for Python 3.12).
2. No additional dependencies are required—everything runs with the Python standard
   library.
3. Generate your first pyramid:

   ```bash
   python -m ffxiv_pyramid.cli generate builds/my_pyramid.json --levels 12 12 18 24 --theme eorzea --title "Hydaelyn League System"
   ```

   Use `--preview` to see the output without writing to disk.

## Repository layout

- `ffxiv_pyramid/` – source package containing the data sets, generator logic, and CLI.
- `examples/eorzea_pyramid.json` – sample four-tier pyramid showcasing the JSON schema.

## Commands

### List available themes

```bash
python -m ffxiv_pyramid.cli themes
```

### Generate a new pyramid

```bash
python -m ffxiv_pyramid.cli generate builds/garlean_ladder.json --levels 18 18 24 --theme garlemald --title "Imperial Revival Pyramid" --description "League play for the liberated provinces."
```

- `--levels` (required): number of clubs in each tier starting from the top.
- `--theme`: pick the flavour set (`eorzea`, `far_east`, or `garlemald`).
- `--division-name`: override division names (provide once per level, e.g. `--division-name "Crystal Premier" --division-name "Source Championship"`).
- `--seed`: ensure repeatable results.
- `--preview`: print the pyramid without saving to disk.

### Resample using an existing pyramid

Keep the same structure but explore different seeds, level sizes, or even themes.

```bash
python -m ffxiv_pyramid.cli resample examples/eorzea_pyramid.json --seed 9876 --preview
```

You can also switch themes or change tiers without touching JSON manually:

```bash
python -m ffxiv_pyramid.cli resample examples/eorzea_pyramid.json --theme far_east --levels 16 18 24 --output builds/far_east_variant.json
```

### Show a pyramid file

```bash
python -m ffxiv_pyramid.cli show examples/eorzea_pyramid.json
```

Add `--no-teams` for a condensed overview of the structure.

## JSON schema overview

Each generated file is a UTF-8 encoded JSON document with the following top-level
properties:

- `title` / `description`: plain text metadata you can edit manually.
- `generated_at`: timestamp (UTC) of the generation run.
- `meta`: dictionary capturing the seed, level sizes, chosen theme, and additional notes
  (used by the `resample` command).
- `divisions`: ordered array from the top tier downward. Each division contains `level`,
  `name`, `short_name`, and a `teams` list. Every team entry has a lore location,
  inspiration, and optional notes.

Feel free to tweak the JSON directly—`python -m ffxiv_pyramid.cli show` will reflect your
changes immediately.

## Rapid iteration tips

- Rerun `generate` with different `--seed` values to explore alternative club rosters
  while keeping the same structure.
- Use `resample` to branch off variants of your favourite setups without destroying the
  original file.
- Store multiple JSON files in `builds/` or `examples/` and compare them with `git diff`
  to track the evolution of your pyramid concepts.

Happy league building, Warrior of Light!
