#!/usr/bin/env python
# coding: utf-8

from requests import post
from json import dumps
from pathlib import Path
from datetime import date

PREFIX = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>Bradley P. Allen</title>
<meta name="description" content="Bradley P. Allen — researcher, INDE Lab, University of Amsterdam. Knowledge engineering in the era of large language models.">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link rel="stylesheet" href="resources/styles.css">
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-X60V83RS7W"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-X60V83RS7W');
</script>
</head>
<body>
<article class="markdown-body">
"""
SUFFIX_TEMPLATE = """
<p class="last-updated"><em>Last updated {last_updated}.</em></p>
</article>
</body>
</html>
"""


def _format_last_updated(today=None):
    today = today or date.today()
    return today.strftime("%-d %B %Y")


def generate_index_html():
    import os

    headers = {"Accept": "application/vnd.github.v3+json"}

    # Use GitHub token if available (for GitHub Actions)
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    markdown = Path("index.md").read_text()
    data = dumps({"text": markdown})
    response = post("https://api.github.com/markdown", headers=headers, data=data)

    if response.status_code != 200:
        print(f"GitHub API Error: {response.status_code}")
        print(response.text)
        exit(1)

    suffix = SUFFIX_TEMPLATE.format(last_updated=_format_last_updated())
    html = f"{PREFIX}\n{response.text}\n{suffix}"
    print(f"Stamped 'Last updated {_format_last_updated()}'.")
    Path("index.html").write_text(html)


if __name__ == "__main__":
    generate_index_html()
