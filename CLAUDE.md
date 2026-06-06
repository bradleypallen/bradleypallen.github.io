# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a minimalistic personal website for Bradley P. Allen that uses GitHub Pages to serve a single-page home page. The site avoids the complexity of static site generators like Hugo or Jekyll by using a simple Python script to convert Markdown to HTML.

## Architecture

The site has a unique architecture that converts Markdown to HTML using GitHub's API:

1. **Content**: The main content is authored in `index.md` using Markdown
2. **Generation**: `generate_index_html.py` converts the Markdown to HTML by sending it to GitHub's API
3. **Styling**: The generated HTML is styled by a custom academic stylesheet, `resources/styles.css`
4. **Output**: The final HTML is written to `index.html` which serves as the homepage

`index.md` is organized as an **academic homepage**: a header (headshot + name +
affiliation + a quiet text link row), then `## About`, `## Selected Publications`,
`## Talks & Media`, and `## Personal` sections, closed by an `<hr>` and a copyright line.

**Critical constraint — pure Markdown only, layout via CSS selectors.** GitHub's Markdown
API *sanitizes* its output: it strips `class`, `id`, `style`, and most raw HTML. So
`index.md` must stay pure Markdown (no inline HTML), and `resources/styles.css` does all
layout by targeting the *element structure* GitHub generates — e.g. headings come wrapped
in `<div class="markdown-heading">…<a class="anchor">`, the leading image becomes the
first `<p>` (floated as the headshot), and the affiliation/link-row are selected via
`.markdown-heading:has(h1) + p` / `+ p + p`. When changing the header or section order in
`index.md`, re-check those structural selectors in `styles.css`. The site is a **single
light theme** — there is no dark mode or theme toggle.

## Development Commands

### Generate the Site
```bash
python generate_index_html.py
```
This command:
- Reads `index.md`
- POSTs it to GitHub's Markdown API (`https://api.github.com/markdown`)
- Wraps the returned HTML fragment with the `PREFIX`/`SUFFIX` string constants defined at the top of `generate_index_html.py` — these contain the `<head>` (charset, viewport, `<title>`, meta description, favicon, `resources/styles.css`, Google Analytics tag) and the closing `</article></body></html>`
- Writes the result to `index.html`

Note: the Markdown API is rate-limited for unauthenticated requests. The script reads `GITHUB_TOKEN` from the environment and authenticates when present (set automatically in GitHub Actions); locally it runs without a token but may hit rate limits.

### Install Dependencies
```bash
pip install -r requirements.txt
```
The only runtime dependency is `requests` (see `requirements.txt` for the pinned version). `ruff` and `mypy` are used for linting/type-checking (their cache dirs are present), but there is no test suite.

## File Structure

- `index.md` - Main content in Markdown format
- `generate_index_html.py` - Script that converts Markdown to HTML
- `index.html` - Generated HTML homepage (do not edit manually)
- `requirements.txt` - Python dependencies
- `resources/styles.css` - Custom academic stylesheet (single light theme)
- `resources/images/` - Images; `headshot.svg` is a monogram placeholder — replace with a real headshot photo
- `resources/Bradley_Allen_CV.pdf` - CV, linked from the header; refresh when the CV is updated
- `CNAME` - GitHub Pages custom domain configuration

## Development Workflow

1. Edit content in `index.md`
2. Commit and push `index.md` changes
3. GitHub Actions automatically runs `generate_index_html.py` to update `index.html`
4. GitHub Actions commits the updated `index.html` and deploys to GitHub Pages

The generated `index.html` is automatically committed by GitHub Actions and should not be edited manually.
- Always do a pull from GitHub before doing a commit and push, as GitHub Actions make changes when deployments occur.

## GitHub Actions Automation

The repository uses GitHub Actions to automate the build and deployment process:

- **Trigger**: Any push to the `master` branch
- **Process**: Automatically runs `generate_index_html.py` to convert `index.md` to `index.html`
- **Deployment**: Commits the updated HTML (as `github-actions[bot]`) and deploys to GitHub Pages
- **Manual generation**: You can still run `python generate_index_html.py` locally for testing, but it's not required for deployment

The workflow (`.github/workflows/generate_index_html.yml`) only commits when `git status --porcelain` shows changes, and includes a deliberate `sleep` before pushing the bot commit. This delay lets the initial Pages deployment start so the bot's push doesn't cancel an in-flight deployment (which previously caused spurious cancellation emails — see commit history). Do not remove the `sleep` without understanding this.