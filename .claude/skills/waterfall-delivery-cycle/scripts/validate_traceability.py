#!/usr/bin/env python3
"""Validate waterfall traceability.json beyond JSON Schema checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any


ID_RE = re.compile(
    r"^(BR|FR|SCRR|RPT|NTF|BAT|DR|IR|MIG|IMP|TST|AC|CON|TBD|RSK)-[0-9]{3,}$"
    r"|^NFR-[A-Z0-9]+-[0-9]{3,}$"
    r"|^SCR-[A-Z0-9]+-[0-9]{3,}$"
    r"|^API-[0-9]{3,}$"
    r"|^TBL-[0-9]{3,}$"
    r"|^FLOW-[0-9]{3,}$"
    r"|^ERR-[A-Z0-9]+-[0-9]{3,}$"
    r"|^(UTV|UT|TV|TC|TD|UTF)-[0-9]{3,}$"
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def iter_nodes(data: dict[str, Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for section in ("requirements", "designs", "tests"):
        for node in data.get(section, []) or []:
            if isinstance(node, dict):
                nodes.append(node)
    return nodes


def validate(data: dict[str, Any], release: bool) -> list[str]:
    errors: list[str] = []
    nodes = iter_nodes(data)
    ids = [node.get("id") for node in nodes]
    ids = [id_value for id_value in ids if isinstance(id_value, str)]
    id_set = set(ids)

    for id_value, count in Counter(ids).items():
        if count > 1:
            errors.append(f"duplicate id: {id_value}")

    for node in nodes:
        id_value = node.get("id")
        if not isinstance(id_value, str) or not ID_RE.match(id_value):
            errors.append(f"invalid id: {id_value!r}")
            continue

        for link in node.get("links", []) or []:
            if not isinstance(link, str) or not ID_RE.match(link):
                errors.append(f"{id_value}: invalid link id {link!r}")
            elif link not in id_set:
                errors.append(f"{id_value}: link target does not exist: {link}")

    if release:
        graph: dict[str, set[str]] = defaultdict(set)
        tc_pass: set[str] = set()
        for node in nodes:
            id_value = node.get("id")
            if not isinstance(id_value, str):
                continue
            for link in node.get("links", []) or []:
                if isinstance(link, str):
                    graph[id_value].add(link)
                    graph[link].add(id_value)
            if node.get("type") == "TC" and node.get("result") == "Pass":
                tc_pass.add(id_value)

        for node in data.get("requirements", []) or []:
            if not isinstance(node, dict) or node.get("type") != "AC":
                continue
            ac_id = node.get("id")
            if not isinstance(ac_id, str):
                continue
            if not reaches_any(ac_id, tc_pass, graph):
                errors.append(f"{ac_id}: no reachable passed TC-* test case")

    return errors


def reaches_any(start: str, targets: set[str], graph: dict[str, set[str]]) -> bool:
    seen = {start}
    queue: deque[str] = deque([start])
    while queue:
        current = queue.popleft()
        if current in targets:
            return True
        for next_id in graph.get(current, set()):
            if next_id not in seen:
                seen.add(next_id)
                queue.append(next_id)
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("traceability_json", type=Path)
    parser.add_argument("--release", action="store_true", help="enforce release-gate AC -> passed TC reachability")
    args = parser.parse_args()

    try:
        data = load_json(args.traceability_json)
        errors = validate(data, args.release)
    except Exception as exc:  # noqa: BLE001 - CLI should return concise failure
        print(f"invalid traceability: {exc}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("traceability-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
