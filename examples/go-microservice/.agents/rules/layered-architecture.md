# Microservice Architecture

This document describes the layout of **one service in a larger microservice ecosystem**. The *internal* shape of this service mirrors 4-Layer DDD (presentation → application → domain ← infrastructure + shared); the *additional* conventions in this template cover the cross-service concerns that only apply when this codebase is one of many cooperating services — health and readiness contracts, retries and circuit breakers, distributed tracing, consumer-driven contract tests, and deploy-manifest discipline.

If this repo is a **monorepo containing multiple services**, you want the `ARCH=MONOREPO` template instead (and each sub-service inside picks its own internal architecture — likely this one).

## Project Structure (Sample)

Concrete entries are placeholders; rename / extend as the project takes shape.
