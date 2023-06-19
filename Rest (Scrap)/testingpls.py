from googleapiclient.discovery import build
import requests
from PIL import Image
from io import BytesIO

# Set your Custom Search Engine ID and API key
cx = 'c6181f801ca8b4273'
api_key = 'AIzaSyBlX2U4hnPnK6F3vsVRl54ai9RnKc21MkE'


def search_images(query):
    # Build the service object for the Custom Search JSON API
    service = build('customsearch', 'v1', developerKey=api_key)

    # Execute a search query
    response = service.cse().list(
        cx=cx,
        q=query,
        searchType='image',
        num=1  # Number of images to retrieve
    ).execute()

    # Extract the image URL from the response
    if 'items' in response:
        image_url = response['items'][0]['link']
        return image_url

    return None


def display_basketball_player_image(player_name):
    # Perform a search for the player's image
    query = player_name + ' basketball player'
    image_url = search_images(query)

    return image_url


# Example usage
player_name = "LeBron James"
print(display_basketball_player_image(player_name))
