from fake_useragent import UserAgent
from selectolax.parser import HTMLParser
from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import time
import requests
import sqlite3
from sqlite3 import Error

COLES_IGNORED_CATEGORIES = ['specials', 'down down', 'bonus bbq credits']
COLES_DOMAIN = "https://www.coles.com.au"
SQLITE3_DB_FILE = "web_scraping.db"
PROXIES_TABLE = "Proxies"


proxy_webpage = "https://github.com/TheSpeedX/PROXY-List/blob/master/socks5.txt"
# download_proxies_list_df_from_github(proxy_webpage)


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn


def download_proxies_list_df_from_github(proxies_list_df_address="https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"):
    conn = create_connection(SQLITE3_DB_FILE)
    if conn is not None:
        # Check if the function was run today
        try:
            existing_proxies_list_df = pd.read_sql_query(
                f"SELECT * from {PROXIES_TABLE}", conn)
            last_run = datetime.strptime(
                existing_proxies_list_df["timestamp"].max(), '%Y-%m-%d %H:%M:%S')
            if last_run.date() == datetime.today().date():
                print("The function was run today. No need to run again.")
                return
        except Error as e:
            print("Table not found, will be created.")

    proxies_list_df_address = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"

    response = requests.get(proxies_list_df_address)
    data = response.text.splitlines()

    # Convert list to DataFrame with the first column named "proxy", second column named "healthy" and third column named "timestamp"
    new_proxies_list_df = pd.DataFrame(data, columns=["proxy"])
    new_proxies_list_df["healthy"] = None
    new_proxies_list_df["timestamp"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")

    # Concatenate the new data with the existing data
    if 'existing_proxies_list_df' in locals():
        proxies_list_df = pd.concat(
            [existing_proxies_list_df, new_proxies_list_df])
    else:
        proxies_list_df = new_proxies_list_df

    # Save DataFrame to SQLite database
    proxies_list_df.to_sql(PROXIES_TABLE, conn,
                           if_exists='append', index=False)
    conn.close()


# Connect to the SQLite database
conn = create_connection(SQLITE3_DB_FILE)

# Create table CATERGORIES_PAGE_DATA in web_scraping.db if it doesn't exist
with conn:
    conn.execute(f"""CREATE TABLE IF NOT EXISTS CATERGORIES_PAGE_DATA (
        category TEXT,
        page_count INTEGER,
        html TEXT,
        timestamp TEXT
    )""")

    conn.commit()

download_proxies_list_df_from_github()


# Extract the whole rows of the table into a DataFrame
proxies_list_df = pd.read_sql_query(
    f"SELECT * from {PROXIES_TABLE}", conn)

print(proxies_list_df)

# # # Read parquet file to DataFrame
# # proxies_list_df = pd.read_parquet("proxies.parquet")

# # Print number of proxies with healthy!=False in the proxies_list_df
# print(
#     f"Number of potential proxies is: {len(proxies_list_df[proxies_list_df['healthy'] != False])}")


# def close_browser_and_context(browser, context):
#     if context is not None:
#         context.close()
#     if browser is not None:
#         browser.close()


# def get_category_urls(page):
#     html = page.content()
#     parser = HTMLParser(html)
#     categories = parser.css("a[data-testid='category-card']")
#     category_urls = {}
#     for category in categories:
#         category_text = category.attributes["aria-label"].split(
#             "/")[-1].lower()
#         if category_text not in COLES_IGNORED_CATEGORIES:
#             category_url = f"{COLES_DOMAIN}{category.attributes['href']}"
#             category_urls[category_text] = category_url
#     return category_urls


# def process_category_page(page, category_urls):

#     categories_dict = {}
#     for category, category_url in category_urls.items():
#         safe_goto(page, category_url)
#         page_count = 0
#         categories_dict[category] = []
#         while True:
#             page.mouse.wheel(0, 10000)
#             html_parser = HTMLParser(page.content())
#             products_html = html_parser.css(
#                 "#coles-targeting-product-tiles")[0].html
#             page_count += 1
#             categories_dict[category].append([datetime.now(),
#                                               page_count,
#                                               products_html])
#             print(categories_dict)
#             input("Press any key to continue...")
#             next_page_button = page.get_by_label("Go to next page")
#             if next_page_button:
#                 next_page_button.click()
#             else:
#                 break
#     return categories_dict


# class AccessDeniedException(Exception):
#     pass


# def safe_goto(page, url):
#     page.goto(url)
#     if "<h1>You can't access Coles from your current location</h1>" in page.content():
#         raise AccessDeniedException("Access to Coles denied")


# # Create a Playwright object
# with sync_playwright() as p:

#     # Create a UserAgent object
#     ua = UserAgent()

#     # Iterate over the DataFrame rows as namedtuples
#     for row in proxies_list_df.itertuples():
#         browser = None
#         context = None  # Initialize context here
#         try:
#             # Only process the row if 'healthy' is not False
#             if row.healthy != False:
#                 # Launch the browser with the proxy
#                 browser = p.chromium.launch(
#                     proxy={"server": f'http://{row.proxy}'},
#                     headless=False, slow_mo=50)

#                 # Create a new context with ignoreHTTPSErrors set to True
#                 context = browser.new_context(
#                     ignore_https_errors=True, user_agent=ua.random)

#                 # This is for turning off the geolocation permission
#                 context.grant_permissions([])

#                 page = context.new_page()
#                 page.on("dialog", lambda dialog: dialog.dismiss())

#                 # Set a fake user agent
#                 page.set_default_navigation_timeout(120 * 1000)
#                 safe_goto(page, "https://www.coles.com.au/browse")

#                 try:
#                     page.get_by_role(
#                         "heading", name="Discover the latest products").click()
#                     page.get_by_label("close popup").click()
#                 except Exception:
#                     print("No popup found")

#                 category_urls = get_category_urls(page)

#                 category_dict = process_category_page(page, category_urls)

#                 print(f"Proxy {row.proxy} is healthy")

#                 # Update the 'healthy' column to True if the page navigation is successful
#                 proxies_list_df.loc[row.Index, 'healthy'] = True
#                 html_parser = HTMLParser(page.content())
#                 # Wait for the user to press a key before continuing
#                 input("Press any key to continue...")
#                 break

#         except TimeoutError:
#             print(f"Proxy {row.proxy}: Timeout error")
#             proxies_list_df.loc[row.Index, 'healthy'] = False
#             close_browser_and_context(browser, context)
#         except Exception as e:
#             print(f"Proxy {row.proxy}: Unexpected error: {e}")
#             proxies_list_df.loc[row.Index, 'healthy'] = False
#             close_browser_and_context(browser, context)
#         finally:
#             close_browser_and_context(browser, context)

#     # Save the updated DataFrame back to the parquet file
#     proxies_list_df.to_parquet("proxies.parquet", index=False)

#     print(html_parser)
