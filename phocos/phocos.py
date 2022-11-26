from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime
from collections import defaultdict

EMAIL = ''
PASSWORD = ''

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://cloud.phocos.com/login")
    page.get_by_placeholder("email address").fill(EMAIL)
    page.get_by_placeholder("email address").press("Tab")
    page.get_by_placeholder("password").fill(PASSWORD)
    page.get_by_placeholder("password").press("Enter")
    print("logged in")
    page.get_by_role("heading", name="State of Charge").click()


    page.mouse.wheel(0, 15000)
    page.get_by_role("heading", name="State of Charge").click()
    page.goto("https://cloud.phocos.com/d/lB2qKFvMz/phocoslink-cloud?orgId=207&refresh=5m&viewPanel=357&inspect=357&inspectTab=data")
    print("loaded dashboard")
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Download CSV").click()
    download = download_info.value
    print(download)
    path = download.path()
    save_name = datetime.utcnow()
    save_name = f'csvs/{save_name}-operation-mode.csv'
    download.save_as(save_name)
    print(download.url, path)
    with open(save_name) as f:
        lines = f.read().strip().split("\n")
    lines = lines[-3:]
    print(lines)
    # ['2022-11-13 17:00:00,Grid', '2022-11-13 17:15:00,Grid', '2022-11-13 17:30:00,']

    keys = ['pprevious', 'previous', 'latest']
    d = defaultdict(dict)
    for i, k in enumerate(keys):
        ts, value = lines[i].split(",")
        d[k]["ts"] = ts
        d[k]["value"] = value
    d = dict(d)
    print(d)
    context.close()
    browser.close()
    return d

def get_latest_status():
    with sync_playwright() as playwright:
        d = run(playwright)
    return d

if __name__ == '__main__':
    get_latest_status()
