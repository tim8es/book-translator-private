# Book Translator — book-state workspace

This repository is an **execution and durable book-state workspace**, not an
independent Book Translator implementation. Its state includes
`books/<slug>/`, `intake/`, `.chat-ops/`, job statuses and delivery receipts.

All reusable code, literary workflows, CLI implementations, provider clients,
validation, review, EPUB builders, and their tests are maintained in:
**https://github.com/tim8es/book-translator**.

## Running

- Auto and monitor Actions use `automation/runtime.lock.json`, checkout the
  exact public commit into ignored `.public-auto-runtime/`, and invoke
  small checked launchers in `automation/`.
- Auto and ChatOps both load the same immutable **executor** revision
  from `automation/runtime.lock.json`. Their job scheduling and model access
  remain independent; book-level concurrency serializes mutations.
- The generic final EPUB Action checks out each book's own pinned **literary**
  revision before running canonical validation/builds. It does not change
  executor or book workflow pins. Public discovery and ChatOps state-only
  bootstrapping are implemented in the public engine, not here.
- `scripts/`, `docs/`, and root workflow contract files may be recreated in
  Actions from the exact book-pinned canonical revision as **ignored, disposable
  runtime cache**. They are not owned or maintained here.

## Change policy

Implement shared bug fixes, workflow changes, tests, and feature work in the
public repository first. Update this repository **only** for Actions triggers,
launchers, pinned runtime SHA, deployment settings, or book state.
Never update a book's own `metadata.json.workflow.resolved_revision`
implicitly when deploying a new public Auto runtime.

**Visibility caution:** the repository's GitHub visibility setting controls
whether book source files, output and Git history are publicly accessible.
Its name alone does not protect them. Do not store credentials in Git.
