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
4. Look up the user's original Telegram chat/message using job_id.
5. Route events:
   - completed: fetch artifact_path from GitHub, calculate SHA-256, compare
     with artifact_sha256, then deliver EPUB to the corresponding chat.
   - completed_preview: perform the same SHA check, but explicitly label
     it as a user-approved UNREVIEWED preview.
   - blocked: send phase, reason, blocked_unit_id, optional
     deferred_review_units, reviewed_units and total_units; do not send a
     partial book.
   - stalled: alert about a POSSIBLE stall; inspect Actions and live claims
     before deciding whether a job truly crashed.
   - integrity_failed: raise an error and never deliver an unverified EPUB.

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
