import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("movie_api_key")


def search_movie(name):
    movie = f"http://www.omdbapi.com/?apikey={api_key}&t={name}"
    movie_data = requests.get(movie)
    return movie_data.json()




