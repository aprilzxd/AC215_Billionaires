import requests
import json

def test_agent_chat_endpoint():
    # Define the API URL
    url = "http://api-service:8001/agent/chat/stream"  # use this if testing in a container

    # Define the payload as a dictionary (no 'stream' key needed since endpoint always streams)
    payload = {
        "prompt": "test message"
    }

    # Send the POST request with stream=True to handle SSE
    with requests.post(url, json=payload, stream=True) as response:
        # Check that we got a 200 OK status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        full_content = None

        # Iterate over the streaming lines
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8").strip()
                if decoded_line.startswith("data:"):
                    # Extract the JSON part after 'data:'
                    data_str = decoded_line[len("data:"):].strip()
                    data_obj = json.loads(data_str)
                    # Update the full_content as we receive more chunks
                    full_content = data_obj.get("content")

        # At the end of the stream, we should have a final full_content
        assert full_content is not None, "No content received from streaming endpoint."
        assert isinstance(full_content, str), "Expected 'content' to be a string"
        # Check that it contains some text related to the user prompt
        assert "test" in full_content.lower(), "Expected the response content to mention 'test'"
