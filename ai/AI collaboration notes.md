# AI collaboration notes

Updated 2026-10-10

## What was done

I built the league-table tool and reviewed your two modules; the tool's 53 tests pass.

1. **Built a league-table tool** from your project rules and two CSVs, in the `league_table` folder: `league.py`, `csv_handler.py`, `main.py`, a README and three test files. All 53 tests pass.
2. **Reviewed your `csv_handler.py`**, then your `league.py`, and cross-checked the pair against my implementation.

## What was verified (by running code)

Every item below comes from code I ran in this session.

- **Tool:** `week10_results.csv` is identical to weeks 1–10 of `Figures.csv`. Totals are consistent across both files, and the pinned Liverpool/Ipswich case shows goal average and goal difference disagreeing.
- **Your `csv_handler.py`:** I confirmed 7 bugs by probing it against a stub `Match` and `TeamStats`: short rows give a poor error; long rows are silently accepted; `int()` is too lenient (it accepts `1_0`, `+2` and non-ASCII digits); line numbers drift after blank lines; header whitespace breaks every row; decode errors leak through; and `mkdir` sits outside the `try`.
- **Your `league.py`:** it gives the same order and totals as mine on both datasets. Goal average beats goal difference, `inf` ranks above any finite average, and exact fractions are handled correctly.
- **Fixes:** my fixes for both files were re-run against the same probes, and they behaved as described.

## What was not verified

Five things were not checked, so treat claims about them as unconfirmed.

- **No Python 3.10, 3.11 or macOS testing.** I only had Linux with 3.12. Your code looks 3.10-safe, but that is untested.
- **I haven't seen your existing tests.** I can't say whether the suite you run covers any of this.
- **The fixes are not in any test suite.** I tested them only with scratch probes, not with new unit tests, so by your own rule they aren't done.
- **The data's origin.** `Figures.csv` has no stated source, and the 1974–75 First Division label is my inference from dates and clubs. Your `league.py` docstring states it as fact, so confirm it.
- **Historical claims.** The full-season order (Derby first, Liverpool above Ipswich) matches my memory of the real season, but I didn't check an outside source.

## Mistakes I made

I made two mistakes, one in a test and one in the first review.

- One of my own tests failed on its first run because I got the arithmetic wrong. I also realised it wouldn't have proved exactness, since doubles could separate those values. I replaced it with values that collapse to the same float but differ as exact fractions.
- In the first `csv_handler.py` review I raised two concerns that depended on code I hadn't seen: `Fraction` formatting on 3.10/3.11 and `nan`. Both turned out not to apply once I saw your `league.py`.

## Where things stand

Only the `league_table` project files are delivered; the fixes to your code exist only in the chat.

- **Delivered:** the `league_table` project files only.
- **Not delivered:** the fixed `read_matches` and the `Match`/name-key patch for `league.py` exist only as code in the chat. Nothing is saved in your project, and nothing is wired into tests.
- **Two implementations exist.** Mine uses `TeamRecord` and `.name`, and ranks by points, goal average, then name. Yours uses `TeamStats` and `.team`, with an extra goals-scored tie-break. They agree on your data only because the data never triggers that tie-break. The README I wrote says "alphabetical" and would be wrong for your version.
- **Cleanup:** a leftover `tests/__pycache__` folder in my project couldn't be deleted because of a sandbox error. It's safe to remove.