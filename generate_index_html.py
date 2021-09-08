#!/usr/bin/env python
# coding: utf-8

from requests import post
from json import dumps
from pathlib import Path

PREFIX = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="resources/styles.css">
<style>
	.markdown-body {
		box-sizing: border-box;
		min-width: 200px;
		max-width: 980px;
		margin: 0 auto;
		padding: 45px;
	}

	@media (max-width: 767px) {
		.markdown-body {
			padding: 15px;
		}
	}
</style>
<article class="markdown-body">
"""
SUFFIX = """
</article>
"""

def generate_index_html():
	headers = { "Accept": "application/vnd.github.v3+json" }
	markdown = Path("index.md").read_text()
	data = dumps({ 'text': markdown })
	response = post('https://api.github.com/markdown', headers=headers, data=data)
	html = f'{PREFIX}\n{response.text}\n{SUFFIX}'
	Path("index.html").write_text(html)

if __name__ == '__main__':
    generate_index_html()
