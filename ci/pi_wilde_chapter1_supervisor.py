#!/usr/bin/env python3
"""Disposable one-chapter Pi pilot supervisor.

Dispatches existing universal GitHub Action one checkpoint at a time. Never
executes model calls itself. Stops at the FIRST story's canonical reviewed
state, with all other story units remaining untouched.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import json
import os
import subprocess
import sys
import time

JOB_ID = "297fd08ee43deb245fd4a033240ded56"
SLUG = "the-happy-prince-and-other-tales"
TEST_BRANCH = "ci/pi-wilde-first-real-book-20261121"
EXPECTED_RUN_NAME = "Pi book translation " + JOB_ID
MAX_DISPATCHES = 16
MAX_RUN_SECONDS = 3300
POLL_SECONDS = 12


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def gh(*args: str) -> str:
    p = subprocess.run(["gh", *args], text=True, encoding="utf-8",
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       timeout=45, check=False)
    if p.returncode:
        raise RuntimeError("GitHub CLI request rejected (" + args[0] + ")")
    return p.stdout


def api(path: str) -> dict:
    return json.loads(gh("api", path))


def read_main_json(path: str) -> dict:
    data = api("repos/" + os.environ["GITHUB_REPOSITORY"]
               + "/contents/" + path + "?ref=main")
    check(data.get("encoding") == "base64", "unsupported_file_encoding")
    return json.loads(base64.b64decode(data["content"]).decode("utf-8"))


def runs() -> list[dict]:
    content = api("repos/" + os.environ["GITHUB_REPOSITORY"] +
                  "/actions/workflows/pi-book-translation.yml/runs"
                  "?event=workflow_dispatch&per_page=60")
    found = [
        x for x in content["workflow_runs"]
        if x.get("display_title") == EXPECTED_RUN_NAME
        and x.get("head_branch") == "main"
    ]
    return sorted(found, key=lambda x: x["id"], reverse=True)


def wait_run(run_id: int) -> None:
    deadline = time.monotonic() + MAX_RUN_SECONDS
    while time.monotonic() < deadline:
        item = api("repos/" + os.environ["GITHUB_REPOSITORY"]
                   + "/actions/runs/" + str(run_id))
        if item.get("status") == "completed":
            print("PI_CHECKPOINT_FINISHED run=" + str(run_id) +
                  " result=" + str(item.get("conclusion")), flush=True)
            check(item.get("conclusion") == "success",
                  "pi_checkpoint_not_successful_run_" + str(run_id))
            return
        time.sleep(POLL_SECONDS)
    raise RuntimeError("pi_checkpoint_wait_timeout_" + str(run_id))


def snapshot() -> tuple[dict, dict, str]:
    progress = read_main_json("books/" + SLUG + "/progress.json")
    status = read_main_json("automation/status/" + JOB_ID + ".json")
    chapters = progress.get("chapters", [])
    check(len(chapters) == 5 and chapters[0].get("unit_id") == "chapter-000001",
          "unexpected_book_unit_layout")
    check(all(c.get("status") == "extracted" for c in chapters[1:]),
          "pilot_advanced_another_story")
    check(status.get("job_id") == JOB_ID and status.get("book_slug") == SLUG,
          "durable_job_identity_mismatch")
    check(status.get("state") in {"running", "done"}, "job_blocked_or_paused")
    first = chapters[0].get("status")
    check(first in {"extracted", "translated", "reviewed"},
          "unexpected_first_story_state")
    retry = status.get("provider_retry")
    if isinstance(retry, dict) and isinstance(retry.get("not_before"), str):
        target = datetime.fromisoformat(retry["not_before"].replace("Z", "+00:00"))
        if target > datetime.now(timezone.utc):
            raise RuntimeError("provider_backoff_active_until_" + retry["not_before"])
    print("PI_BOOK_CHECKPOINT first_story=" + first +
          " phase=" + str(status.get("phase")) +
          " completed_segments=" +
          str((status.get("structural_segment_progress") or {}).get("completed", "n/a")) +
          " model_calls=" + str(status.get("model_calls_started", "n/a")),
          flush=True)
    return status, progress, first


def main() -> None:
    check(os.environ.get("GITHUB_REF") ==
          "refs/heads/" + TEST_BRANCH, "wrong_test_branch")
    check(bool(os.environ.get("GH_TOKEN")), "github_actions_token_missing")
    for i in range(MAX_DISPATCHES):
        status, progress, first = snapshot()
        if first == "reviewed":
            print("FIRST_STORY_REVIEWED_CONFIRMED", flush=True)
            return

        existing = runs()
        latest = existing[0] if existing else None
        if latest and latest.get("status") != "completed":
            print("WAIT_EXISTING_PI_RUN id=" + str(latest["id"]), flush=True)
            wait_run(latest["id"])
            continue

        before = latest["id"] if latest else 0
        print("DISPATCH_ONE_PI_CHECKPOINT iteration=" + str(i+1), flush=True)
        gh("workflow", "run", "pi-book-translation.yml",
           "--repo", os.environ["GITHUB_REPOSITORY"], "--ref", "main",
           "-f", "probe_only=false", "-f", "job_id=" + JOB_ID,
           "-f", "continue_automatically=false")
        next_id = None
        for _ in range(45):
            candidates = runs()
            if candidates and candidates[0]["id"] > before:
                next_id = candidates[0]["id"]
                break
            time.sleep(4)
        check(next_id is not None, "dispatch_unconfirmed_no_retry")
        print("PI_DISPATCH_CONFIRMED run=" + str(next_id), flush=True)
        wait_run(next_id)

    # Final check even if the last dispatch crossed MAX_DISPATCHES.
    _, _, first = snapshot()
    check(first == "reviewed", "first_story_not_reviewed_within_bounded_dispatches")
    print("FIRST_STORY_REVIEWED_CONFIRMED", flush=True)


try:
    main()
except BaseException as exc:
    print("PI_CHAPTER1_SUPERVISOR_STOPPED category=" + type(exc).__name__
          + " code=" + str(exc)[:130], file=sys.stderr)
    sys.exit(1)
