import requests
import os
from dotenv import load_dotenv

# Load the .env file and make its content available as environment variables
load_dotenv()

class YouTubeAPIClient:
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self):
        # Load the API key from .env and store it in the object
        self.api_key = os.getenv("YOUTUBE_API_KEY")

    def get(self, endpoint, params):
        # Automatically attach the API key to every request
        params["key"] = self.api_key
        try:
            # Send GET request to the full URL (BASE_URL + endpoint)
            # timeout=10 means if the API doesn't respond within 10 seconds, we stop
            response = requests.get(
                f"{self.BASE_URL}/{endpoint}",
                params=params,
                timeout=10
            )
            # If response is not 200 (e.g. 403 or 404), raise an error automatically
            response.raise_for_status()
            # If everything is good , return the JSON response
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Timeout on {endpoint}")
            return None
        except requests.exceptions.HTTPError as e:
            # If the API returns an error like 403 or 404
            print(f"HTTP Error on {endpoint}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed on {endpoint}: {e}")
            return None