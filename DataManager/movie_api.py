"""
movie_api: A Python module for accessing movie data using the OMDb API.

This module provides a function to search for movie data using the OMDb API.
The OMDb API allows you to retrieve information about movies such as their title,
director, year of release, rating, and more.

Requirements:
    - requests: This module uses the 'requests' library to send HTTP requests to the API.
    - python-dotenv: This module uses 'python-dotenv' to load environment variables from a .env file.

Usage:
    1. Before using this module, make sure to have the 'requests' and 'python-dotenv' libraries
       installed in your Python environment using 'pip install requests python-dotenv'.

    2. Create a .env file in the same directory as this script and define the 'movie_api_key'
       environment variable with your actual OMDb API key.

Example:
    # Import the module and call the search_movie function
    import movie_api

    # Search for movie data with the movie name "Inception"
    movie_name = "Inception"
    movie_data = movie_api.search_movie(movie_name)

    # Check if the movie data is found and print relevant information
    if movie_data:
        print(f"Movie: {movie_data['Title']}")
        print(f"Director: {movie_data['Director']}")
        print(f"Year: {movie_data['Year']}")
        print(f"Rating: {movie_data['imdbRating']}")
    else:
        print(f"Movie '{movie_name}' not found or there was an API error."

Note:
    - Before using this code, ensure that you have obtained an OMDb API key
      from https://www.omdbapi.com and set it as the 'movie_api_key' environment
      variable in the .env file.

    - This module assumes that the 'movie_api_key' environment variable
      is defined in the .env file using 'python-dotenv'.

API Documentation:
    For more details on the OMDb API, visit https://www.omdbapi.com
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("movie_api_key")


def search_movie(name):
    """
    Searches for movie data using the OMDb API.

    Parameters:
        name (str): The name of the movie to search for.

    Returns:
        dict: A dictionary containing movie data, or None if
        the movie is not found or there was an API error.
    """
    movie = f"http://www.omdbapi.com/?apikey={api_key}&t={name}"
    movie_data = requests.get(movie)
    return movie_data.json()
