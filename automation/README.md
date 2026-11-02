# Existing-repository GitHub Actions book translation (opt-in)

This runner is an **optional automated execution adapter**. The canonical
Book Translator state machine and all literary contracts remain in the pinned
public workflow revision. The adapter **does not** change existing books,
their workflow pins, the chat-operations queue, or manual translation support.

## Existing repository visibility

The entire job stays in `tim8es/book-translator-private` alongside current books,
state, and Actions. **No separate repository** is needed. The repository is
currently PUBLIC, despite its name; source EPUB, translation chapters, results,
and Git history can be visible to anyone. This is an intentional deployment
choice for the current project, not a requirement for GitHub Actions.

The operator is responsible for the material uploaded to the public repository.

OmniRoute and its upstream LLM providers also receive source passages.
Review provider terms before enabling paid workloads.

## Configuration

Configure the following GitHub Actions secret and repository variables:

- Secret: OMNIROUTE_API_KEY
- Variable: OMNIROUTE_BASE_URL (HTTPS, OpenAI-compatible base, usually ending in /v1)
- Variable: OMNIROUTE_TRANSLATOR_MODEL
- Variable: OMNIROUTE_REVIEWER_MODEL
- Variable: OMNIROUTE_CORRECTOR_MODEL

Review actual provider compatibility before enabling a paid workload. This
implementation uses POST /chat/completions and does not automate a ChatGPT web
subscription. Ensure GitHub Actions can write to main; branch protections that
prevent non-force pushes require a separately reviewed publication strategy.

## n8n intake contract

1. Assign a random 32-character lowercase hex job_id and calculate SHA-256
   over the exact original EPUB bytes. Do not use the Telegram file_id as a
   job ID or expose bot/user identifiers in the book slug.
2. Commit the original to intake/auto/<job_id>/source.epub and a UTF-8 JSON
   request to intake/auto/<job_id>/request.json on main. Include the original
   source_filename when available. The EPUB title identifies the durable book
   workspace; job_id identifies only the submitted request. A later edition of
   the same title goes through the pinned canonical source-update comparison,
   which reuses only verified unchanged chapters. Ambiguous matches stop for
   manual review. Avoid partial dispatch:
   upload both paths, verify the returned blob bytes and request content, then
   trigger Actions. Use a Git tree/commit to upload both files atomically where
   possible. Retry a failed push only after rechecking HEAD.
3. POST GitHub Actions workflow_dispatch for auto-translate.yml on main with
   input job_id. Poll automation/status/<job_id>.json. Dispatch is optional for
   recovery: a 15-minute schedule scans for unfinished requests.
4. When state=done, use the output artifact_path and artifact_sha256 in the
   status to retrieve and verify the final EPUB (or download the Actions
   artifact from the finishing workflow run), then send through Telegram.
   When state is missing, still working, or blocked, **do not deliver**.

Example request (fill in exact source bytes SHA-256, do not paste placeholders
into a production commit):

    {
      "schema_version": 1,
      "job_id": "0123456789abcdef0123456789abcdef",
      "source_sha256": "<64-lowercase-hex-digest>",
      "target_language": "ru",
      "source_filename": "original.epub"
    }

Optional: workflow_revision (exact 40-hex public commit), title, author,
source_filename. A new book uses a stable slug derived from its EPUB title and
resolves public main exactly once. Existing books retain their workflow pin;
new editions use that pinned revision's source-update contract.

Books with historical `source-updates/` remain blocked until their legacy
translations have been reconciled into canonical state. A per-book
`automation-reconciliation.json` may record the pinned workflow, the audited
source revision and a digest of every historical update file. The adapter
verifies that proof and prevents unchanged imported units from reverting to
`extracted`. A changed history, workflow, missing baseline unit or lost
acceptance blocks processing again. Canonical preflight still validates all
current book and translation hashes before any model call.

An explicit user approval can cover exact existing source and translation
hashes in `automation/user-approvals/<book-slug>.json`. Unchanged approved units
do not need a second Reviewer call; a new or changed unit follows the normal
translation and review process. This approval is not a Reviewer PASS and does
not change the canonical review ledger. When a book contains user-approved
units without independent review, the canonical builder emits an unreviewed
preview and the job sets `review_provenance=user-approved-unreviewed`; delivery
must clearly label that provenance. Existing unapproved units and unresolved
Reviewer findings cannot use this path.

## Execution and recovery

The workflow intentionally runs at most one state-machine checkpoint per
invocation. n8n does not orchestrate Translator/Reviewer calls. The Actions
runner checks out the exact book engine revision into a disposable runner,
runs standard extract/seal/validate/verify and canonical claim/accept/review/
release/finalize/build commands, and publishes each checkpoint using a normal
non-force push to main. A failed compare-and-swap never overwrites remote state.

A Translator claim is committed *before* invoking the model. Reviewer uses a
separate call, only receiving original, accepted translation, literary role
instructions and bounded continuity. Reviewer outcomes require five checked
areas and no unresolved findings for PASS; the canonical review-record and
accept-review are separate gates. A correction round cap prevents an endless
quality loop. The same claim session is resumed if a step is restarted while
its lease is live; expired claims may need cleanup according to the pinned
workflow's canonical cleanup-claims procedure.

This is a **bounded initial MVP**, not unrestricted unattended production:

- Only EPUB, maximum input 15 MB and chapter text 70,000 characters.
- Unsupported EPUB semantics and complex layout remain blocked by the
  canonical extraction and source-coverage checks.
- No technical chunking of oversized chapters yet.
- One writer at a time for automatic books; other GitHub clients may write
  concurrently, protected by non-force publication and canonical claims.
- A runner failure or a persistent model/provider error fails the job. A
  stale claim or failed stage requires examination and audited recovery; do
  not delete claim/coordination locks manually or force-push.
- The adapter reads role instructions via the pinned `agent-manifest.json`
  `context_profiles` and passes the full glossary and style guide. Oversized
  memory fails explicitly instead of silently dropping early decisions.
- Translator/Corrector return structured chapter text and glossary/style
  proposals. The Orchestrator reconciles glossary proposals through the
  canonical claim-bound `ProposalManager` after accepting the translation.
  Reviewer independently checks proposed stylistic decisions, then the
  Orchestrator reconciles those through the same canonical protocol after
  a successful review. Each new claim binds the exact shared-state revisions.
- Active literary waves are not automated. This first adapter does not
  summarize every preceding chapter into a separate plot/continuity memory:
  only the previous chapter excerpt plus canonical glossary/style decisions
  are sent. Do not imply unlimited book-wide recall.
- Automatic model decisions are not a substitute for a human literary review.
  Memory proposals may legitimately be empty; a syntactically valid model
  response alone does not prove all names or voice decisions are captured.
- Model costs depend on provider and tokens. Configure spending caps upstream
  in OmniRoute; this MVP does **not** enforce a book-level monetary limit.
- The reviewer is an LLM, not a guarantee of literary correctness; evaluate
  finished books before offering an unqualified quality guarantee.
- Artifact retention is 30 days; durable final output remains under the
  existing book workspace until deleted under your data retention policy.

For testing, create a small **authorized synthetic** EPUB and assert:
request hash rejection, source-coverage admission, claim owner, translation
acceptance, independent PASS and CORRECTIONS_REQUIRED, restart recovery,
stale Git commit rejection, final EPUB SHA, and delivered artifact parity.
Run the repo's tests in the PR; do not enable production jobs by merging
before the integration test has been verified.
