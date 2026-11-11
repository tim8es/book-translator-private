# Book state notifications: GitHub to n8n to Telegram

This GitHub-only state observer does not mutate books, claims, translations,
review ledgers, or pinned workflow revisions.

## Where it runs

A separate GitHub Actions workflow at .github/workflows/book-job-monitor.yml
is triggered after EVERY Automatic book translation workflow run, even if
GitHub Actions reports success while a book is blocked. It also runs at
minutes 7, 22, 37 and 52 of every hour as a recovery fallback. GitHub
scheduled workflows can be delayed.

n8n receives signed metadata-only events and routes them to Telegram.
Store Telegram chat/message ID in n8n's existing intake mapping keyed by
job_id, not in the public GitHub repository.

## GitHub Actions configuration

Set two Actions repository SECRETS (Settings > Secrets and variables > Actions):

- BOOK_EVENTS_WEBHOOK_URL: production HTTPS n8n Webhook POST URL.
- BOOK_EVENTS_SIGNING_SECRET: a long randomly generated shared HMAC secret.

Both are required. Until configured, the monitor logs a warning, sends
nothing, and deliberately writes no delivery receipts. Never commit either
secret to this public repository.

## n8n recipient workflow

1. Receive POST and preserve the raw JSON body and incoming headers.
2. Verify X-Book-Event-Signature = sha256=<hex HMAC-SHA256> of
   timestamp + "." + the exact raw JSON body bytes, using the shared secret.
   Timestamp is X-Book-Event-Timestamp; reject requests older than five
   minutes. Compare in constant time. Do not reserialize JSON before signing.
   Self-hosted n8n can use an authenticated Code node with built-in crypto
   enabled, or another trusted HMAC verification mechanism.
3. Deduplicate in durable n8n storage using X-Book-Event-Id / event_id
   BEFORE causing Telegram side effects. Use an outbox to handle Telegram
   delivery failures. Respond HTTP 2xx only if the event has been durably
   accepted; return non-2xx on failure. A rare Git receipt push race can
   cause redelivery of the same event, so n8n deduplication is essential.
4. Route **completed** / **completed_preview** to the original user's
   Telegram chat, after the existing EPUB integrity verification.
5. Route **blocked**, **stalled**, and **integrity_failed** to the
   administrator's Telegram chat, NOT to the submitting user. Include the
   job ID, phase, reason, and verified unit counts when present. Do not
   deliver any partial or unverified EPUB.
6. Route terminal checkpoint failures arriving via N8N_DELIVERY_CALLBACK_URL
   and all payloads with admin_alert=true or recipient=admin to the
   administrator's chat. This is an n8n receiver requirement; GitHub can
   only verify HTTP acceptance, not Telegram delivery.

Example event is metadata only (no source or translation prose):

    {
      "schema_version": 1,
      "event_id": "<stable SHA-256>",
      "job_id": "71e930bbab9570de74ee8fda86a625fc",
      "type": "blocked",
      "state": "blocked",
      "phase": "correction-limit-reached",
      "reason": "correction-limit-reached",
      "book_slug": "gothams-fortune-teller",
      "blocked_unit_id": "chapter-000007",
      "correction_rounds": {"chapter-000007": 3},
      "failures": 0,
      "status_updated_at": "2026-11-02T16:54:16.255548+00:00",
      "reviewed_units": 6,
      "total_units": 7
    }

## Independent verification

A status of done alone never authorizes delivery. The monitor validates
the EPUB is under the current book's output directory; the SHA-256 agrees
with both status and output/manifest.json; EPUB ZIP CRC and mimetype pass;
output unit count agrees with progress; and all reviewed units have the
latest independent PASS tied to accepted source and translation SHA-256.
Any unresolved finding fails closed. The only separate path is an
explicitly user-approved unreviewed preview bound to exact approval hashes.

Jobs with an unchanged running status for two hours or more, or registered
intake without durable status for two hours or more, receive a stalled
warning. Malformed statuses and incomplete done books receive
integrity_failed. Neither warning modifies original job state.

## Deduplication, recoverability and operations

After a successful HTTP 2xx, GitHub commits a receipt to:
automation/notifications/sent/<job-id>/<event-id>.json.

The event ID is stable across retries, and receipts are checked before
delivery. HTTPS redirects are refused; failed HTTP calls leave the event
pending. Receipt commits use non-force pushes and retry safe rebases.

Manual inspection without delivery:

    python automation/job_monitor.py --dry-run --include-missing

To backfill after configuring secrets, use Actions > Book job state monitor >
Run workflow. The scheduled monitor also picks up undelivered events.
Do not manually remove claims or change correction round counters.

## GitHub pre-job failure recovery and batching

A GitHub Actions startup_failure creates no job and cannot execute the
process-level n8n callback or write a durable book status. The independent
Book job state monitor now polls the 50 most recent Automatic book translation
runs on each scheduled/completed monitor cycle, looking back 36 hours for
startup_failure and action_required. It recovers the job ID from the run title,
or (for legacy #511-style runs) the single intake request in the triggering
commit. It posts the existing job_id/run_id/conclusion contract to
N8N_DELIVERY_CALLBACK_URL, with recipient=admin, admin_alert=true and a stable
event_id, and records a durable receipt under
automation/notifications/sent/_actions/<run-id>.json.

The n8n delivery callback must route these administrator alerts **only** to
the configured admin Telegram chat, deduplicate by event_id/run_id, and return
HTTP 2xx only after durable acceptance. A missing job ID is permitted for
pre-job failures: include the GitHub run URL for investigation. Confirm the
routing in n8n separately; GitHub-only tests cannot verify Telegram delivery.

The tests workflow no longer runs for book-only checkpoints, intake requests,
job status writes or notification receipts. Pull requests still run full
checks. Batched book integrity validation runs twice an hour and can be
started manually with a lookback window. This reduces runner pressure without
weakening per-checkpoint canonical validation or final delivery gates.
