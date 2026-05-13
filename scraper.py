import json
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

BASE_URL = "https://ekantipur.com/"
ENTERTAINMENT_URL = urljoin(BASE_URL, "entertainment")
CARTOON_URL = urljoin(BASE_URL, "cartoon")


def fetch_entertainment_news(limit=5):
	news_items = []
	with sync_playwright() as p:
		browser = p.chromium.launch(headless=True)
		page = browser.new_page()
		page.goto(ENTERTAINMENT_URL, wait_until="domcontentloaded")

		# Cards live under the main wrapper; slice to the top 5 only.
		items = page.locator("div.category-main-wrapper div.category").all()[:limit]

		for item in items:
			# Guard each lookup to avoid crashes on missing nodes.

			title_locator = item.locator("h2 a")
			title = title_locator.text_content().strip() if title_locator.count() else None

			author_locator = item.locator("div.author-name")
			author = None
			if author_locator.count():
				author_text = author_locator.text_content().strip()
				author = author_text if author_text else None

			image_locator = item.locator("div.category-image img")
			image_url = None
			if image_locator.count():
				# Some cards use lazy-loaded attributes or srcset instead of src.
				src = (
					image_locator.get_attribute("src")
					or image_locator.get_attribute("data-src")
					or image_locator.get_attribute("data-original")
				)
				if not src:
					srcset = image_locator.get_attribute("srcset")
					if srcset:
						src = srcset.split(",")[0].strip().split(" ")[0]
				if src:
					image_url = urljoin(BASE_URL, src)

			news_items.append(
				{
					"title": title,
					"image_url": image_url,
					"category": "मनोरञ्जन",
					"author": author,
				}
			)

		browser.close()

	return news_items


def _cartoon_title_and_author(raw_title):

	if not raw_title:
		return None, None
	s = raw_title.strip()
	if "-" not in s:
		return s, None
	head, tail = s.rsplit("-", 1)
	head = head.strip()
	tail = tail.strip()
	title = head if head else s
	if tail:
		return title, tail
	return title, None


def fetch_cartoon_of_the_day():
	"""Scrape the primary cartoon block from the cartoon listing page."""
	with sync_playwright() as p:
		browser = p.chromium.launch(headless=True)
		page = browser.new_page()
		page.goto(CARTOON_URL, wait_until="domcontentloaded")

		section = page.locator("div.cartoon-wrapper").first
		title = None
		image_url = None
		author = None

		if section.count():
			title_locator = section.locator("div.cartoon-description p").first
			raw_title = None
			if title_locator.count():
				t = title_locator.text_content()
				raw_title = t.strip() if t else None

			title, author = _cartoon_title_and_author(raw_title)

			image_locator = section.locator("div.cartoon-image img").first
			if image_locator.count():
				src = (
					image_locator.get_attribute("src")
					or image_locator.get_attribute("data-src")
					or image_locator.get_attribute("data-original")
				)
				if not src:
					srcset = image_locator.get_attribute("srcset")
					if srcset:
						src = srcset.split(",")[0].strip().split(" ")[0]
				if src:
					image_url = urljoin(BASE_URL, src)

		browser.close()

	return {
		"title": title,
		"image_url": image_url,
		"author": author,
	}


if __name__ == "__main__":
	payload = {
		"entertainment_news": fetch_entertainment_news(),
		"cartoon_of_the_day": fetch_cartoon_of_the_day(),
	}
	with open("output.json", "w", encoding="utf-8") as f:
		json.dump(payload, f, ensure_ascii=False, indent=2)

