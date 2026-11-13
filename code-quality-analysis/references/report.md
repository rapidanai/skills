# Evidence-based report

Render according to [modes.md](modes.md). Keep the same finding identities, severity, confidence, evidence, and token estimates across modes.

Begin with scope and coverage: selected lenses, inspected paths, sampling limits, inaccessible areas, and checks actually run. Distinguish “no findings in inspected scope” from “not inspected.” Rank by demonstrated practical consequence, not the number of SOLID labels. Merge only the same underlying issue across lenses; unrelated defects in one file remain separate.

## Finding record (Developer; retained as evidence in other modes)

### N. [Title] [HIGH | MEDIUM | LOW]
**Lens / concern**: Applicable lenses and relevant principle, if any.
**Observation**: What the source actually does.
**Practical impact**: Who or what is affected; concrete failure, change amplification, or navigation/testing burden.
**Evidence**: Verified `file:line` references, including both sites for a repeated pattern. A unique finding can have one citation.
**Confidence**: High / Medium / Low, with what was verified and what remains uncertain. Unsupported suspicions belong in open questions, not ranked findings.
**Divergence**: Number of competing instances where relevant.
**Agent impact**: What future AI-assisted work could get wrong or needlessly repeat.
**Before/after token impact**: Use [tokens.md](tokens.md): same representative task, current work, hypothetical improved work, expenditure direction, savings rating, basis/confidence, and upfront effort. Unknown is valid; no invented totals or percentages.
**Session context**: Recent changes or migration-in-progress evidence, when applicable.

Learning adds a short “Why this matters” paragraph per finding. Plain language leads with the practical consequence and keeps the verified evidence in a concise appendix keyed to finding IDs. Do not hide unresolved risk to make the summary reassuring.

## Severity and evidence

- **HIGH:** evidenced significant behavior/data risk or repeated change failure with broad reach; state the affected behavior and reach. File size, a direct import, or a principle label is insufficient.
- **MEDIUM:** concrete local defect or recurring maintenance/navigation burden with limited reach.
- **LOW:** isolated clarity or housekeeping problem with demonstrated relevance.

Separate confidence from severity. Do not downgrade an unsupported guess to MEDIUM or LOW and report it anyway. Before reporting any finding, read the full relevant function/class and check callers, conventions, or dynamic discovery as needed. A clean/simple implementation is a valid outcome.

End with a short overall pattern summary, conservative before/after token-impact assessment, and open questions/coverage limits. A brief hypothetical improved state may illustrate savings; detailed changes and prescriptions belong in the optional plan. Never present proposed changes as completed work.
