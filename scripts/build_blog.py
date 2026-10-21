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
		<link rel="icon" href="{root}favicon.ico?v=2" sizes="any">
		<link rel="icon" type="image/png" href="{root}images/favicon-32.png?v=2" sizes="32x32">
		<link rel="apple-touch-icon" href="{root}images/apple-touch-icon.png?v=2">
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Cinzel:wght@500&display=swap">
		<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/css/uikit.min.css" />
		<link rel="stylesheet" href="{root}assets/css/landing.css?v=30">
	</head>
	<body>
		<div class="page-wrapper">
			<header class="page-header" uk-sticky>
				<div class="uk-container uk-container-xlarge">
					<div class="page-header__inner">
						<div class="page-header__logo">
							<a class="brand-logo" href="{root}index.html" aria-label="Novadent"><span class="brand-nova">NOVA</span><span class="brand-dent">DENT</span></a>
						</div>
						<div class="page-header__scroll-menu">
							<ul class="mainmenu">
								<li><a href="{root}index.html#about">Про нас</a></li>
								<li><a href="{root}index.html#services">Послуги</a></li>
								<li><a href="{root}index.html#faq">Часті запитання</a></li>
								<li><a href="{root}blog/index.html">Блог</a></li>
								<li><a href="{root}index.html#prices">Ціни</a></li>
								<li><a href="#contact">Контакти</a></li>
							</ul>
						</div>
						<div class="page-header__right">
							<a class="header-address" href="https://www.google.com/maps/search/?api=1&amp;query=%D0%92%D1%96%D0%BD%D0%BD%D0%B8%D1%86%D1%8F%2C+%D0%B2%D1%83%D0%BB.+%D0%93%D0%BE%D0%B3%D0%BE%D0%BB%D1%8F%2C+15" target="_blank" rel="noopener noreferrer"><span class="header-address__city">м. Вінниця</span><span class="header-address__street">вул. Гоголя 15</span></a>
							<div class="page-header__phones">
								<a class="phone phone--desktop" href="tel:+380751777567">075 177 75 67</a>
								<a class="phone phone--mobile" href="tel:+380751777567" aria-label="Зателефонувати: 075 177 75 67">
									<svg width="40" height="40" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M7 3.5h2.2l1.2 3-1.6 1a12.5 12.5 0 0 0 6.7 6.7l1-1.6 3 1.2V18a1.5 1.5 0 0 1-1.6 1.5A15.5 15.5 0 0 1 4.5 5.1 1.5 1.5 0 0 1 6 3.5H7Z" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/></svg>
								</a>
							</div>
							<div class="page-header__menu">
								<a class="icon-button" href="#offcanvas" uk-toggle aria-label="Меню">
									<svg width="46" height="46" viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M6 9h20M6 16h20M6 23h20" stroke="#111" stroke-width="1.8" stroke-linecap="round"/></svg>
								</a>
							</div>
						</div>
					</div>
				</div>
			</header>
			<main class="page-main" id="top">
				<section class="blog-section">
					<div class="uk-container uk-container-xlarge">
						<div class="blog-panel">
							{content}
						</div>
					</div>
				</section>
				<section class="contact-section" id="contact">
					<div class="contact-layout">
						<div class="contact-copy">
							<h2 class="uk-h1">Контакти</h2>
							<p class="contact-facts">
								<strong>Адреса:</strong><br>
								<a href="https://www.google.com/maps/search/?api=1&amp;query=%D0%92%D1%96%D0%BD%D0%BD%D0%B8%D1%86%D1%8F%2C+%D0%B2%D1%83%D0%BB.+%D0%93%D0%BE%D0%B3%D0%BE%D0%BB%D1%8F%2C+15" target="_blank" rel="noopener noreferrer">Вінниця, вул. Гоголя 15</a><br>
								<a href="tel:+380751777567">075 177 75 67</a>
							</p>
							<p class="contact-facts">
								<strong>Графік роботи:</strong><br>
								Пн-пт: 9.00–18.00<br>
								Сб: 9.00–15.00<br>
								Нд: вихідний
							</p>
							<p><a class="uk-button" href="https://www.google.com/maps/dir/?api=1&amp;destination=%D0%92%D1%96%D0%BD%D0%BD%D0%B8%D1%86%D1%8F%2C+%D0%B2%D1%83%D0%BB.+%D0%93%D0%BE%D0%B3%D0%BE%D0%BB%D1%8F%2C+15" target="_blank" rel="noopener noreferrer">Прокласти маршрут</a></p>
						</div>
						<div class="contact-map">
							<iframe title="Novadent на карті — Вінниця, Гоголя 15" src="https://maps.google.com/maps?q=%D0%92%D1%96%D0%BD%D0%BD%D0%B8%D1%86%D1%8F%2C+%D0%93%D0%BE%D0%B3%D0%BE%D0%BB%D1%8F+15&amp;hl=uk&amp;z=16&amp;ie=UTF8&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
						</div>
					</div>
				</section>
			</main>
			<footer class="page-footer">
				<div class="uk-container uk-container-xlarge">
					<div class="page-footer__wrapper">
						<div class="page-footer__top">
							<div class="page-footer__inner">
								<div class="page-footer__logo">
									<a class="brand-logo brand-logo--footer" href="{root}index.html" aria-label="Novadent"><span class="brand-nova">NOVA</span><span class="brand-dent">DENT</span></a>
								</div>
								<div class="page-footer__contacts">
									<a class="phone-footer" href="tel:+380751777567">
										<span class="phone-footer__number">075 177 75 67</span>
									</a>
									<a class="phone-footer" href="tel:+380951877887">
										<span class="phone-footer__number">095 187 78 87</span>
									</a>
									<a class="footer-instagram" href="https://www.instagram.com/novadent_vinnytsia" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
										<svg width="34" height="34" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/></svg>
									</a>
								</div>
								<div class="page-footer__adress">
									<div class="footer-title">Контакти</div>
									<ul class="adress-list">
										<li class="adress-list__item">
											<div class="adress-list__value">
												<a href="#contact"><span>Вінниця, вул. Гоголя 15</span></a>
												<span>Пн-пт: 9:00–18:00</span>
												<span>Сб: 9:00–15:00</span>
											</div>
										</li>
									</ul>
								</div>
								<div class="page-footer__menu">
									<div class="footer-title">Пацієнтам</div>
									<ul class="footer-menu">
										<li><a href="{root}index.html#about">Про нас</a></li>
										<li><a href="{root}index.html#faq">Часті запитання</a></li>
										<li><a href="{root}blog/index.html">Блог</a></li>
										<li><a href="{root}index.html#prices">Ціни</a></li>
										<li><a href="#contact">Контакти</a></li>
									</ul>
								</div>
								<div class="page-footer__menu">
									<div class="footer-title">Послуги</div>
									<ul class="footer-menu">
										<li><a href="{root}index.html#services">Консультація</a></li>
										<li><a href="{root}index.html#services">Терапія</a></li>
										<li><a href="{root}index.html#services">Протезування</a></li>
										<li><a href="{root}index.html#services">Візіограф (рентген)</a></li>
									</ul>
								</div>
							</div>
						</div>
						<div class="page-footer__bottom">
							<ul class="footer-links">
								<li><span>© Novadent. Права захищені 2026</span></li>
							</ul>
						</div>
					</div>
				</div>
				<a class="button-to-top" href="#top" uk-scroll aria-label="Вгору">
					<svg width="28" height="28" viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M4 11.5 9 6.5l5 5" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
				</a>
			</footer>
			<div id="offcanvas" uk-offcanvas="overlay: true; flip: true; mode: slide">
				<div class="uk-offcanvas-bar">
					<div class="uk-offcanvas-header">
						<a class="brand-logo" href="{root}index.html" uk-toggle="target: #offcanvas" aria-label="Novadent"><span class="brand-nova">NOVA</span><span class="brand-dent">DENT</span></a>
						<button class="menu-close uk-offcanvas-close" type="button" aria-label="Закрити">
							<svg width="34" height="34" viewBox="0 0 22 22" fill="none" aria-hidden="true"><path d="M5 5l12 12M17 5 5 17" stroke="#111" stroke-width="1.6" stroke-linecap="round"/></svg>
						</button>
					</div>
					<div class="uk-offcanvas-body">
						<ul class="uk-nav uk-nav-default">
							<li><a href="{root}index.html#about" uk-toggle="target: #offcanvas">Про нас</a></li>
							<li><a href="{root}index.html#services" uk-toggle="target: #offcanvas">Послуги</a></li>
							<li><a href="{root}index.html#faq" uk-toggle="target: #offcanvas">Часті запитання</a></li>
							<li><a href="{root}blog/index.html" uk-toggle="target: #offcanvas">Блог</a></li>
							<li><a href="{root}index.html#prices" uk-toggle="target: #offcanvas">Ціни</a></li>
							<li><a href="{root}index.html#contact" uk-toggle="target: #offcanvas">Контакти</a></li>
						</ul>
					</div>
					<div class="uk-offcanvas-foot">
						<a class="offcanvas-book" href="tel:+380751777567">
							<span>Записатися</span>
							<svg width="26" height="26" viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M4 14 14 4M7 4h7v7" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
						</a>
						<a class="offcanvas-phone" href="tel:+380751777567">075 177 75 67</a>
						<a class="offcanvas-instagram" href="https://www.instagram.com/novadent_vinnytsia" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
							<svg width="34" height="34" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/></svg>
						</a>
					</div>
				</div>
			</div>
		</div>
		<div class="page-footer-buttons">
			<a class="page-footer-button" href="tel:+380751777567">
				<svg width="32" height="32" viewBox="0 0 22 22" fill="none" aria-hidden="true"><path d="M6.4 3.2h2l1.1 2.8-1.5.9a11.4 11.4 0 0 0 6.1 6.1l.9-1.5 2.8 1.1v2a1.4 1.4 0 0 1-1.5 1.4A14.2 14.2 0 0 1 4.9 4.7a1.4 1.4 0 0 1 1.5-1.5Z" stroke="#333" stroke-width="1.6" stroke-linejoin="round"/></svg>
				<span>075 177 75 67</span>
			</a>
		</div>
		<script src="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit.min.js"></script>
		<script src="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit-icons.min.js"></script>
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


