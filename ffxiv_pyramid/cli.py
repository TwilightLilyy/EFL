"""Command line interface for the FFXIV football pyramid app."""
from __future__ import annotations

from argparse import ArgumentParser, Namespace
import random
from pathlib import Path
from typing import Sequence
from textwrap import indent

from .data import THEMES
from .generator import generate_pyramid
from .io import load_pyramid, save_pyramid
from .model import Pyramid


def _build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Create and iterate on FFXIV themed football pyramids.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate command
    generate_parser = subparsers.add_parser(
        "generate", help="Generate a brand new pyramid and optionally save it to disk."
    )
    generate_parser.add_argument("output", help="Path to save the generated pyramid (must end with .json).")
    generate_parser.add_argument(
        "--levels",
        metavar="N",
        type=int,
        nargs="+",
        required=True,
        help="Number of clubs in each level from top to bottom (e.g. --levels 12 12 18).",
    )
    generate_parser.add_argument(
        "--theme",
        default="eorzea",
        choices=sorted(THEMES.keys()),
        help="Which FFXIV region should inspire the pyramid?",
    )
    generate_parser.add_argument("--title", help="Custom title for the pyramid.")
    generate_parser.add_argument("--description", help="Optional descriptive blurb for the pyramid.")
    generate_parser.add_argument("--seed", type=int, help="Seed for deterministic generation.")
    generate_parser.add_argument(
        "--division-name",
        action="append",
        dest="division_names",
        help="Override the name for a level. Provide one per level in order.",
    )
    generate_parser.add_argument(
        "--preview",
        action="store_true",
        help="Print the generated pyramid without writing to disk.",
    )

    # resample command
    resample_parser = subparsers.add_parser(
        "resample",
        help="Re-roll a pyramid using the metadata in an existing file, optionally tweaking options.",
    )
    resample_parser.add_argument("source", help="Existing pyramid JSON file to use as a template.")
    resample_parser.add_argument(
        "--output",
        help="Where to write the updated pyramid. Defaults to overwriting the source file.",
    )
    resample_parser.add_argument(
        "--levels",
        metavar="N",
        type=int,
        nargs="+",
        help="Override level sizes while keeping the rest of the template.",
    )
    resample_parser.add_argument(
        "--theme",
        choices=sorted(THEMES.keys()),
        help="Switch to a different theme without editing the file manually.",
    )
    resample_parser.add_argument("--seed", type=int, help="Optional new random seed.")
    resample_parser.add_argument(
        "--division-name",
        action="append",
        dest="division_names",
        help="Override level names for the regenerated pyramid.",
    )
    resample_parser.add_argument("--title", help="Update the title while regenerating.")
    resample_parser.add_argument("--description", help="Update the description while regenerating.")
    resample_parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview the regenerated pyramid without writing to disk.",
    )

    # show command
    show_parser = subparsers.add_parser("show", help="Pretty print the contents of a pyramid file.")
    show_parser.add_argument("source", help="Path to the JSON pyramid file to display.")
    show_parser.add_argument(
        "--no-teams",
        action="store_true",
        help="Only show division names instead of listing every team.",
    )

    # themes command
    subparsers.add_parser("themes", help="List all available themes and their highlights.")

    return parser


def _format_team_line(index: int, team_name: str, inspiration: str, location: str) -> str:
    return f"{index:>2}. {team_name} — {location} ({inspiration})"


def _print_pyramid(pyramid: Pyramid, *, show_teams: bool = True) -> None:
    print(pyramid.title)
    if pyramid.description:
        print(pyramid.description)
    if pyramid.meta:
        meta_info = {
            "Theme": pyramid.meta.get("theme"),
            "Levels": pyramid.meta.get("levels"),
            "Seed": pyramid.meta.get("seed"),
        }
        filtered = {key: value for key, value in meta_info.items() if value is not None}
        if filtered:
            print("Meta:")
            for key, value in filtered.items():
                print(f"  {key}: {value}")
    if pyramid.generated_at:
        print(f"Generated at: {pyramid.generated_at.isoformat()} UTC")
    print()

    for division in sorted(pyramid.divisions, key=lambda d: d.level):
        header = f"Level {division.level}: {division.name}"
        if division.short_name:
            header += f" ({division.short_name})"
        print(header)
        if show_teams:
            lines = [
                _format_team_line(idx + 1, team.name, team.inspiration, team.location)
                for idx, team in enumerate(division.teams)
            ]
            if lines:
                print(indent("\n".join(lines), "  "))
        print()


def _generate_from_args(args: Namespace) -> tuple[Pyramid, int]:
    seed = args.seed if args.seed is not None else random.randint(1, 999999)
    pyramid = generate_pyramid(
        level_sizes=args.levels,
        theme=args.theme,
        seed=seed,
        title=args.title,
        description=args.description,
        custom_division_names=args.division_names,
    )
    return pyramid, seed


def _handle_generate(args: Namespace) -> None:
    pyramid, seed = _generate_from_args(args)
    if args.preview:
        _print_pyramid(pyramid)
        print(f"(Preview generated with seed {seed})")
        return
    output_path = Path(args.output)
    save_pyramid(pyramid, output_path)
    print(f"Saved new pyramid to {output_path} (seed={seed})")


def _handle_resample(args: Namespace) -> None:
    source = Path(args.source)
    pyramid = load_pyramid(source)
    meta = pyramid.meta
    theme = args.theme or meta.get("theme", "eorzea")
    levels = args.levels or meta.get("levels")
    if not levels:
        raise SystemExit("The template pyramid does not contain level metadata. Provide --levels explicitly.")
    seed = args.seed if args.seed is not None else random.randint(1, 999999)
    division_names = args.division_names or meta.get("custom_division_names")
    title = args.title or pyramid.title
    description = args.description or pyramid.description
    regenerated = generate_pyramid(
        levels,
        theme=theme,
        seed=seed,
        title=title,
        description=description,
        custom_division_names=division_names,
        extra_meta={"resampled_from": str(source)},
    )
    if args.preview:
        _print_pyramid(regenerated)
        print(f"(Preview generated with seed {seed})")
        return
    target = Path(args.output) if args.output else source
    save_pyramid(regenerated, target)
    print(f"Saved regenerated pyramid to {target} (seed={seed})")


def _handle_show(args: Namespace) -> None:
    pyramid = load_pyramid(args.source)
    _print_pyramid(pyramid, show_teams=not args.no_teams)


def _handle_themes() -> None:
    print("Available themes:\n")
    for key, theme in sorted(THEMES.items()):
        print(f"{key}: {theme.premier_title}")
        print(f"  Highlight: {theme.highlight}")
        print(f"  Sample locations: {', '.join(theme.locations[:5])}...")
        print()


def main(argv: Sequence[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "generate":
        _handle_generate(args)
    elif args.command == "resample":
        _handle_resample(args)
    elif args.command == "show":
        _handle_show(args)
    elif args.command == "themes":
        _handle_themes()
    else:
        parser.error("Unknown command")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
