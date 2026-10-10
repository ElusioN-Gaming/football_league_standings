import csv
import tempfile
import unittest
from pathlib import Path

from league import Match, calculate_standings
from csv_handler import read_matches, write_standings


def by_name(standings, name):
    return next(team for team in standings if team.team == name)


class LeagueCalculationTests(unittest.TestCase):
    def test_win_awards_two_points(self):
        table = calculate_standings([Match("Alpha", "Beta", 2, 0)])
        self.assertEqual(by_name(table, "Alpha").points, 2)
        self.assertEqual(by_name(table, "Beta").points, 0)

    def test_draw_awards_one_point_each(self):
        table = calculate_standings([Match("Alpha", "Beta", 1, 1)])
        self.assertEqual(by_name(table, "Alpha").points, 1)
        self.assertEqual(by_name(table, "Beta").points, 1)

    def test_goal_and_match_statistics(self):
        table = calculate_standings([
            Match("Alpha", "Beta", 3, 1),
            Match("Beta", "Gamma", 2, 2),
        ])
        alpha = by_name(table, "Alpha")
        beta = by_name(table, "Beta")
        self.assertEqual((alpha.played, alpha.won, alpha.drawn, alpha.lost), (1, 1, 0, 0))
        self.assertEqual((alpha.goals_for, alpha.goals_against, alpha.goal_difference), (3, 1, 2))
        self.assertEqual((beta.played, beta.won, beta.drawn, beta.lost), (2, 0, 1, 1))
        self.assertEqual(beta.points, 1)

    def test_points_rank_before_goal_average(self):
        table = calculate_standings([
            Match("Lower goal average", "Opponent A", 1, 0),
            Match("Higher points", "Opponent B", 2, 0),
            Match("Higher points", "Opponent C", 1, 0),
        ])
        self.assertEqual(table[0].team, "Higher points")

    def test_goal_average_is_historical_tiebreak_not_goal_difference(self):
        # Both have 2 points. Team A has GD +3 but average 4/1=4;
        # Team B has GD +4 but average 5/1=5; B ranks higher by goal average.
        table = calculate_standings([
            Match("Team A", "A Opponent", 4, 1),
            Match("Team B", "B Opponent", 5, 1),
        ])
        self.assertEqual(table[0].team, "Team B")

    def test_zero_goals_conceded_does_not_crash(self):
        table = calculate_standings([
            Match("Clean Sheet", "Opponent", 1, 0),
            Match("Goalless", "Other", 0, 0),
        ])
        self.assertEqual(by_name(table, "Clean Sheet").goal_average, float("inf"))

    def test_reject_negative_score(self):
        with self.assertRaises(ValueError):
            calculate_standings([Match("Alpha", "Beta", -1, 0)])

    def test_reject_team_playing_itself(self):
        with self.assertRaises(ValueError):
            calculate_standings([Match("Alpha", "alpha", 1, 0)])

    def test_csv_read_and_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            input_path = tmp / "matches.csv"
            output_path = tmp / "nested" / "standings.csv"
            input_path.write_text(
                "home_team,away_team,home_goals,away_goals\nAlpha,Beta,2,0\n",
                encoding="utf-8",
            )
            matches = read_matches(input_path)
            table = calculate_standings(matches)
            write_standings(output_path, table)
            with output_path.open(newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]["team"], "Alpha")
            self.assertEqual(rows[0]["points"], "2")
            self.assertEqual(len(rows), 2)

    def test_csv_missing_columns_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text("home,away,score\nAlpha,Beta,2-0\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing required columns"):
                read_matches(path)

    def test_empty_csv_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.csv"
            path.write_text("home_team,away_team,home_goals,away_goals\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "no match results"):
                read_matches(path)


if __name__ == "__main__":
    unittest.main()
