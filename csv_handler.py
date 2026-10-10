"""CSV input/output helpers."""
import csv
from pathlib import Path
from league import Match, TeamStats

INPUT_COLUMNS = {"home_team", "away_team", "home_goals", "away_goals"}
OUTPUT_COLUMNS = [
    "position", "team", "played", "won", "drawn", "lost",
    "goals_for", "goals_against", "goal_difference", "goal_average", "points",
]


def read_matches(path: str | Path) -> list[Match]:
    path = Path(path)
    try:
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                raise ValueError("Input CSV is empty or has no header row.")
            missing = INPUT_COLUMNS - {name.strip() for name in reader.fieldnames if name}
            if missing:
                raise ValueError("Input CSV is missing required columns: " + ", ".join(sorted(missing)))
            matches = []
            for line_number, row in enumerate(reader, start=2):
                if not row or all(value is None or not str(value).strip() for value in row.values()):
                    continue
                try:
                    home = (row.get("home_team") or "").strip()
                    away = (row.get("away_team") or "").strip()
                    if not home or not away:
                        raise ValueError("home_team and away_team are required")
                    home_goals = int((row.get("home_goals") or "").strip())
                    away_goals = int((row.get("away_goals") or "").strip())
                    matches.append(Match(home, away, home_goals, away_goals))
                except (ValueError, AttributeError) as exc:
                    raise ValueError(f"Invalid data on CSV line {line_number}: {exc}") from exc
            if not matches:
                raise ValueError("Input CSV contains no match results.")
            return matches
    except OSError as exc:
        raise ValueError(f"Could not read input file '{path}': {exc}") from exc


def write_standings(path: str | Path, standings: list[TeamStats]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=OUTPUT_COLUMNS)
            writer.writeheader()
            for position, team in enumerate(standings, start=1):
                average = team.goal_average
                writer.writerow({
                    "position": position,
                    "team": team.team,
                    "played": team.played,
                    "won": team.won,
                    "drawn": team.drawn,
                    "lost": team.lost,
                    "goals_for": team.goals_for,
                    "goals_against": team.goals_against,
                    "goal_difference": team.goal_difference,
                    "goal_average": "INF" if average == float("inf") else f"{average:.3f}",
                    "points": team.points,
                })
    except OSError as exc:
        raise ValueError(f"Could not write output file '{path}': {exc}") from exc
