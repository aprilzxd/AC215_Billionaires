import requests

def test_agent_chat_endpoint():
    # Define the API URL
    url = "http://api-container:8001/agent/chat"

    # Define the payload as a dictionary
    payload = {
        "prompt": "test message",
        "stream": False
    }

    # Send the POST request
    response = requests.post(url, json=payload)

    # Parse the response
    result = response.json()

    # Assertions to check the response
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "response" in result, f"Expected key 'response' in response, got {result}"
    assert isinstance(result["response"], str), "Expected 'response' to be a string"