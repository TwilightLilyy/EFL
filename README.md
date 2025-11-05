# Eorzean Football Labs Toolkit

A collection of command line tools for building fictional football league structures and
streamlining Football Manager 2026 editor workflows. The repository currently ships with
two utilities:

* **FFXIV Pyramid Builder** – generate lore-friendly English-style football pyramids
  inspired by Final Fantasy XIV regions.
* **FM26 Auto Editor** – append competition, club, nation, and continent changes to
  Football Manager 2026 Pre-Game Editor XML files from CSV spreadsheets.

Both tools run entirely on the Python standard library and are designed for fast
iteration when experimenting with custom data sets.

## Requirements

* Python 3.10 or newer (the project is regularly exercised with Python 3.12)
* No third-party dependencies are required

Clone the repository and run the modules directly with `python -m …` or point scripts to
`main.py` for the Football Manager helper.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## FFXIV Pyramid Builder

The `ffxiv_pyramid` package focuses on quickly producing JSON descriptions of tiered
football competitions. Each build captures the generated teams, division metadata, and
the random seed so you can iterate on favourite ideas.

### Available commands

Run the tool from the repository root with:

```bash
python -m ffxiv_pyramid.cli <command> [options]
```

The CLI exposes four sub-commands:

| Command    | Purpose |
|------------|---------|
| `themes`   | List the bundled themes (Eorzea, Far East, Garlemald) and their highlights. |
| `generate` | Create a brand new pyramid with custom level sizes, titles, and descriptions. |
| `resample` | Re-roll an existing JSON pyramid while keeping its metadata intact. |
| `show`     | Pretty-print the contents of a pyramid file for quick inspection. |

### Common workflows

Generate a four-tier Eorzean pyramid, preview it, and capture the seed used for later
reproduction:

```bash
python -m ffxiv_pyramid.cli generate builds/my_pyramid.json \
  --levels 12 12 18 24 --theme eorzea --title "Hydaelyn League System" --preview
```

Once you like a structure, drop `--preview` to write the JSON file. Rerun the command with
`--seed` to reproduce the same set of teams.

Regenerate a saved file with different settings using the `resample` command:

```bash
python -m ffxiv_pyramid.cli resample examples/eorzea_pyramid.json \
  --theme far_east --levels 16 18 24 --output builds/far_east_variant.json
```

When exploring existing files, use `show` to display the hierarchy. Add `--no-teams` to
omit team listings for a concise overview.

Each generated JSON document includes the title, description, seed, level sizes, and a
full list of divisions with team inspirations and locations. The files are intentionally
human-friendly so you can tweak names directly and rerun the CLI to preview adjustments.

## FM26 Auto Editor

The `fm26_auto_editor` package automates applying large batches of text and numeric
updates to Football Manager 2026 editor exports. Instead of editing the XML by hand, you
can supply CSV files that describe the desired changes. The tool converts each row into a
`<record>` in the `db_changes` list, preserving the original XML structure.

### Running the CLI

Invoke the CLI module or use `python main.py` (which forwards to the same entry point):

```bash
python -m fm26_auto_editor \
  --base-xml EorzeanFootball.xml \
  --out-xml EorzeanFootball_out.xml \
  --competitions-csv competitions.csv \
  --clubs-csv clubs.csv \
  --nations-csv nations.csv \
  --continents-csv continents.csv
```

Provide only the CSV files you need; categories you omit are ignored. Use `--dry-run` to
preview how many changes would be generated without writing the output file. Increase
logging verbosity by repeating `-v` (for example `-vv` for debug information).

The expected CSV headers are documented alongside the repository's data definitions. Each
row should include the relevant unique IDs from Football Manager, plus the names or
values you wish to update. Invalid or missing IDs are reported in the logs so you can fix
problematic rows quickly.

### Typical flow

1. Export the base database from the Football Manager 2026 Pre-Game Editor as XML.
2. Prepare CSV sheets describing the edits for competitions, clubs, nations, and/or continents.
3. Run `fm26_auto_editor` with `--dry-run` to verify counts.
4. Re-run without `--dry-run` to generate an updated XML ready to import back into the editor.

## Repository layout

```
examples/             Sample pyramid JSON output.
ffxiv_pyramid/        FFXIV-themed pyramid generator source code and data.
fm26_auto_editor/     Football Manager editor automation utilities.
main.py               Convenience entry point for the auto editor CLI.
```

Feel free to adapt the data sets, extend the CLI commands, or wire the tools into larger
workflows for your custom football projects.
