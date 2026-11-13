# Before/after code-quality measurements

Use this when planning verification or comparing an authorized implementation. Measure code and checks deterministically; do not infer development-token or dollar savings from source size.

## Comparable scope

Record the baseline revision, final revision or working-tree state, included files, exclusions, commands, and tool versions. The bundled [comparison script](../scripts/compare_code.py) accepts two snapshot directories and the same relative file list; it counts physical lines and changed lines without external packages. For example: `python3 scripts/compare_code.py /tmp/before /tmp/after src/orders.py`. Run it only on authorized code snapshots, and report its inputs. Compare the same source scope before and after. Use repository history or a saved baseline for the before-state; if unavailable, say so rather than reconstructing a number from memory. Separate source, tests, generated code, and documentation when their changes matter.

A useful compact comparison includes:

| Measure | What to report |
| --- | --- |
| Physical source lines | Before, after, and net difference for the same files and counting rule; state whether blank lines and comments are included. |
| Changed lines | Added and deleted lines separately, for example from `git diff --numstat`; this is change size, not the same as the net source-line difference. |
| Files and duplication | Files changed and verified duplicate rules or change sites removed, when countable from source. |
| Behavior | Finding-specific before/after observations or checks, such as preview and checkout totals for the same input. |
| Verification | Test and lint commands, pass/fail counts or findings, and any unavailable checks. Compare only like-for-like runs. |
| Other metrics | Complexity, coverage, dependency counts, or static-analysis findings only when a tool and consistent baseline are available and relevant. |

For a small fix, fewer divergent rules and a passing regression check may matter more than a line reduction. Added tests can increase total lines while improving confidence. Do not treat a smaller file, lower complexity score, or passing command as proof of overall quality by itself. Report regressions and uncertainty.

For read-only reviews and unimplemented plans, give the current observation and specify what to measure after implementation. Do not show hypothetical after numbers or claim a measurement ran. Use the same metrics and evidence in Developer, Plain language, and Learning modes; only presentation differs.
