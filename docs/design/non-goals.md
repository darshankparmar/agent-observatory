# Non-Goals

This document defines what **Agent Observatory intentionally does not do**.

These are not missing features. They are **explicit design boundaries**.

Agent Observatory is designed to be a **fail-open, session-centric instrumentation layer** for AI agents. Anything that violates that role is out of scope.

## 1. Not a Tracing Backend

Agent Observatory does **not**:

* store traces
* index traces
* query traces
* aggregate traces
* retain historical data

It emits **fully materialized session envelopes** and hands them off to exporters.

Storage, retention and querying belong to downstream systems (e.g. OpenTelemetry backends, custom infrastructure).

## 2. Not a UI or Visualization Tool

Agent Observatory does **not**:

* provide dashboards
* render timelines
* visualize spans
* offer replay or analysis views

Any visualization or inspection tooling must live **outside** the core library and consume exported envelopes.

This keeps the core:

* backend-agnostic
* vendor-neutral
* safe to embed in runtimes

## 3. Not a Metrics or Analytics Platform

Agent Observatory does **not**:

* compute aggregates
* emit metrics
* calculate latencies or KPIs
* provide “insights” or recommendations

It captures **what happened**, not **what it means**.

Analysis is intentionally deferred to downstream systems.

## 4. Not a Logging Framework

Agent Observatory does **not**:

* replace structured logging
* manage log levels
* intercept stdout/stderr
* unify logs and traces

Logs and observability traces serve different purposes and coexist by design.

## 5. Not an Agent Framework

Agent Observatory does **not**:

* define agent lifecycles
* manage agent state
* impose execution models
* provide planning or reasoning abstractions
* define what an “agent” is

It observes agent behavior, it does not participate in it.

## 6. No Automatic OpenTelemetry Configuration

Agent Observatory does **not**:

* configure global tracer providers
* mutate OpenTelemetry state
* install OTEL SDKs
* assume any OTEL backend

If OpenTelemetry is used, it must be **explicitly configured by the host application**.

This avoids global side effects and allows clean coexistence with other OTEL-instrumented systems.

## 7. No Background Magic or Hidden Threads

Agent Observatory does **not**:

* spawn hidden threads
* auto-start background workers
* flush implicitly on process exit
* rely on `atexit` hooks

All background behavior is **explicit and opt-in**.

This makes the library predictable in:

* servers
* runtimes
* tests
* constrained environments

## 8. No Guarantees Beyond Fail-Open Safety

Agent Observatory does **not** guarantee:

* trace completeness under overload
* delivery under exporter failure
* persistence across crashes

What it *does* guarantee:

* agent execution is never blocked
* agent execution is never crashed
* failures degrade safely and deterministically

Reliability of observability is intentionally subordinate to reliability of agents.

## 9. No Opinionated Defaults for Production

Agent Observatory does **not**:

* choose exporters for you
* select backends
* recommend vendors
* optimize for specific observability stacks

It provides **primitives**, not prescriptions.

## 10. No End-User Product Guarantees

Agent Observatory is **not** designed for:

* direct end-user adoption
* turnkey setup
* minimal configuration paths
* “just works” experiences

It is intended to be embedded by:

* agent frameworks
* platform teams
* runtime authors

## Design Implication

If a proposed feature requires any of the following, it is **out of scope**:

* persistent state
* global configuration
* background automation
* UI concerns
* metrics or analytics
* agent behavior coupling

Such features should be implemented **outside** the core library, consuming exported session envelopes.

## Stability of These Non-Goals

These non-goals are **intentional and durable**.

Breaking them is considered a **design regression**, not an evolution.

## How This Helps the Project

These constraints ensure Agent Observatory remains:

* safe to embed
* easy to reason about
* compatible with many environments
* viable as shared infrastructure
* suitable as a common instrumentation layer
