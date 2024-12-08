import requests
import plotly.graph_objects as go

# Define the endpoint and query parameters
url = "http://127.0.0.1:8001/plot_stock_prices"
params = {
    "companies": "NVDA",
    "start_date": "2024-11-18",
    "end_date": "2024-11-22"
}

# Make the GET request
try:
    plot_response = requests.get(url, params=params)

    # Check if the request was successful
    if plot_response.status_code == 200:
        # Extract the JSON response
        fig_json = plot_response.json()

        # Flatten the y values in case they are nested lists
        for trace in fig_json['data']:
            if isinstance(trace['y'], list) and isinstance(trace['y'][0], list):
                trace['y'] = [item[0] for item in trace['y']]

        # Create the Plotly figure from the JSON data
        fig = go.Figure(data=fig_json.get("data", []), layout=fig_json.get("layout", {}))

        # Show the plot
        fig.show()

    else:
        print(f"Failed to fetch plot data. HTTP Status Code: {plot_response.status_code}")
        print(f"Response: {plot_response.text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
