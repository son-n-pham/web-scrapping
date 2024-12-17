from playwright.sync_api import Playwright, sync_playwright, expect
import time


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demo.vuestorefront.io/")

    # Add this as code_gen does not record mouse movement
    page.mouse.wheel(0, 4000)

    time.sleep(2)
    page.get_by_test_id("scroll-top").get_by_test_id("button").click()
    time.sleep(4)
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
