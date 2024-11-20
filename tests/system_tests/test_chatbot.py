import pytest
import json
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8501"  # Replace with the Streamlit app URL

@pytest.fixture(scope="session")
def start_streamlit():
    """Start the Streamlit app before running tests."""
    import subprocess
    import time

    process = subprocess.Popen(["streamlit", "run", "app.py"])  # Replace 'app.py' with your Streamlit script
    time.sleep(5)  # Give time for the app to start
    yield
    process.terminate()

@pytest.fixture(scope="function")
def page(start_streamlit):
    """Start Playwright and open the page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL)
        yield page
        browser.close()

def test_ui_loads(page):
    """Test that the chatbot UI loads properly."""
    assert page.title() == "Finance Chatbot"
    assert page.locator("text=Finance Chatbot").is_visible()
    assert page.locator("text=Ask about stocks, company info, or financial news...").is_visible()

def test_user_input_submission(page):
    """Test user input submission and message display."""
    user_message = "What is the stock price of AAPL?"
    page.fill("textarea", user_message)  # Locate the input box and type a message
    page.press("textarea", "Enter")  # Simulate pressing Enter

    # Verify that the user message is displayed
    assert page.locator("text=What is the stock price of AAPL?").is_visible()

def test_backend_integration(page, mocker):
    """Test backend integration with a mocked API."""
    # Mock the backend API response
    mock_response = {"response": ["The current price of AAPL is $150."]}
    mocker.patch("requests.post", return_value=mock_response)

    user_message = "What is the stock price of AAPL?"
    page.fill("textarea", user_message)
    page.press("textarea", "Enter")

    # Verify the assistant's response is displayed
    assert page.locator("text=The current price of AAPL is $150.").is_visible()

def test_error_handling(page, mocker):
    """Test error handling when the API fails."""
    # Simulate an API failure
    mocker.patch("requests.post", side_effect=Exception("API is down"))

    user_message = "What is the stock price of AAPL?"
    page.fill("textarea", user_message)
    page.press("textarea", "Enter")

    # Verify that an error message is displayed or the app doesn't crash
    assert page.locator("text=Error occurred").is_visible()  # Replace with actual error message logic

def test_plot_rendering(page, mocker):
    """Test that stock plotting works."""
    # Mock the API response for stock plot instructions
    mock_response = {
        "response": [
            json.dumps(
                {
                    "companies": ["AAPL"],
                    "start_date": "2023-01-01",
                    "end_date": "2023-03-31",
                }
            )
        ]
    }
    mocker.patch("requests.post", return_value=mock_response)

    user_message = "Show me the stock price of AAPL for the last 3 months."
    page.fill("textarea", user_message)
    page.press("textarea", "Enter")

    # Verify that a plot is rendered
    assert page.locator("text=AAPL Stock Prices").is_visible()  # Replace with actual plot title or identifier
