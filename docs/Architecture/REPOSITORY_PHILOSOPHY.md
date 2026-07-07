# Repository Philosophy

Version: 1.0

---

## Purpose

This repository is designed to be understandable by both humans and AI.

Every directory, module, document, and file has a single responsibility.

The goal is to reduce complexity, eliminate duplication, and make the system maintainable for years.

---

## Core Engineering Principles

### 1. Single Responsibility

Every module should have one responsibility.

Every document should answer one question.

Every directory should have one purpose.

---

### 2. Modular First

Large systems are built from small independent components.

Each module should be testable in isolation.

No module should depend unnecessarily on another.

---

### 3. Source of Truth

Every piece of information should exist only once.

Avoid duplicate documents.

Avoid duplicate calculations.

Avoid duplicate business rules.

---

### 4. Separation of Concerns

Planning documents are not architecture.

Architecture documents are not implementation.

Implementation is not generated output.

Generated output is never source code.

---

### 5. AI Friendly

The repository should be understandable by:

- ChatGPT
- Claude
- Codex
- Gemini
- Future AI systems

An AI should be able to understand the repository simply by reading the documentation.

---

### 6. Human Friendly

Any experienced developer should be able to locate code in under 30 seconds.

If something cannot be found quickly, the repository structure should be improved.

---

### 7. No Magic

Business logic should be explicit.

Avoid hidden assumptions.

Avoid "clever" code.

Prefer readability over brevity.

---

### 8. Preserve History

Nothing should be deleted unless it has no future value.

Deprecated documents should move into Archive.

Historical decisions should remain discoverable.

---

### 9. Build for Scale

Every feature should be designed with future growth in mind.

Today's MVP should evolve into tomorrow's platform without requiring a complete rewrite.

---

### 10. Legacy

This project is intended to outlive its original creator.

Documentation is considered part of the product.

Every architectural decision should make the system easier for future developers—including family members—to understand and maintain.