"""League calculation rules for the English First Division, 1974-75."""
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


@dataclass(frozen=True)
class Match:
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int


@dataclass
class TeamStats:
    team: str
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    @property
    def goal_average(self) -> float:
        if self.goals_against == 0:
            return float("inf") if self.goals_for > 0 else 0.0
        return self.goals_for / self.goals_against


def _sort_key(stats: TeamStats):
    # Use exact fractions for ranking, not the rounded value shown in the CSV.
    if stats.goals_against == 0:
        average_key = (1, Fraction(0, 1)) if stats.goals_for > 0 else (0, Fraction(0, 1))
    else:
        average_key = (0, Fraction(stats.goals_for, stats.goals_against))
    return (-stats.points, -average_key[0], -average_key[1], -stats.goals_for, stats.team.casefold())


def calculate_standings(matches: Iterable[Match]) -> list[TeamStats]:
    teams: dict[str, TeamStats] = {}

    for match in matches:
        home = match.home_team.strip()
        away = match.away_team.strip()
        if not home or not away:
            raise ValueError("Team names must not be empty.")
        if home.casefold() == away.casefold():
            raise ValueError(f"A team cannot play itself: {home}.")
        for label, score, team in (
            ("home", match.home_goals, home),
            ("away", match.away_goals, away),
        ):
            if isinstance(score, bool) or not isinstance(score, int) or score < 0:
                raise ValueError(f"Invalid {label} score for {team}: {score!r}.")

        home_stats = teams.setdefault(home, TeamStats(team=home))
        away_stats = teams.setdefault(away, TeamStats(team=away))
        home_stats.played += 1
        away_stats.played += 1
        home_stats.goals_for += match.home_goals
        home_stats.goals_against += match.away_goals
        away_stats.goals_for += match.away_goals
        away_stats.goals_against += match.home_goals

        if match.home_goals > match.away_goals:
            home_stats.won += 1
            away_stats.lost += 1
            home_stats.points += 2
        elif match.home_goals < match.away_goals:
            away_stats.won += 1
            home_stats.lost += 1
            away_stats.points += 2
        else:
            home_stats.drawn += 1
            away_stats.drawn += 1
            home_stats.points += 1
            away_stats.points += 1

    return sorted(teams.values(), key=_sort_key)
