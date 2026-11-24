# Rapidan AI Skills

This repository is the open-source home for Rapidan AI's reusable agent skills.

## Installation requests

If the user gives this repository URL and asks to install its skills, read [INSTALL.md](INSTALL.md) and perform the installation for your current runtime. The guide covers Codex, Claude Code, and Hermes, destination selection, existing copies, and verification. Installation is self-contained — no internal handbook or code-quality audit is required.

## Repository development

- Keep each skill in its own directory with a `SKILL.md` entry point and its supporting references.
- Preserve relative reference links and include every referenced document when distributing a skill.
- Keep public content free of credentials and private environment configuration.
- Keep the shared skill runtime-neutral; host-specific tool details belong in `references/runtimes.md`.
- Run `python3 -m unittest discover -s tests -v`, check relative links, and review the diff before publishing changes.
- This repository is self-contained: everything needed to develop, test, and publish a skill lives here. If your environment maintains an internal handbook, consult it for operational context — it is optional, and external contributors do not need it.

For installation, honor the user’s named skills exactly. Use `install.py --list` to discover packages; ask for a selection when multiple exist and none was specified. Install all only when explicitly requested.
