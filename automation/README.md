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

Optional Actions variables `OMNIROUTE_TRANSLATOR_FALLBACK_MODEL`,
`OMNIROUTE_REVIEWER_FALLBACK_MODEL` and
`OMNIROUTE_CORRECTOR_FALLBACK_MODEL` select backup models for the matching role
after two successive transient provider failures **or rejected model-output protocol attempts on the same unit**. They
must support the role's JSON contract. If absent, the configured primary is
used. Credentials and model identifiers are never written to the book status.

### Recovering model and provider failures

Each HTTP call has one durable budget reservation (rather than three hidden
network retries within one reservation). Rate limits (429), temporary server
errors (408/5xx) and network timeouts are classified separately from invalid
generated JSON. On transient failures, Auto releases its owned claim and
commits `provider_retry` with the precise unit, role, attempt count, failure
class and next retry timestamp (bounded exponential delay, 1–60 minutes,
honouring numeric Retry-After). It does **not** increment the model-format
failure counter or issue an immediate recursive Actions dispatch. The existing
scheduled Auto workflow will pick up the job when the deadline has passed.
A restarted Actions run revalidates the saved checkpoint, original EPUB and
canonical source/claims before requesting the model again.

For a real **model-output** failure that remains after bounded schema/coverage
repairs, Auto may defer one extracted untranslated unit through the **pinned
canonical** `book.py defer-translation` only if that selected book revision
supports it. It uses the shared hash-bound `.workflow/needs-attention.json`
queue rather than an adapter-owned skip list; other chapters can proceed.
Unchanged deferred units require explicit `book.py retry-attention` to return
to work. Already translated, independently rejected units keep the existing
`defer-review` path. Invalid source bytes, claim/CAS conflicts, unrecognized
model failures and provider misconfiguration are never silently deferred.
When all runnable units are exhausted, the book remains not done until
attention entries have been repaired, translated and independently reviewed.

**Compatibility:** existing books keep their exact workflow revision. A
revision without canonical `defer-translation` cannot gain that transition via
an Auto adapter: it continues to fail closed until an explicit, audited
revision migration. No automatic migration or acceptance is performed.

### OmniRoute JSON-mode compatibility and diagnostics

The adapter requests `response_format: {"type":"json_object"}` from
`/chat/completions`. A JSON-only API key or upstream route must actually
honor this format; the key setting alone does not validate the translation
protocol, semantic coverage or support for strict JSON Schema. The reusable
`omniroute-json-smoke.yml` workflow checks the configured translator model
using one synthetic JSON object. It runs once when the smoke workflow file is
merged to `main`, and can later be launched manually; it never sends book
content or prints the API key, provider URL, model identifier or response text.
A successful smoke confirms only basic JSON API interoperability.

A successful provider response can expose `model_response_diagnostics` in
book status with `finish_reason`, `response_format`, output character count,
provider refusal flag and token usage if available, alongside unit, role and
primary/fallback route. The response body and credentials are never logged
to the status file. Rejected truncated/filtered responses report only a
sanitized finish reason. An absent usage field means the provider did not
return it, not that it used zero tokens.

When a translated unit is being fully retranslated after a completeness
alarm, the corrector uses the Translator structural protocol. Its missing-
coverage and invalid-JSON errors now contribute to the same per-unit
recovery/fallback counter and, after bounded attempts, may be moved to the
pinned canonical `defer-review` queue if the unchanged artifact has a current,
independent rejected review. The existing translation remains unapproved.
Unknown failures, invalid source, and provider outages cannot be deferred.

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
3. POST GitHub Actions workflow_dispatch for auto-translate.yml on main
   with input job_id. Poll automation/status/<job_id>.json. If dispatch
   events are delayed or unavailable, the existing 15-minute schedule
   scans for unfinished requests as a recovery fallback. Do not assume that
   publishing request.json triggers Actions: there is intentionally no push
   trigger for auto-translate.yml. GitHub scheduled runs may be delayed.
4. When state=done, use the output artifact_path and artifact_sha256 in the
   status to retrieve and verify the final EPUB (or download the Actions
   artifact from the finishing workflow run), then send through Telegram.
   When state is missing, still working, or blocked, **do not deliver**.

## Independent monitoring and n8n notifications

A separate GitHub Actions monitor observes every completed automatic workflow
run (including runs reporting success for durable blocked jobs) and scans again
every 15 minutes. It validates completed EPUBs against their manifest, checksum
and current independent review evidence; checks blocked and stale statuses;
and sends signed, idempotent metadata events to n8n. n8n maps the job ID to
the original Telegram recipient and delivers errors or verified EPUBs.

Configure GitHub Actions secrets BOOK_EVENTS_WEBHOOK_URL and
BOOK_EVENTS_SIGNING_SECRET. Without both secrets the monitor inspects but
cannot send messages. The full receiver specification, HMAC verification and
recovery procedure are documented in automation/NOTIFICATIONS.md.

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

## Deterministic book identity and resume

Book matching happens **before** initialization and before a model request.
The preferred title and author are read from the EPUB package metadata
(dc:title / dc:creator); explicit request title/author overrides are supported
for manually corrected metadata. The source EPUB SHA-256, not a generated EPUB
UUID or the uploaded filename, identifies the exact edition.

