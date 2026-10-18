#!/usr/bin/env python3
"""Build static blog pages from Markdown posts saved by Sveltia CMS."""

import html
import re
from datetime import datetime
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "blog" / "posts"
ARTICLES = ROOT / "blog" / "articles"
INDEX = ROOT / "blog" / "index.html"

SHELL = """<!DOCTYPE html>
<html lang="uk">
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<title>{title}</title>
		<meta name="description" content="{description}" />
		<link rel="icon" href="/favicon.ico?v=2" sizes="any">
		<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/css/uikit.min.css" />
		<link rel="stylesheet" href="/assets/css/landing.css?v=28">
	</head>
	<body>
		<div class="page-wrapper">
			<header class="page-header" uk-sticky>
				<div class="uk-container uk-container-xlarge">
					<div class="page-header__inner">
						<div class="page-header__logo">
							<a class="brand-logo" href="/" aria-label="Novadent"><span class="brand-nova">NOVA</span><span class="brand-dent">DENT</span></a>
						</div>
						<div class="page-header__scroll-menu">
							<ul class="mainmenu">
								<li><a href="/#about">Про нас</a></li>
								<li><a href="/#services">Послуги</a></li>
								<li><a href="/blog/">Блог</a></li>
								<li><a href="/#prices">Ціни</a></li>
								<li><a href="/#contact">Контакти</a></li>
							</ul>
						</div>
						<div class="page-header__right">
							<a class="header-address" href="https://www.google.com/maps/search/?api=1&amp;query=%D0%92%D1%96%D0%BD%D0%BD%D0%B8%D1%86%D1%8F%2C+%D0%B2%D1%83%D0%BB.+%D0%93%D0%BE%D0%B3%D0%BE%D0%BB%D1%8F%2C+15" target="_blank" rel="noopener noreferrer"><span class="header-address__city">м. Вінниця</span><span class="header-address__street">вул. Гоголя 15</span></a>
							<div class="page-header__phones">
								<a class="phone phone--desktop" href="tel:+380751777567">075 177 75 67</a>
							</div>
						</div>
					</div>
				</div>
			</header>
			<main class="page-main">
				<section class="blog-section">
					<div class="uk-container uk-container-xlarge">
						{content}
					</div>
				</section>
			</main>
			<footer class="page-footer">
				<div class="uk-container uk-container-xlarge">
					<div class="page-footer__wrapper">
						<div class="page-footer__bottom">
							<ul class="footer-links">
								<li><a href="/">На головну</a></li>
								<li><span>© Novadent. Права захищені 2026</span></li>
							</ul>
						</div>
					</div>
				</div>
			</footer>
		</div>
		<script src="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit.min.js"></script>
	</body>
</html>
"""


def parse_post(path):
    text = path.read_text(encoding="utf-8")
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip().strip("'\"")
            body = parts[2].strip()
    title = meta.get("title") or path.stem
    raw_date = meta.get("date", "").replace("Z", "+00:00")
    parsed = None
    if raw_date:
        try:
            parsed = datetime.fromisoformat(raw_date)
        except ValueError:
            parsed = None
    image = meta.get("image", "")
    return {
        "slug": path.stem,
        "title": title,
        "date": parsed,
        "date_label": parsed.strftime("%d.%m.%Y") if parsed else "",
        "image": image,
        "html": markdown.markdown(body, extensions=["extra", "sane_lists"]),
        "description": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", markdown.markdown(body)))[:160],
    }


def page(title, description, content):
    return SHELL.format(
        title=html.escape(title),
        description=html.escape(description),
        content=content,
    )


def main():
    posts = []
    if POSTS.exists():
        for path in sorted(POSTS.glob("*.md")):
            posts.append(parse_post(path))
    posts.sort(key=lambda item: item["date"] or datetime.min, reverse=True)

    ARTICLES.mkdir(parents=True, exist_ok=True)
    keep = {f"{item['slug']}.html" for item in posts}
    for old in ARTICLES.glob("*.html"):
        if old.name not in keep:
            old.unlink()

    items = []
    for item in posts:
        image = ""
        if item["image"]:
            src = item["image"] if item["image"].startswith("/") else f"/{item['image']}"
            image = f'<img class="blog-cover" src="{html.escape(src)}" alt="">'
        when = f"<time>{html.escape(item['date_label'])}</time>" if item["date_label"] else ""
        items.append(
            f'<li><a href="/blog/articles/{html.escape(item["slug"])}.html">{when}'
            f'<span>{html.escape(item["title"])}</span></a></li>'
        )
        article = (
            f'<p><a href="/blog/">Блог</a></p>'
            f'<h1 class="uk-h1">{html.escape(item["title"])}</h1>'
            f'{when}'
            f'{image}'
            f'<div class="blog-article">{item["html"]}</div>'
        )
        target = ARTICLES / f"{item['slug']}.html"
        target.write_text(
            page(f"{item['title']} — Novadent", item["description"] or item["title"], article),
            encoding="utf-8",
        )

    if items:
        listing = '<h1 class="uk-h1">Блог</h1><ul class="blog-list">' + "".join(items) + "</ul>"
    else:
        listing = '<h1 class="uk-h1">Блог</h1><p>Поки що немає записів.</p>'
    INDEX.write_text(page("Блог — Novadent", "Блог стоматології Novadent у Вінниці.", listing), encoding="utf-8")


if __name__ == "__main__":
    main()
