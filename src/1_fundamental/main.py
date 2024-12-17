# Import the necessary modules
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

# Start a new Playwright context
with sync_playwright() as p:
    # Launch a new browser instance. Here we're using Chromium (which includes Google Chrome and other browsers) and setting it to not run in headless mode (i.e., it will open a browser window so you can see what's happening)
    browser = p.chromium.launch(headless=False, slow_mo=50)

    # Open a new page in the browser
    page = browser.new_page()

    # Navigate to the specified URL
    page.goto("https://demo.opencart.com/admin/")

    # Fill the username and password fields with the specified text
    page.fill("input#input-username", "demo")
    page.fill("input#input-password", "demo")

    # Click the submit button to log in
    page.click("button[type=submit]")

    # Wait until the 'div.tile-body' element is visible on the page. This is useful for ensuring that the page has fully loaded before we try to interact with it.
    page.wait_for_selector('div.tile-body', state="visible", timeout=10000)

    # Get the HTML content of the '#content' element on the page
    html = page.inner_html("#content")

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find the 'h2' element with class 'float-end' and get its text content. This is the total number of orders.
    total_orders = soup.find("h2", {"class": "float-end"}).text
    print(total_orders)

    # Get the directory that contains the current script
    code_folder = os.path.dirname(os.path.abspath(__file__))

    # Construct the path where the screenshot will be saved
    screenshot_path = os.path.join(code_folder, "example_1.png")

    # Take a screenshot of the page and save it to the specified path
    page.screenshot(path=screenshot_path)
