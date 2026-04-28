#!/usr/bin/env python3
"""Evidence health checker — verify that all evidence source URLs are reachable.

Modular design for future extension:
  - check_url()          → HTTP HEAD/GET with status classification
  - classify_result()    → alive / redirect / dead / timeout
  - generate_report()    → JSON + markdown output

Usage:
    python3 scripts/verify_evidence.py [--output DIR] [--strict] [--timeout SECS]

Exit codes:
    0 — All URLs alive (or --strict not set)
    1 — Dead URLs detected (only with --strict)
"""

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH_PATH = os.path.join(REPO_ROOT, "graph", "gaia.json")
DEFAULT_TIMEOUT = 15


@dataclass
class URLResult:
    url: str
    skill_id: str
    evidence_index: int
    evidence_class: str
    status: str  # alive, redirect, dead, timeout, error
    http_code: Optional[int] = None
    latency_ms: Optional[int] = None
    detail: Optional[str] = None


def check_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> tuple[str, Optional[int], Optional[int], Optional[str]]:
    """Send HTTP HEAD (fallback GET) to url. Returns (status, http_code, latency_ms, detail)."""
    headers = {"User-Agent": "Gaia-Evidence-Checker/1.0"}
    start = time.time()

    for method in ["HEAD", "GET"]:
        req = Request(url, headers=headers, method=method)
        try:
            with urlopen(req, timeout=timeout) as resp:
                latency = int((time.time() - start) * 1000)
                code = resp.getcode()
                return classify_result(code), code, latency, None
        except HTTPError as e:
            latency = int((time.time() - start) * 1000)
            if e.code == 405 and method == "HEAD":
                continue  # HEAD not allowed, try GET
            return classify_result(e.code), e.code, latency, str(e.reason)
        except URLError as e:
            latency = int((time.time() - start) * 1000)
            reason = str(e.reason)
            if "timed out" in reason.lower() or "timeout" in reason.lower():
                return "timeout", None, latency, reason
            return "error", None, latency, reason
        except Exception as e:
            latency = int((time.time() - start) * 1000)
            return "error", None, latency, str(e)

    return "error", None, None, "All methods exhausted"


def classify_result(http_code: int) -> str:
    """Classify HTTP status code into a health bucket."""
    if 200 <= http_code < 300:
        return "alive"
    elif 300 <= http_code < 400:
        return "redirect"
    else:
        return "dead"


def generate_report(results: list[URLResult], output_dir: Optional[str]) -> tuple[str, str]:
    """Generate JSON and markdown reports. Returns (json_path, md_path) or prints to stdout."""
    summary = {
        "total": len(results),
        "alive": sum(1 for r in results if r.status == "alive"),
        "redirect": sum(1 for r in results if r.status == "redirect"),
        "dead": sum(1 for r in results if r.status == "dead"),
        "timeout": sum(1 for r in results if r.status == "timeout"),
        "error": sum(1 for r in results if r.status == "error"),
    }

    report_data = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": summary,
        "results": [asdict(r) for r in results],
    }

    # Markdown report
    md_lines = [
        "# Evidence Health Report",
        f"**Generated:** {report_data['generated_at']}",
        "",
        "## Summary",
        f"- Total URLs: {summary['total']}",
        f"- Alive: {summary['alive']}",
        f"- Redirect: {summary['redirect']}",
        f"- Dead: {summary['dead']}",
        f"- Timeout: {summary['timeout']}",
        f"- Error: {summary['error']}",
        "",
    ]

    dead_or_bad = [r for r in results if r.status in ("dead", "timeout", "error")]
    if dead_or_bad:
        md_lines.append("## Issues Found")
        md_lines.append("")
        md_lines.append("| Skill | Class | Status | Code | URL |")
        md_lines.append("|---|---|---|---|---|")
        for r in dead_or_bad:
            md_lines.append(f"| `{r.skill_id}` | {r.evidence_class} | {r.status} | {r.http_code or '-'} | {r.url} |")
        md_lines.append("")
    else:
        md_lines.append("## All URLs Healthy")
        md_lines.append("")

    md_content = "\n".join(md_lines)
    json_content = json.dumps(report_data, indent=2, ensure_ascii=False)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        json_path = os.path.join(output_dir, "evidence-health.json")
        md_path = os.path.join(output_dir, "evidence-health.md")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json_content + "\n")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content + "\n")
        return json_path, md_path
    else:
        print(md_content)
        return "", ""


def main():
    parser = argparse.ArgumentParser(description="Verify evidence source URLs")
    parser.add_argument("--output", "-o", help="Output directory for reports")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any dead URLs found")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout in seconds")
    args = parser.parse_args()

    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        graph = json.load(f)

    results: list[URLResult] = []
    skills = graph.get("skills", [])
    total_urls = sum(len(s.get("evidence", [])) for s in skills)

    print(f"Checking {total_urls} evidence URLs across {len(skills)} skills...")

    for skill in skills:
        skill_id = skill["id"]
        for idx, ev in enumerate(skill.get("evidence", [])):
            url = ev.get("source", "")
            if not url:
                continue

            status, code, latency, detail = check_url(url, timeout=args.timeout)
            result = URLResult(
                url=url,
                skill_id=skill_id,
                evidence_index=idx,
                evidence_class=ev.get("class", "?"),
                status=status,
                http_code=code,
                latency_ms=latency,
                detail=detail,
            )
            results.append(result)

            icon = {"alive": ".", "redirect": "~", "dead": "X", "timeout": "T", "error": "!"}
            sys.stdout.write(icon.get(status, "?"))
            sys.stdout.flush()

    print()

    json_path, md_path = generate_report(results, args.output)
    if args.output:
        print(f"\nReports written to: {json_path}, {md_path}")

    dead_count = sum(1 for r in results if r.status in ("dead", "timeout", "error"))
    if dead_count:
        print(f"\n⚠ {dead_count} URL(s) have issues.")
        if args.strict:
            sys.exit(1)
    else:
        print("\n✅ All evidence URLs are healthy.")


if __name__ == "__main__":
    main()
