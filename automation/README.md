# Private-only GitHub Actions book translation (opt-in)

This runner is an **optional automated execution adapter**. The canonical
Book Translator state machine and all literary contracts remain in the pinned
public workflow revision. The adapter **does not** change existing books,
their workflow pins, the chat-operations queue, or manual translation support.

## Security gate — must be addressed before first intake

GitHub's repository API reported this repository as **PUBLIC** during development.
Do not upload or submit any user EPUB or translation while it is public.
The Actions workflow verifies the repository API reports private=true **before**
selecting or opening a job. The status of repository visibility must be
independently checked again before the n8n upload step. A GitHub Secrets key
does not make a public repository's committed book files private.

Only process material the user is authorized to translate and store. Never send
copyrighted user books to public repositories. Check model-provider terms and
data handling before sending text to OmniRoute or its upstream provider.

## Preparation after the repository is private

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

1. Verify repository visibility with the authenticated GitHub REST repository
   metadata endpoint. Require private=true; fail closed otherwise.
2. Assign a random 32-character lowercase hex job_id and calculate SHA-256
   over the exact original EPUB bytes. Do not use the Telegram file_id as a
   job ID or expose bot/user identifiers in the book slug.
3. Commit the original to intake/auto/<job_id>/source.epub and a UTF-8 JSON
   request to intake/auto/<job_id>/request.json on main. Avoid partial dispatch:
   upload both paths, verify the returned blob bytes and request content, then
   trigger Actions. Use a Git tree/commit to upload both files atomically where
   possible. Retry a failed push only after rechecking HEAD.
4. POST GitHub Actions workflow_dispatch for auto-translate.yml on main with
   input job_id. Poll automation/status/<job_id>.json. Dispatch is optional for
   recovery: a 15-minute schedule scans for unfinished requests.
5. When state=done, use the output artifact_path and artifact_sha256 in the
   status to retrieve and verify the final EPUB (or download the private Actions
   artifact from the finishing workflow run), then send through Telegram.
   When state is missing, still working, or blocked, **do not deliver**.

Example request (fill in exact source bytes SHA-256, do not paste placeholders
into a production commit):

    {
      "schema_version": 1,
      "job_id": "0123456789abcdef0123456789abcdef",
      "source_sha256": "<64-lowercase-hex-digest>",
      "target_language": "ru"
    }

Optional: workflow_revision (exact 40-hex public commit), title, author.
A new unpinned book resolves public main exactly once and records the commit
in metadata.json.workflow; subsequent steps use the book's own pin. Only new
books with deterministic slug auto-<job_id> are admitted. Existing books remain
untouched, including those on older revisions.

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
- The current adapter does not automatically reconcile glossary/style change
  proposals or run active literary waves. Such work must not silently skip
  existing memory-impact gates.
- Model costs depend on provider and tokens. Configure spending caps upstream
  in OmniRoute; this MVP does **not** enforce a book-level monetary limit.
- The reviewer is an LLM, not a guarantee of literary correctness; evaluate
  finished books before offering an unqualified quality guarantee.
- Artifact retention is 30 days; durable final output remains under the
  private book workspace until deleted under your data retention policy.

For testing, create a small **authorized synthetic** EPUB and assert:
request hash rejection, source-coverage admission, claim owner, translation
acceptance, independent PASS and CORRECTIONS_REQUIRED, restart recovery,
stale Git commit rejection, final EPUB SHA, and delivered artifact parity.
Run the repo's tests in the PR; do not enable production jobs by merging
before this integration test and the visibility/security gate are verified.
