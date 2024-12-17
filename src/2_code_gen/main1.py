

# //*[@id="__next"]/div/main/div/div/div/div/p[2]
# #__next > div > main > div > div > div > div > p:nth-child(4)

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demo.vuestorefront.io/")
    page.get_by_test_id("category-index-link").click()
    page.get_by_role("link", name="Men ( 633 )").click()
    page.get_by_role("link", name="Shoes ( 116 )").click()
    page.locator(".relative > a").first.click()
    page.get_by_test_id("quantitySelectorIncreaseButton").click()
    page.get_by_test_id("addToCartButton").click()
    page.get_by_test_id("cart-action").get_by_test_id("button").click()
    page.get_by_test_id("goToCheckout").click()
    page.get_by_test_id(
        "contact-information").get_by_test_id("addButton").click()
    page.get_by_test_id(
        "contact-information-form").get_by_test_id("input-field").click()
    page.get_by_test_id(
        "contact-information-form").get_by_test_id("input-field").fill("fake@gmail.com")
    page.get_by_test_id("save").click()
    page.get_by_role("button", name="Add billing address").click()
    page.get_by_test_id("firstNameInput").click()
    page.get_by_test_id("firstNameInput").fill("fake")
    page.get_by_test_id("firstNameInput").press("Tab")
    page.get_by_test_id("lastNameInput").fill("name")
    page.locator("label").filter(
        has_text="Phone").get_by_test_id("input").click()
    page.get_by_test_id("phoneInput").fill("432534")
    page.get_by_test_id("streetNameInput").click()
    page.get_by_test_id("streetNameInput").fill("12321 fsdgfs")
    page.get_by_test_id("cityInput").click()
    page.get_by_test_id("cityInput").fill("dfa")
    page.get_by_test_id("postalCodeInput").click()
    page.get_by_test_id("postalCodeInput").fill("32543")
    page.get_by_text("State-- Select --California").click()
    page.get_by_test_id("stateSelect").select_option("California")
    page.get_by_text("Use as shipping address").click()
    page.get_by_test_id("save").click()
    page.get_by_role("button", name="Credit Card").click()
    page.frame_locator("iframe[name=\"__privateStripeFrame6517\"]").get_by_text(
        "Card numberSelect card brand").click()
    page.frame_locator("iframe[name=\"__privateStripeFrame6517\"]").get_by_placeholder(
        "1234 1234 1234").click()
    page.frame_locator("iframe[name=\"__privateStripeFrame6517\"]").get_by_placeholder(
        "1234 1234 1234").fill("4111 1111 1111")
    page.frame_locator("iframe[name=\"__privateStripeFrame6517\"]").get_by_placeholder(
        "MM / YY").click()
    page.frame_locator("iframe[name=\"__privateStripeFrame6517\"]").get_by_placeholder(
        "1234 1234 1234").click()
    page.frame_locator("iframe[name=\"__privateStripeFrame6517\"]").get_by_placeholder(
        "1234 1234 1234").fill("4111 1111 1111 1111")
    page.frame_locator("iframe[name=\"__privateStripeFrame6517\"]").get_by_placeholder(
        "MM / YY").click()
    page.frame_locator("iframe[name=\"__privateStripeFrame6517\"]").get_by_placeholder(
        "MM / YY").fill("02 / 26")
    page.frame_locator("iframe[name=\"__privateStripeFrame6517\"]").get_by_placeholder(
        "MM / YY").press("Tab")
    page.frame_locator("iframe[name=\"__privateStripeFrame6517\"]").get_by_placeholder(
        "CVC").fill("431")
    page.get_by_test_id("placeOrder").click()
    page.get_by_text("680e4829-7c2a-4209-a3f8-").click()
    page.get_by_text(
        "Estimated delivery timetomorrowOrder number680e4829-7c2a-4209-a3f8-1231759747b1").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
