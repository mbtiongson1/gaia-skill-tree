import html
import json
import os
from typing import Dict, Iterable, List, Tuple


CATALOG_PATH = os.path.join("graph", "real_skill_catalog.json")


def _escape(value):
    return html.escape(str(value or ""), quote=True)


def _source_by_id(catalog):
    return {source["id"]: source for source in catalog.get("sources", [])}


def _source_label(source):
    label = source.get("name", source.get("id", "Unknown source"))
    count = source.get("reportedSkillCount")
    if count:
        return f"{label} ({count})"
    return label


def _render_sources(catalog):
    rows = []
    for source in catalog.get("sources", []):
        rows.append(
            "<tr>"
            f"<td><a href=\"{_escape(source.get('url'))}\">{_escape(source.get('name'))}</a></td>"
            f"<td>{_escape(source.get('type'))}</td>"
            f"<td>{_escape(source.get('reportedSkillCount', ''))}</td>"
            f"<td>{_escape(source.get('notes'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _render_bucket(bucket, sources):
    cards = []
    for item in bucket.get("items", []):
        source = sources.get(item.get("sourceId"), {})
        source_url = item.get("detailUrl") or item.get("sourceUrl") or source.get("url", "")
        maps_to = item.get("mapsToGaia", [])
        chips = "".join(f"<span>{_escape(skill)}</span>" for skill in maps_to)
        path = item.get("path")
        path_html = f"<p class=\"path\">{_escape(path)}</p>" if path else ""
        cards.append(
            "<article class=\"skill-card\">"
            f"<h3><a href=\"{_escape(source_url)}\">{_escape(item.get('name'))}</a></h3>"
            f"<p class=\"source\">{_escape(_source_label(source))}</p>"
            f"<p>{_escape(item.get('description'))}</p>"
            f"{path_html}"
            f"<div class=\"chips\">{chips}</div>"
            "</article>"
        )
    return (
        "<section class=\"bucket\">"
        f"<h2>{_escape(bucket.get('name'))}</h2>"
        f"<p>{_escape(bucket.get('summary'))}</p>"
        f"<div class=\"grid\">{''.join(cards)}</div>"
        "</section>"
    )


def _render_html(catalog):
    sources = _source_by_id(catalog)
    buckets = "\n".join(_render_bucket(bucket, sources) for bucket in catalog.get("buckets", []))
    generated_at = _escape(catalog.get("updatedAt", "unknown"))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Gaia Real Skill Catalog</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f8fa;
      --ink: #1d2430;
      --muted: #5d6878;
      --line: #d9dee7;
      --panel: #ffffff;
      --accent: #1967d2;
      --chip: #eef4ff;
    }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.5;
    }}
    header, main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 32px 20px;
    }}
    header {{
      padding-bottom: 12px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 34px;
      line-height: 1.12;
      letter-spacing: 0;
    }}
    h2 {{
      margin: 0 0 8px;
      font-size: 22px;
      letter-spacing: 0;
    }}
    h3 {{
      margin: 0 0 8px;
      font-size: 16px;
      letter-spacing: 0;
    }}
    p {{
      margin: 0 0 14px;
      color: var(--muted);
    }}
    a {{
      color: var(--accent);
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .source-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0 32px;
      background: var(--panel);
      border: 1px solid var(--line);
    }}
    th, td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      font-size: 14px;
    }}
    th {{
      color: var(--muted);
      font-weight: 650;
      background: #f0f3f8;
    }}
    .bucket {{
      margin: 0 0 34px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 14px;
    }}
    .skill-card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      min-height: 185px;
    }}
    .source, .path {{
      font-size: 13px;
      margin-bottom: 10px;
    }}
    .path {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      color: #3f4a5a;
      overflow-wrap: anywhere;
    }}
    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 12px;
    }}
    .chips span {{
      border-radius: 999px;
      background: var(--chip);
      color: #174ea6;
      font-size: 12px;
      padding: 4px 8px;
    }}
    footer {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 8px 20px 36px;
      color: var(--muted);
      font-size: 13px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Gaia Real Skill Catalog</h1>
    <p>Curated named skills from live SKILL.md ecosystems, grouped into Gaia-friendly buckets for review before promotion into the canonical graph.</p>
  </header>
  <main>
    <h2>Sources</h2>
    <table class="source-table">
      <thead>
        <tr><th>Source</th><th>Type</th><th>Reported skills</th><th>Why it matters</th></tr>
      </thead>
      <tbody>
        {_render_sources(catalog)}
      </tbody>
    </table>
    {buckets}
  </main>
  <footer>Generated from graph/real_skill_catalog.json on {generated_at}. Edit the JSON source, then run python3 scripts/generateProjections.py.</footer>
</body>
</html>
"""


def _render_markdown(catalog):
    sources = _source_by_id(catalog)
    lines = [
        "# Gaia Real Skill Catalog",
        "",
        "Curated named skills from live SKILL.md ecosystems, grouped into Gaia-friendly buckets for review before promotion into the canonical graph.",
        "",
        "## Sources",
        "",
        "| Source | Type | Reported skills | Notes |",
        "|---|---|---:|---|",
    ]
    for source in catalog.get("sources", []):
        lines.append(
            f"| [{source.get('name')}]({source.get('url')}) | {source.get('type')} | "
            f"{source.get('reportedSkillCount', '')} | {source.get('notes', '')} |"
        )

    for bucket in catalog.get("buckets", []):
        lines.extend(["", f"## {bucket.get('name')}", "", bucket.get("summary", ""), ""])
        for item in bucket.get("items", []):
            source = sources.get(item.get("sourceId"), {})
            link = item.get("detailUrl") or item.get("sourceUrl") or source.get("url", "")
            maps_to = ", ".join(f"`{skill}`" for skill in item.get("mapsToGaia", []))
            path = item.get("path")
            path_text = f" Path: `{path}`." if path else ""
            lines.append(
                f"- [{item.get('name')}]({link}) - {item.get('description')} "
                f"Source: {source.get('name', item.get('sourceId'))}.{path_text} Maps to: {maps_to}."
            )
    lines.extend(["", f"*Generated from graph/real_skill_catalog.json on {catalog.get('updatedAt', 'unknown')}.*", ""])
    return "\n".join(lines)


def generate_catalog_pages(catalog: Dict, output_dir: str = ".") -> Tuple[str, str]:
    os.makedirs(output_dir, exist_ok=True)
    html_path = os.path.join(output_dir, "real-skills.html")
    md_path = os.path.join(output_dir, "real-skills.md")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(_render_html(catalog))
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(_render_markdown(catalog))

    return html_path, md_path


def main():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    html_path, md_path = generate_catalog_pages(catalog)
    print(f"Generated {html_path} and {md_path}.")


if __name__ == "__main__":
    main()
