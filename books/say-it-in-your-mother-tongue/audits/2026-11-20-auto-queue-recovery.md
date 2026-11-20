# Approved Auto preflight recovery — Say It in Your Mother Tongue

- Recovery timestamp: 2026-11-20T14:41:48.422Z
- Job: a7b9e400d5f2439c8b1e110db202633f
- Source SHA-256: 12e210ce5a95daf56a97ada583ec15c274780c4ddfa7fb92da6a88c67f7c403d
- Workflow revision: 8bb30227adc4bb921429611e12a0af803c9b6487
- Original blocked job status Git blob: 4feb70734f674357345a43e78a2fff714cb3e41b (archived unchanged)
- Historical needs-attention Git blob: 9f84a9e1b5f2decb9bcc324f12a7b82f60a220da (19 entries, archived under .workflow/history)
- Repaired needs-attention Git blob: 25bde9c912e058c7efd9bb1b4f77b28b7cb3224f (empty, pinned revision)
- Progress Git blob: c437d7722b67cd1e03b28383313ecf51d2471f18 (48 extracted, 6 reviewed; unchanged)
- Failure: mismatched historical needs-attention queue made canonical resume return blocked. No model requests were started and no active claim was present at recovery.
- Only the orchestration adapter job is moved to an auditable paused checkpoint for normal Auto validation/restart; no source, chapter, translation acceptance, review PASS or review ledger is changed. The old error remains in durable recoveries and the archived original status.
