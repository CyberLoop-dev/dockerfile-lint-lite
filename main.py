#!/usr/bin/env python3
"""Read-only checks for common Dockerfile configuration issues."""
import argparse
import re
from pathlib import Path

SECRET = re.compile(r"(?:PASSWORD|TOKEN|SECRET|API[_-]?KEY)\s*=\s*[^\s$]+", re.I)


def lint(text: str) -> list[dict]:
    findings = []
    lines = text.splitlines()
    instructions = []
    for number, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"([A-Za-z]+)\s+(.*)", stripped)
        if not match:
            continue
        instruction, value = match.group(1).upper(), match.group(2).strip()
        instructions.append((instruction, value, number))
        if instruction == "FROM":
            image = value.split()[0]
            if image.lower().endswith(":latest") or (":" not in image and "@" not in image and image.lower() != "scratch"):
                findings.append({"line": number, "level": "WARN", "message": f"Base image '{image}' is not pinned to a version or digest."})
        if instruction == "ADD":
            findings.append({"line": number, "level": "INFO", "message": "Prefer COPY unless you specifically need ADD archive or URL behavior."})
        if instruction in {"ARG", "ENV"} and SECRET.search(value):
            findings.append({"line": number, "level": "ERROR", "message": "Possible hard-coded secret assignment; use a runtime secret mechanism instead."})
    if not any(item[0] == "FROM" for item in instructions):
        findings.append({"line": 1, "level": "ERROR", "message": "No FROM instruction was found."})
    if not any(item[0] == "USER" for item in instructions):
        findings.append({"line": len(lines) or 1, "level": "WARN", "message": "No USER instruction found; consider running the application as a non-root user."})
    if not any(item[0] == "HEALTHCHECK" for item in instructions):
        findings.append({"line": len(lines) or 1, "level": "INFO", "message": "No HEALTHCHECK instruction found; add one if the image runs a long-lived service."})
    for i, (instruction, value, number) in enumerate(instructions):
        if instruction == "RUN" and "apt-get update" in value and "apt-get install" not in value:
            next_run = next((v for op, v, _ in instructions[i+1:] if op == "RUN"), "")
            if "apt-get install" in next_run:
                findings.append({"line": number, "level": "WARN", "message": "Combine apt-get update and install in one RUN layer to reduce stale package-index issues."})
                break
    return sorted(findings, key=lambda item: (item["line"], item["level"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dockerfile", type=Path)
    parser.add_argument("--strict", action="store_true", help="return exit code 1 for WARN or ERROR findings")
    args = parser.parse_args()
    try:
        findings = lint(args.dockerfile.read_text(encoding="utf-8"))
    except OSError as exc:
        parser.error(str(exc))
    if not findings:
        print("No findings.")
        return 0
    for item in findings:
        print(f"{item['level']:5} line {item['line']:>4}: {item['message']}")
    return 1 if args.strict and any(x["level"] in {"WARN", "ERROR"} for x in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
