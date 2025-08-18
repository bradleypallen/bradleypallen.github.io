# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a minimalistic personal website for Bradley P. Allen that uses GitHub Pages to serve a single-page home page. The site avoids the complexity of static site generators like Hugo or Jekyll by using a simple Python script to convert Markdown to HTML.

## Architecture

The site has a unique architecture that converts Markdown to HTML using GitHub's API:

1. **Content**: The main content is authored in `index.md` using Markdown
2. **Generation**: `generate_index_html.py` converts the Markdown to HTML by sending it to GitHub's API
3. **Styling**: The generated HTML includes GitHub's markdown styles via `resources/styles.css`
4. **Output**: The final HTML is written to `index.html` which serves as the homepage

## Development Commands

### Generate the Site
```bash
python generate_index_html.py
```
This command:
- Reads `index.md` 
- Converts it to HTML using GitHub's Markdown API
- Wraps it with HTML structure including CSS and Google Analytics
- Writes the result to `index.html`

### Install Dependencies
```bash
pip install -r requirements.txt
```
The only dependency is `requests==2.25.1` for making API calls to GitHub.

## File Structure

- `index.md` - Main content in Markdown format
- `generate_index_html.py` - Script that converts Markdown to HTML
- `index.html` - Generated HTML homepage (do not edit manually)
- `requirements.txt` - Python dependencies
- `resources/styles.css` - GitHub markdown styles
- `resources/images/` - Images used in the site
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
- **Deployment**: Commits the updated HTML and deploys to GitHub Pages
- **Manual generation**: You can still run `python generate_index_html.py` locally for testing, but it's not required for deployment