# Revenue Recovery System
# Development Standards

Version: 1.0
Status: Active

---

# Purpose

This document defines the development standards for the Revenue Recovery System.

Its purpose is to ensure that every module, document, and future enhancement follows the same architecture, coding standards, testing workflow, and documentation process.

Consistency is more important than speed.

---

# Project Structure

```
src/
    modules/
    reports/
    tests/

docs/

data/
    companies/
    competitors/

assets/
    charts/
    images/

output/
    reports/
    charts/
```

---

# Module Philosophy

Every business function should exist as its own module.

Examples

- Data Loader
- Scoring Engine
- Executive Summary
- Competitive Analysis
- Recommendation Engine
- Chart Generator
- PDF Generator

Modules should perform one responsibility only.

Avoid creating "god files" that perform multiple unrelated functions.

---

# Development Workflow

Every new module should follow this sequence.

1. Create module.

2. Create test file.

3. Verify console output.

4. Improve formatting.

5. Commit to Git.

6. Integrate into report generator.

7. Test PDF.

8. Commit again.

Never integrate untested code.

---

# Coding Standard

Prefer readable code over clever code.

Use descriptive variable names.

Separate logic into small functions whenever practical.

Comment major sections.

Keep files focused on a single responsibility.

---

# Documentation Workflow

Whenever an architectural decision is made:

Update:

- DECISIONS.md

When project philosophy changes:

Update:

- PROJECT_CONTEXT.md

When report layout changes:

Update:

- REPORT_FRAMEWORK.md

When development workflow changes:

Update:

- DEVELOPMENT_STANDARDS.md

When future ideas arise:

Update:

- IDEAS.md

Never rely on memory.

Documentation is part of development.

---

# Session Startup Checklist

At the beginning of every coding session:

cd ~/Revenue-Recovery-System/05-Code/revenue-recovery

source venv/bin/activate

git status

pwd

tree -L 2

Confirm:

✓ Correct project

✓ Virtual environment active

✓ Git clean

✓ Working on latest version

---

# Session Shutdown Checklist

Before ending a session:

Run all tests.

Generate sample PDF.

Review output.

Commit changes.

Push to GitHub.

Update documentation if necessary.

Update ROADMAP.md if milestones changed.

Leave project in a deployable state.

---

# AI Pair Programming Standard

The AI assistant should always provide:

1. Exact terminal commands.

2. Exact filenames.

3. Where to paste code.

4. Complete scripts whenever practical.

5. Save instructions.

6. Test instructions.

7. Expected output.

Assume the developer is focused on building the product rather than remembering commands.

The objective is to minimize mistakes, reduce context switching, and maintain development momentum.

---

# MVP Principle

The objective is to build a functional Minimum Viable Product first.

Perfection is deferred until Version 2.

If a feature provides significant business value and does not compromise architecture, implement it.

Otherwise, document it in IDEAS.md for future development.

---

# Final Principle

Every line of code should support one of three goals:

1. Generate better reports.

2. Convert more prospects into paying clients.

3. Make the platform easier to maintain and improve.

If it does not support one of those goals, reconsider whether it belongs in the project.
