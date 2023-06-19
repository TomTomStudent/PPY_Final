from matplotlib import font_manager
import pandas as pd
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplcursors
import sys
import requests
from PIL import Image, ImageTk, UnidentifiedImageError
from io import BytesIO
from googleapiclient.discovery import build
import io


def get_player_info(player_name):
    csv_files = ['Data\\NBA player 2022-2023.csv',
                 'Data\\NBA player 2021-2022.csv', 'Data\\NBA player 2020-2021.csv']
    player_info = []

    for csv_file in csv_files:
        data = pd.read_csv(csv_file)
        matching_rows = data[data['Player'] == player_name]
        for _, row in matching_rows.iterrows():
            player_info.append(row)

    return player_info


def get_sus_player(player_name):
    player_info = []
    data = pd.read_csv('Data\\pure_efficiency_stats_22_23.csv')
    matching_rows = data[data['Player'] == player_name]
    for _, row in matching_rows.iterrows():
        player_info.append(row)

    # for x in player_info:
    #     print(x)
    return player_info


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

# player_name = "LeBron James"
# print(display_basketball_player_image(player_name))
