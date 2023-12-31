"""
JSON Data Manager Module

This module provides a JSON-based data manager implementation
for the movie management web application. It includes functionalities
to interact with user and movie data stored in a JSON file.

Classes:
- JSONDataManager: Implements the DataManagerInterface for managing user
  and movie data in a JSON file.

"""
import json
from .data_manager_interface import DataManagerInterface
from .omdb_movie_api import search_movie


class JSONDataManager(DataManagerInterface):
    """
    JSON Data Manager Class

    This class implements the DataManagerInterface interface for managing user
    and movie data in a JSON file.

    Attributes:
        filename (str): The name of the JSON file used for data storage.

    Methods:
        get_all_users(): Get a list of all usernames.
        get_data(): Get the entire data stored in the JSON file.
        save_data(new_data): Save new data to the JSON file.
        generate_user_id(): Generate a new user ID.
        find_user_id(user_id): Find a user's ID by user ID.
        generate_movie_id(user_id): Generate a new movie ID for a specific user.
        get_user_movies(user_id): Get the movies associated with a user.
        add_user(name): Add a new user to the database.
        add_movie(movie_name, user_id): Add a new movie to a user's collection.
        delete_movie(user_id, movie_id): Delete a movie from a user's collection.
        update_movie_info(user_id, movie_id, updated_movie_info): Update movie information.
    """

    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self) -> list:
        """
        Get a list of all usernames in the database.

        Returns:
            list: A list of usernames.
        """
        users = []
        for item in self.get_data():
            users.append(item['name'])
        return users

    def get_data(self):
        """
        Get the entire data stored in the JSON file.

        Returns:
            dict: The data stored in the JSON file.
        """
        try:
            with open(self.filename, "r", encoding="UTF-8") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return []

    def save_data(self, new_data):
        """
        Save new data to the JSON file.

        Args:
            new_data (dict): The new data to be saved.

        Returns:
            str: A success message indicating the data has been written.
        """
        with open(self.filename, 'w', encoding='UTF-8') as file:
            json.dump(new_data, file)
        return 'Successfully written the new data'

    def generate_user_id(self):
        """
        Generate a new unique user ID.

        Returns:
            int: The newly generated user ID.
        """
        new_id = max([user['id'] for user in self.get_data()]) + 1
        return new_id

    def find_user_id(self, user_id):
        """
        Find a user's ID by the given user ID.

        Args:
            user_id (int): The user ID to search for.

        Returns:
            list or None: A list of found user IDs or None if not found.
        """
        find_user_by_id = [user['id']
                           for user in self.get_data() if user_id == user['id']]
        if user_id in find_user_by_id:
            return find_user_by_id
        return None

    def generate_movie_id(self, user_id):
        """
        Generate a new unique movie ID for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            int: The newly generated movie ID.
        """
        movie_id = len([movies for user in self.get_data() if user['id']
                        in self.find_user_id(user_id) for movies in user['movies']]) + 1
        return movie_id

    def get_user_movies(self, user_id) -> [list, str]:
        """
        Get the movies associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of movies associated with the user.
        """
        for item in self.get_data():
            if item['id'] == user_id:
                if not item['movies']:
                    return []
                else:
                    return item['movies']
        return 'User does not exist'

    def add_user(self, name):
        """
        Add a new user to the database.

        Args:
            name (str): The name of the new user.

        Returns:
            str or None: A success message or an error message.
        """
        try:
            data = self.get_data()
            new_id = self.generate_user_id()
            new_user = {'id': new_id,
                        'name': name,
                        'movies': []}
            data.append(new_user)
            with open('DataManager/movie.json', 'w', encoding='UTF-8') as file:
                json.dump(data, file)
        except Exception as e:
            return f"Error occurred while adding user: {str(e)}"

    def add_movie(self, movie_name, user_id):
        """
        Add a new movie to a user's collection.

        Args:
            movie_name (str): The name of the movie.
            user_id (int): The ID of the user.

        Returns:
            str or None: A success message or an error message.
        """
        try:
            data = self.get_data()
            movie_data = search_movie(movie_name)
            get_user_id = self.find_user_id(user_id)
            if get_user_id is not None:

                # check if movie already exists in user account
                check_movie_list = [movie_info['name'] for item in data
                                    if item['id'] == user_id for movie_info in item['movies']]
                if movie_data['Title'] in check_movie_list:
                    return 'Movie already exists'

                # compiles the information of the movie and generates unique id
                new_movie = {'id': self.generate_movie_id(user_id),
                             'name': movie_data['Title'],
                             'director': movie_data['Director'],
                             'year': movie_data["Year"],
                             'rating': float(movie_data["imdbRating"]),
                             'poster': movie_data['Poster'],
                             'plot': movie_data['Plot']}

                [item['movies'].append(new_movie)
                 for item in data if item['id'] == user_id]
                self.save_data(data)
        except Exception as e:
            return f"error occurred while adding movie : {str(e)}"

    def delete_movie(self, user_id, movie_id):
        """
        Delete a movie from a user's collection.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to be deleted.

        Returns:
            str or None: A success message or an error message.
        """
        try:
            data = self.get_data()

            movie_info = [movie for item in data if item['id'] == user_id
                          for movie in item['movies'] if movie['id'] == movie_id]

            movie_lst = [movie for item in data if item['id'] == user_id
                         for movie in item['movies']]

            if movie_info:
                movie_lst.remove(movie_info[0])

                # Update the data with the modified movie_lst
                for item in data:
                    if item['id'] == user_id:
                        item['movies'] = movie_lst

                # fill the movies id gap
                for user_info in data:
                    if user_info['id'] == user_id:
                        for index, movie_info in enumerate(user_info['movies'], start=1):
                            movie_info['id'] = index

            self.save_data(data)
        except Exception as e:
            return f"error occurred while deleting movie : {str(e)}"

    def update_movie_info(self, user_id, movie_id, updated_movie_info):
        """
        Update movie information.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to be updated.
            updated_movie_info (dict): The updated information for the movie.

        Returns:
            str or None: A success message or an error message.
        """
        try:
            data = self.get_data()

            # Find the movie to be updated
            for user_info in data:
                if user_info['id'] == user_id:
                    for movie_info in user_info['movies']:
                        if movie_info['id'] == movie_id:
                            # Update the movie information
                            movie_info.update(updated_movie_info)
                            break

            self.save_data(data)
        except Exception as e:
            return f"error occurred while updating movie information : {str(e)}"