The automated adapter tries these deterministic checks in order:

1. **Exact SHA-256** of the source EPUB: same input edition. Use the existing
   workspace; do not retranslate previously accepted chapters.
2. **Exact normalized EPUB title** with author compatibility: existing book,
   possibly a changed source edition. Wrong author, conflicting workspaces,
   or incompatible target language block automatic matching.
3. **Renamed but closely related EPUB title** and identical author: require
   the candidate source to contain the ENTIRE previously published XHTML
   spine as an identical text prefix, in reading order. An existing single
   spine unit must contain at least 500 normalized characters, to avoid
   mistaking generic frontmatter for a shared novel. The original EPUB
   must be accessible under the existing book's embedded source storage.
   A single proven match can continue the old book; several matches or
   insufficient evidence cause a safe BookIdentityError.

File names, especially the canonical internal name source.epub, are **not**
book identity and cannot independently trigger a match. Filename changes and
random EPUB UUID changes do not force a new translation.

Once a book is identified, the pinned canonical update-source command
performs the authoritative full-corpus delta: unchanged source units keep
their original unit_id, accepted Russian translation and current independent
review evidence; changed or new units are extracted for normal translation
and review. No approximate chapter similarity is ever used to reuse a
translation. Changing only the EPUB metadata may lead to a new source
revision or no-op depending on the canonical full-corpus comparison.

A similar name with a changed initial chapter is **not proven** to be the same
book, and the adapter will block rather than invent a new workspace or
silently discard prior progress. A totally unrelated title is a new work.
Ambiguous workspaces need explicit manual reconciliation; no existing book
is merged or renamed automatically.

Regression scenario: "The Map of Quiet Places — 1 Chapter (Test Edition)"
followed by "... — 2 Chapters (Test Edition)" under the same author. Their
first XHTML spine item is identical. The latter is routed to the one-chapter
workspace and the canonical source-update handles chapter 2 only. Already
created duplicate workspaces remain untouched; a future update that could
equally match multiple existing editions is deliberately blocked for review.

## Execution and recovery

The workflow intentionally runs at most one state-machine checkpoint per
invocation. n8n does not orchestrate Translator/Reviewer calls. The Actions
runner checks out the exact book engine revision into a disposable runner.
For normal books it obtains the next operation from the pinned canonical
`resume --json` endpoint and loads instructions using that revision's
`workflow.context_routing`; the adapter does not maintain a competing
lifecycle or instruction-routing state machine. The explicit user-approved
preview path retains a separate opt-in policy, without claiming Reviewer PASS.

State mutation uses the pinned standard extract/seal/validate/verify and
claim/accept/review/release/finalize/build commands. Every checkpoint is
published using a normal non-force push to main. If main advanced because an
unrelated book/job was updated, the runner verifies that its own book and status
paths are unchanged, replays its exact committed patch through a disposable
Git index based on the newer main, and attempts a bounded non-force push.
The runner never rebases or resets the active pinned-engine checkout and never
force-pushes. Same-book/status collisions, rewritten upstream history, or
exhausted push retries fail closed without silently overwriting state. A non-model failure (such as unsupported
EPUB semantics, malformed input, or a failed canonical CLI stage) produces a
durable **blocked** status when a status-only compare-and-swap publication is
safe. The runner never commits potentially partial book mutations or releases/takes
over ambiguous claims. An operator may resume a `phase=model-blocked` job
with `resume_blocked=true`, or an `operator-intervention-required` job with
`resume_interrupted=true` only while its recorded canonical claim is still
live. Both actions require the original `job_id`, verify the source hash and
pinned engine, record the recovery, and preserve the cumulative model-call
count. Interrupted recovery reuses the same claim session; it never deletes or
replaces a claim. Expired claims still require the pinned canonical cleanup
procedure. If the repository changed concurrently and even status-only
publication is unsafe, the Actions step fails and no durable blocked status is
promised. The scheduler skips blocked jobs and corrupt status files instead of
retrying one poisoned request forever. After a terminal job the workflow
dispatches **the next unpinned pending request**, rather than retrying the
blocked ID.

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
- A source unit consisting only of external Markdown hyperlinks is preserved
  exactly without a model call. The adapter always preserves link destinations;
  it keeps external labels unchanged for block-preserving EPUB extraction and
  allows label translation in ordinary text extraction.
- The runner now enforces a durable maximum of 36 model invocations per
  job by default. Override with repository variable OMNIROUTE_MODEL_CALL_LIMIT
  (integer 1–400). Each invocation is reserved and checkpointed **before**
  sending its request; reaching the cap blocks and releases the active claim.
  Transport retries inside one invocation may still issue additional HTTP
  attempts. This is **not** a monetary or token-based budget: configure an
  upstream OmniRoute spending cap and check provider pricing separately.
- Each unit may receive at most four accepted Reviewer records. If the fourth
  still requires corrections, defer that unit and continue with the next one.
  Deferred units remain unreviewed; the job blocks before final delivery until
  each deferred unit has a current PASS review.
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
