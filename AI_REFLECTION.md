# AI Collaboration Reflection

During development, I made a deliberate design decision to keep the solution dependency-free and split it into three small modules: the CLI entry point, the league calculation logic, and CSV input/output. This keeps the rules independently testable and makes the program easier to review than a single large script. I also chose Python's `unittest` and `csv` modules so the project can run on macOS/Linux without installing packages.

A key historical decision was to use the 1974/75 points system (two points for a win) and goal average as the tie-break after points, rather than applying modern goal-difference rules. The supplied source file also wrapped entire CSV rows in quotes, so I normalised it into a conventional CSV before using it as application input. I kept the original week labels and included weeks 1 through 10; this is an explicit assumption that should be checked against the assessor's intended definition of “the 10th week.”

Before submission, I will review this reflection and amend it to accurately describe my own decisions, any mistakes or suggestions I challenged during the actual AI-assisted development, and how I verified the final result. The repository should contain authentic AI session exports from the assistant actually used; this starter project does not claim to contain Claude Code session files.
