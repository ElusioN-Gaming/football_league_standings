import argparse
import sys
from csv_handler import read_matches, write_standings
from league import calculate_standings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate English First Division standings using 1974-75 scoring rules."
    )
    parser.add_argument(
        "--input", default="data/week10_results.csv",
        help="Path to the match-results CSV (default: data/week10_results.csv)."
    )
    parser.add_argument(
        "--output", default="output/week10_standings.csv",
        help="Path for the standings CSV (default: output/week10_standings.csv)."
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        matches = read_matches(args.input)
        standings = calculate_standings(matches)
        write_standings(args.output, standings)
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Processed {len(matches)} matches for {len(standings)} teams.")
    print(f"Standings written to: {args.output}")
    print("Top five:")
    for position, team in enumerate(standings[:5], start=1):
        avg = "INF" if team.goal_average == float("inf") else f"{team.goal_average:.3f}"
        print(f"{position:>2}. {team.team:<22} Pts {team.points:>2}  P {team.played:>2}  GAve {avg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
