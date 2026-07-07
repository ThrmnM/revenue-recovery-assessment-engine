# Revenue Recovery System
# ENGINEERING CONSTITUTION
Version 2.0

---

# Mission

Build the fastest, simplest and most effective AI-powered business growth platform for local service businesses.

Every feature must either:

• Generate revenue
• Recover revenue
• Save time
• Improve customer experience

If it does none of these, it probably doesn't belong.

---

# Core Principles

## 1. Production First

No placeholder code.

No demo code.

No fake data unless used for testing.

Every completed feature should be deployable.

---

## 2. MVP First

Working software beats perfect software.

Revenue funds refinement.

Ship.

Learn.

Improve.

---

## 3. Simplicity Wins

Avoid unnecessary complexity.

Avoid enterprise bloat.

Every feature should have a clear business purpose.

---

## 4. Build Assets

Everything becomes an asset.

Code

Documentation

Prompts

Templates

Reports

Automation

Workflows

SOPs

Nothing should have to be recreated twice.

---

## 5. Revenue First

Every module should answer one question:

"How does this help the customer make or recover more money?"

---

# Modular Construction Protocol

Everything is built from the top down.

Capability

↓

Module

↓

Feature

↓

Task

Example

Capability

Assessment Engine

↓

Module

Competitive Analysis

↓

Feature

Google Visibility Analysis

↓

Task

Calculate visibility score

Every Feature must be completed before moving to the next Feature.

Every Module must be completed before moving to the next Module.

The system must remain runnable after every completed task.

---

# AI Collaboration Workflow

This project uses two AI systems.

Each has a specific responsibility.

---

## ChatGPT

Responsible for:

Business strategy

Architecture

Planning

Brainstorming

Feature design

Prioritisation

Code review

Prompt engineering

Documentation

Quality assurance

Decision making

---

## Codex

Responsible for:

Technical planning

Implementation

Refactoring

Testing

Bug fixing

Code generation

Repository operations

---

# Two-Brain Rule

No significant feature enters production until it has been reviewed by two independent reasoning processes.

Workflow

ChatGPT

↓

Codex Planning

↓

ChatGPT Review

↓

Codex Implementation

↓

Testing

↓

Git Commit

---

# Planning Protocol

Every feature begins inside ChatGPT.

Before implementation we answer:

1. Why are we building it?

2. Which Capability does it belong to?

3. Which Module does it belong to?

4. Which Feature is being implemented?

5. What does success look like?

Only then is Codex asked to produce a technical implementation plan.

The implementation plan is reviewed before coding begins.

---

# Implementation Protocol

Codex receives only clearly defined work.

Every implementation request should contain:

Objective

Files to modify

Requirements

Acceptance criteria

Implementation should begin only after the plan has been approved.

---

# Testing Protocol

Every module should include testing.

No feature is complete until:

✓ Code runs

✓ Tests pass

✓ Output verified

✓ Documentation updated

✓ Git committed

✓ Git pushed

---

# Documentation Protocol

Whenever functionality changes, update documentation where applicable.

Possible documents include:

ARCHITECTURE.md

BUSINESS_MODEL.md

DECISIONS.md

ROADMAP.md

SOP.md

README.md

Engineering documentation is considered part of development.

---

# Git Protocol

Commit often.

Commit working software.

Never commit broken code.

Every commit should leave the repository in a deployable state.

Commit messages should explain WHY the change was made.

---

# PDF Standard

Every assessment should appear to have been produced by a professional consulting firm.

Professional typography

Professional spacing

Professional colour palette

Clear hierarchy

Business-focused language

No generic developer output.

---

# Automation First

If a repetitive task can be automated,

automate it.

If AI can perform it reliably,

AI should perform it.

Humans should make decisions.

Machines should execute them.

---

# Prospect Philosophy

Revenue follows prioritisation.

Businesses are ranked by:

Revenue Opportunity

Distress Score

Business Impact

Sales effort should always begin with the highest opportunity prospects.

---

# Version Control Philosophy

Version 1

Working.

Version 2

Better.

Version 3

Excellent.

Never delay Version 1 while chasing Version 3.

---

# Definition of Done

A task is complete only when:

✓ Business objective achieved

✓ Code implemented

✓ Tested successfully

✓ Documentation updated

✓ Committed

✓ Pushed to GitHub

✓ Ready for production

---

# North Star

Every assessment should make the business owner think:

"I don't just want this report...

I want these people to build this system for my business."

If the software creates that reaction,

the mission is being accomplished.

---

# Campaign-First Architecture

The Revenue Recovery System is not a PDF generator.

It is an automated campaign engine.

Every module exists to support the complete workflow from prospect discovery to booked appointments.

The system shall always be designed around the following pipeline:

Prospect Discovery
        ↓
Business Intelligence Engine
        ↓
Assessment Generation
        ↓
PDF Generation
        ↓
Email Generation
        ↓
Campaign Queue
        ↓
n8n Automation
        ↓
Gmail Delivery
        ↓
Appointments
        ↓
Clients

No module may be developed in isolation without considering how it fits into the complete campaign pipeline.

---

# Mock-First Development

All new features shall be developed using deterministic mock data.

External services including:

• Google
• Facebook
• Gmail
• Search APIs
• Maps APIs
• Social APIs

must not become implementation dependencies until the internal workflow has been fully validated.

Mock data shall mirror production data structures as closely as possible.

Replacing mock providers with live providers should require changing only the data provider layer.

---

# Single Source Of Truth

Prospect information shall exist in one authoritative location only.

Supabase will become the primary datastore.

No duplicated business logic.

No duplicated scoring.

No duplicated assessment calculations.

Every downstream component consumes data from the Business Intelligence Engine.

---

# Explain Everything

Every numerical score generated by the system must be explainable.

Every recommendation must reference supporting evidence.

Every weakness must include at least one practical recommendation.

Every assessment must include positive findings whenever supported by available evidence.

Numbers without explanations are prohibited.

---

# Human Approval Before Outreach

Campaigns may be generated automatically.

Emails may be personalized automatically.

PDFs may be generated automatically.

Final outreach remains subject to operator approval unless explicitly configured otherwise.