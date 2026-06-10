# Layered Architecture (4-Layer DDD)

This document describes the layered architecture of this project — `presentation/` (UI surface), `application/` (business logic), `domain/` (pure models), `infrastructure/` (I/O) — plus `shared/` for cross-cutting utilities. Dependencies flow inward only: a new module goes in the layer matching its responsibility, and must not import from a layer further out.

## Project Structure (Sample)

Concrete entries are placeholders; rename / extend as the project takes shape.
