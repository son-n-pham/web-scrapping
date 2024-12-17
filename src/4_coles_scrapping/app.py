from playwright.sync_api import Playwright, sync_playwright
from selectolax.parser import HTMLParser
from datetime import datetime
import time

COLES_IGNORED_CATEGORIES = ['specials', 'down down', 'bonus bbq credits']
COLES_DOMAIN = "https://www.coles.com.au"


def get_category_urls(page):
    html = page.content()
    parser = HTMLParser(html)
    categories = parser.css("a[data-testid='category-card']")
    category_urls = []
    for category in categories:
        category_text = category.attributes["aria-label"].split(
            "/")[-1].lower()
        if category_text not in COLES_IGNORED_CATEGORIES:
            category_url = f"{COLES_DOMAIN}{category.attributes['href']}"
            category_urls.append(category_url)
    return category_urls


def process_category_page(page, category_url):
    page.goto(category_url)
    page_count = 0
    categories_dict = {}
    while True:
        page.mouse.wheel(0, 10000)
        products_html = page.query_selector(
            "#coles-targeting-product-tiles").inner_html()
        page_count += 1
        categories_dict[category_url] = [datetime.now(), page, products_html]
        print(categories_dict)
        time.sleep(30)
        next_page_button = page.get_by_label("Go to next page")
        if next_page_button:
            next_page_button.click()
        else:
            break


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context()

    # This is for turning off the geolocation permission
    context.grant_permissions([])
    # context.grant_permissions([], origin="https://www.coles.com.au")
    page = context.new_page()
    page.on("dialog", lambda dialog: dialog.dismiss())

    page.goto("https://www.coles.com.au/browse")

    try:
        page.get_by_role(
            "heading", name="Discover the latest products").click()
        page.get_by_label("close popup").click()
    except Exception:
        print("No popup found")

    category_urls = get_category_urls(page)
    for category_url in category_urls:
        process_category_page(page, category_url)

    time.sleep(600)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
