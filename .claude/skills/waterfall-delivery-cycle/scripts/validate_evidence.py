#!/usr/bin/env python3
"""Validate waterfall evidence packets beyond JSON Schema checks."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {"phase", "status", "metrics", "artifacts"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def sha256(path: Path) -> str:
    if sys.platform.startswith("win"):
        escaped_path = str(path).replace("'", "''")
        command = f"(Get-FileHash -Algorithm SHA256 -LiteralPath '{escaped_path}').Hash.ToLower()"
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                command,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()

    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_artifact(root: Path, evidence_path: Path, artifact_path: str) -> Path:
    path = Path(artifact_path)
    if path.is_absolute():
        return path

    root_candidate = (root / path).resolve()
    if root_candidate.exists():
        return root_candidate

    return (evidence_path.parent / path).resolve()


def validate(data: dict[str, Any], evidence_path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - data.keys())
    if missing:
        errors.append(f"missing required top-level fields: {', '.join(missing)}")
        return errors

    metrics = data.get("metrics")
    if not isinstance(metrics, dict):
        errors.append("metrics must be an object")
        return errors

    blockers = metrics.get("blockers")
    blocker_ids = data.get("blocker_ids", []) or []
    if not isinstance(blockers, int) or blockers < 0:
        errors.append("metrics.blockers must be a non-negative integer")
    elif blockers != len(blocker_ids):
        errors.append(f"metrics.blockers ({blockers}) must equal blocker_ids length ({len(blocker_ids)})")

    if data.get("status") == "Completed" and blockers:
        errors.append("Completed evidence cannot have blockers")

    test_fields = ("test_count", "test_success", "test_failure", "test_pending")
    if all(isinstance(metrics.get(f), int) for f in test_fields):
        total = metrics["test_success"] + metrics["test_failure"] + metrics["test_pending"]
        if metrics["test_count"] != total:
            errors.append(
                f"metrics.test_count ({metrics['test_count']}) != "
                f"test_success + test_failure + test_pending ({total})"
            )

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts must be a non-empty array")
    else:
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                errors.append(f"artifacts[{index}] must be an object")
                continue
            artifact_path = artifact.get("path")
            if not isinstance(artifact_path, str) or not artifact_path:
                errors.append(f"artifacts[{index}].path is required")
                continue
            if artifact.get("hash_algorithm") != "sha256":
                errors.append(f"artifacts[{index}].hash_algorithm must be sha256")
            expected_hash = artifact.get("hash")
            if not isinstance(expected_hash, str) or len(expected_hash) != 64:
                errors.append(f"artifacts[{index}].hash must be a sha256 hex digest")
                continue

            resolved = resolve_artifact(root, evidence_path, artifact_path)
            if not resolved.exists():
                errors.append(f"artifacts[{index}] missing file: {artifact_path}")
                continue
            actual_hash = sha256(resolved)
            if actual_hash.lower() != expected_hash.lower():
                errors.append(f"artifacts[{index}] hash mismatch: {artifact_path}")

    commands = data.get("commands", []) or []
    if not isinstance(commands, list):
        errors.append("commands must be an array")
    else:
        for index, command in enumerate(commands):
            if not isinstance(command, dict):
                errors.append(f"commands[{index}] must be an object")
                continue
            status = command.get("status")
            exit_code = command.get("exit_code")
            if status == "Pass" and exit_code != 0:
                errors.append(f"commands[{index}] is Pass but exit_code is {exit_code}")
            if status == "Fail" and exit_code == 0:
                errors.append(f"commands[{index}] is Fail but exit_code is 0")
            cmd_str = command.get("command", "")
            is_manual = command.get("manual", False)
            if cmd_str.startswith("manual:") and status == "Pass" and not is_manual:
                errors.append(
                    f"commands[{index}] has manual command but status is Pass; "
                    "set manual:true or use status Skipped, or automate the command"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_json", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root for relative artifact paths")
    args = parser.parse_args()

    try:
        evidence_path = args.evidence_json.resolve()
        data = load_json(evidence_path)
        errors = validate(data, evidence_path, args.root.resolve())
    except Exception as exc:  # noqa: BLE001 - CLI should return concise failure
        print(f"invalid evidence: {exc}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("evidence-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