def asset(src, root):
    if src.startswith("/"):
        return root + src[1:]
    return src


def page(title, description, content, root):
    return SHELL.format(
        title=html.escape(title),
        description=html.escape(description),
        content=content,
        root=root,
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
    article_root = "../../"
    for item in posts:
        image = ""
        if item["image"]:
            src = asset(item["image"] if item["image"].startswith("/") else f"/{item['image']}", article_root)
            image = f'<img class="blog-cover" src="{html.escape(src)}" alt="">'
        when = f"<time>{html.escape(item['date_label'])}</time>" if item["date_label"] else ""
        body = item["html"].replace('src="/', f'src="{article_root}')
        items.append(
            f'<li><a href="articles/{html.escape(item["slug"])}.html">{when}'
            f'<span>{html.escape(item["title"])}</span></a></li>'
        )
        article = (
            f'<p><a href="../index.html">Блог</a></p>'
            f'<h1 class="uk-h1">{html.escape(item["title"])}</h1>'
            f'{when}'
            f'{image}'
            f'<div class="blog-article">{body}</div>'
        )
        target = ARTICLES / f"{item['slug']}.html"
        target.write_text(
            page(f"{item['title']} — Novadent", item["description"] or item["title"], article, article_root),
            encoding="utf-8",
        )

    if items:
        listing = '<h1 class="uk-h1">Блог</h1><ul class="blog-list">' + "".join(items) + "</ul>"
    else:
        listing = '<h1 class="uk-h1">Блог</h1><p>Поки що немає записів.</p>'
    INDEX.write_text(page("Блог — Novadent", "Блог стоматології Novadent у Вінниці.", listing, "../"), encoding="utf-8")


if __name__ == "__main__":
    main()
