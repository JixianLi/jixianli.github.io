"""Rebuild the publication list in index.html from publication_list.csv.

usage: uv run --no-project python build_publications.py  (from the repository root)
Rows with an empty img column get no preview slot; forthcoming = yes adds a NEW! badge.
"""
import csv
import html
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
START, END = "<!--PUBLICATIONS START-->", "<!--PUBLICATIONS END-->"
LINK_COLUMNS = [("arxiv", "arxiv"), ("github", "project"), ("doi", "doi"), ("video", "video")]


def paper_item(row):
    title = html.escape(row["title"])
    authors = html.escape(row["authors"]).replace("Jixian Li", "<b>Jixian Li</b>")
    links = [f'<span class="venue">{html.escape(row["venue"])}</span>']
    links += [f'<a href="{html.escape(row[column])}">[{label}]</a>' for column, label in LINK_COLUMNS if row.get(column)]
    new_badge = '<span class="new-badge" title="Forthcoming">NEW!</span> ' if row.get("forthcoming") == "yes" else ""
    text = f'<div><p class="paper-title">{new_badge}{title}</p><p class="paper-authors">{authors}</p><p class="paper-links">{" ".join(links)}</p></div>'
    if not row["img"]:
        return f'        <li class="paper no-preview">{text}</li>'
    return f'        <li class="paper"><img src="{html.escape(row["img"])}" alt="Teaser figure for {title}">{text}</li>'


def publication_block(rows):
    by_year = defaultdict(list)
    for row in rows:
        by_year[int(row["year"])].append(row)
    parts = [START]
    for year in sorted(by_year, reverse=True):
        parts.append(f'      <p class="year-label">~*~ {year} ~*~</p>\n      <ul class="paper-list">')
        parts += [paper_item(row) for row in reversed(by_year[year])]
        parts.append("      </ul>")
    parts.append("      " + END)
    return "\n".join(parts)


def main():
    with open(HERE / "publication_list.csv", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file, skipinitialspace=True))
    page = HERE / "index.html"
    text = page.read_text()
    block = publication_block(rows)
    text, count = re.subn(re.escape(START) + ".*?" + re.escape(END), lambda match: block, text, flags=re.S)
    if count != 1:
        raise SystemExit(f"expected one {START} ... {END} block in index.html, found {count}")
    page.write_text(text)
    print(f"{len(rows)} publications written")


if __name__ == "__main__":
    main()
