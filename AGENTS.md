# Rapidan AI Skills

This repository is the open-source home for Rapidan AI's reusable agent skills.

- Keep each skill in its own directory with a `SKILL.md` entry point and its supporting references.
- Preserve relative reference links and include every referenced document when distributing a skill.
- Keep public content free of credentials and private environment configuration.
- Keep the shared skill runtime-neutral; host-specific tool details belong in `references/runtimes.md`.
- Run `python3 -m unittest discover -s tests -v`, check relative links, and review the diff before publishing changes.
- For maintainers working inside Rapidan AI's environment, consult `~/Seafile/rapidanAI/AGENTS.md` and its handbook index for operational context. External contributors do not need that private handbook.
