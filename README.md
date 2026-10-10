# English First Division standings, 1974/75

A Python command-line application that reads match results from a CSV file and writes a league table as CSV. It uses the rules of the English First Division in that season: two points for a win, and goal average (not goal difference) to separate teams level on points.

The included data produces the table after **week 10** of the 1974/75 season (110 matches, 22 teams).

## Quick start (macOS / Linux)

Requirements: Python 3.10 or newer. No third-party packages, so there is nothing to install.

From the project root (the folder containing `main.py`):

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

`python3 main.py` reads `data/week10_results.csv` and writes `output/week10_standings.csv`. It then prints a summary that begins:

```text
Processed 110 matches for 22 teams.
Standings written to: output/week10_standings.csv
```

Developed and run on: Windows 11 Pro 25H2 and Python 3.12.5

### Expected result

The top of the generated table (values are goal average to 3 decimals):

| Pos | Team | P | W | D | L | F | A | GD | GAvg | Pts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Ipswich Town | 10 | 8 | 0 | 2 | 18 | 6 | 12 | 3.000 | 16 |
| 2 | Newcastle | 10 | 6 | 2 | 2 | 19 | 14 | 5 | 1.357 | 14 |
| 3 | Manchester City | 10 | 6 | 2 | 2 | 14 | 11 | 3 | 1.273 | 14 |

Newcastle rank above Manchester City because both have 14 points and Newcastle's goal average is higher. The full table is committed as `output/week10_standings.csv`.

## Running in PyCharm or on Windows

1. Open the project folder (the one containing `main.py`) with **File > Open**.
2. If prompted, add a local Python 3.10+ interpreter. A virtual environment is fine; nothing needs installing.
3. Run `main.py`. The working directory must be the project root. If it is not, set it under **Run > Edit Configurations**.
4. To run the tests, right-click the `tests` folder and choose **Run 'Unittests in tests'**, or use the Terminal tab.

On Windows, if `python3` is not recognised, use `py main.py` and `py -m unittest discover -s tests -v`.

## Input format

A CSV file with a header row and one match per line.

| Column | Meaning |
| --- | --- |
| `home_team`, `away_team` | Team names |
| `home_goals`, `away_goals` | Whole numbers, 0 or more |
| `week`, `date` | Present in the included data; not needed for the calculation |

Invalid input (missing columns, malformed rows, non-numeric or negative scores) stops the run with an error message instead of producing a partial table.

## Output format

`output/week10_standings.csv` has one row per team with these columns:

`position, team, played, won, drawn, lost, goals_for, goals_against, goal_difference, goal_average, points`

- `goal_average` is goals for divided by goals against, shown to 3 decimals. It is `INF` for a team that has scored but not conceded, and `0.000` for a team with no goals for or against.
- `goal_difference` is shown for information only. It is never used for ranking.

## Ranking rules

1. A win is 2 points, a draw 1 point, and a defeat 0.
2. Teams are ranked by points, highest first.
3. Teams level on points are ranked by **goal average**: goals scored divided by goals conceded, highest first. The ratio is compared exactly; only the displayed value is rounded.
4. If still level, teams are ranked by goals scored, then alphabetically by name, so that the output is the same on every run.

Sources for these rules (accessed 2026-10-10):

- [11v11.com league-table notes](https://www.11v11.com/league-tables/league-championship/2020/): two points for a win until 1981; Division One from 1889 to 1976 used goal average, then goals scored, with a mini-league as a last resort.
- [English club records](https://www.stevesfootballstats.uk/club_records.html): goal difference replaced goal average from 1976-77, and three points for a win began in 1981-82.

The 1974/75 season falls inside the goal-average period, so goal difference is not used. The historical mini-league tie-break is not implemented; teams still level after rule 4 are separated only by name. This does not affect the week-10 table.

## Data

- **Source:** [[fill in: where `Figures.csv` came from, and the date you obtained it]]
- **`data/Figures.csv`** is the full 1974/75 First Division fixture list with scores (462 matches, 22 clubs). In this file each whole line is wrapped in quotes and blank lines separate weeks, so it was parsed and converted to a standard CSV.
- **`data/week10_results.csv`** holds every match whose `Wk` label is 1 to 10: 110 matches, exactly 10 per club.

### How "week 10" is defined

The cutoff follows the `Wk` label in the source, not the calendar date. Two matches labelled week 9 were rescheduled and played much later: Leeds United 2-1 Tottenham on 1974-12-04 and Newcastle 3-1 Arsenal on 1975-04-23. They are included, so every club has played exactly 10 matches.

The alternative is a table of what had actually been played by the end of week 10. That would exclude those two matches, leaving Leeds United, Tottenham, Newcastle and Arsenal with 9 games each. If you need that version, filter `data/week10_results.csv` by date before running.

## Project layout

- `main.py`: command-line entry point
- `league.py`: league calculation and ranking rules
- `csv_handler.py`: CSV reading, validation and writing
- `tests/`: automated tests
- `data/`: input data (`Figures.csv`, `week10_results.csv`)
- `output/week10_standings.csv`: generated standings table
- `CLAUDE.md`, `AI_REFLECTION.md`, `.claude/`, `ai/`: AI collaboration artifacts

## AI collaboration

Tool used: Claude in the claude.ai chat.

`CLAUDE.md` holds the project instructions given to the assistant. `AI_REFLECTION.md` is my reflection on the collaboration. The conversation history is in `ai/`. 