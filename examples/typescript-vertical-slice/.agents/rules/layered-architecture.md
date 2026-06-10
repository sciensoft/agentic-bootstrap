# Vertical Slice Architecture

This document describes the **feature-first** layout of this project. Instead of organising by *technical layer* (presentation / application / domain / infrastructure), every feature is a self-contained vertical slice that owns its own thin layers internally. The only allowed cross-slice dependency is `shared/`; **features never import from each other**.

The trade-off vs 4-Layer DDD / Hexagonal: adding a new feature is faster (everything for it lives in one folder) and removing one is trivial (delete the folder); the cost is that cross-cutting refactors touch many slices instead of a single layer, and the discipline of "no feature-to-feature imports" needs active enforcement (linter rule, code review).

## Project Structure (Sample)

Concrete entries are placeholders; rename / extend as the project takes shape.
