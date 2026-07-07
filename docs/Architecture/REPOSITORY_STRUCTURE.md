# Repository Structure

Version: 1.0

---

## Purpose

This document defines the canonical repository structure.

All future development must conform to this specification.

---

# Top Level


01-Setup/

02-Screenshots/

03-Prompts/

04-Workflows/

05-Code/

06-Content/

07-Issues-and-Fixes/

08-Releases/

README.md

USER.md

ANTI_VALUES.md


05-Code/

revenue-recovery-assessment-engine/


---

# docs/


---

# src/


---

# tests/


---

# data/


---

# output/


---

# Rules

Planning documents belong in docs/planning.

Architecture documents belong in docs/architecture.

Business strategy belongs in docs/business.

Generated PDFs belong in output.

Mock data belongs in data/mock.

Production configuration belongs in config.

Repositories only read and write data.

Services contain business logic.

Exporters generate output.

Models define shared objects.

Utilities contain reusable helper functions.

---

# Repository Standards

No duplicate documents.

No duplicate calculations.

No generated files inside src.

No business logic inside exporters.

No mock data inside production code.

No architecture decisions inside planning documents.

No implementation notes inside architecture.

---

# Goal

Every file should have exactly one logical home.

A developer or AI should be able to predict where a file belongs without searching the repository.
