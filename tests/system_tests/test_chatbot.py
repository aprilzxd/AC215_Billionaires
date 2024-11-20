import pytest
import json
from playwright.sync_api import sync_playwright

BASE_URL = "http://api-container:8001"
ENDPOINT = "/agent/chat"

@pytest.fixture(scope="session")
def start_streamlit():
    """Start the Streamlit app before running tests."""
    import subprocess
    import time

    process = subprocess.Popen(["streamlit", "run", "src/frontend/chat.py"])
    time.sleep(5)
    yield
    process.terminate()

@pytest.fixture(scope="function")
def page(start_streamlit):
    """Start Playwright and open the page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL + ENDPOINT)
        yield page
        browser.close()
