# Project instructions

- Keep the implementation compatible with Python 3.10+ and macOS/Linux.
- Prefer the Python standard library; do not add dependencies without a clear reason.
- Keep calculation rules in `../league.py`, CSV handling in `csv_handler.py`, and CLI concerns in `main.py`.
- Preserve historical rules: two points for a win, one for a draw, and goal average as the primary tie-break after points.
- Never rank by modern goal difference before goal average.
- Validate malformed CSV rows and invalid scores with actionable errors.
- Add or update automated tests for every behaviour change.
- Run `python3 -m unittest discover -s tests -v` before considering a change complete.
- Do not invent historical match results. Record source and cutoff assumptions in the README.
