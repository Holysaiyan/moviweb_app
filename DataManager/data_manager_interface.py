from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """
    Data Manager Interface (Abstract Base Class)

    This class defines the interface for managing user and movie data.

    Methods:
        get_all_users(): Get a list of all usernames.
        get_user_movies(user_id): Get the movies associated with a specific user.
        add_user(name): Add a new user to the database.
        get_data(): Get the entire data stored in the data manager.
        save_data(): Save data to the data manager.
        generate_user_id(): Generate a new user ID.
        find_user_id(): Find a user's ID.
        generate_movie_id(): Generate a new movie ID.
        add_movie(movie_name, user_id): Add a new movie to a user's collection.
        delete_movie(user_id, movie_id): Delete a movie from a user's collection.
        update_movie_info(user_id, movie_id, updated_movie_info): Update movie information.
    """

    @abstractmethod
    def get_all_users(self):
        """
        Get a list of all usernames in the database.

        Returns:
            list: A list of usernames.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Get the movies associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of movies associated with the user.
        """
        pass

    @abstractmethod
    def add_user(self, name):
        """
        Add a new user to the database.

        Args:
            name (str): The name of the new user.

        Returns:
            str or None: A success message or an error message.
        """
        pass

    @abstractmethod
    def get_data(self):
        """
        Get the entire data stored in the data manager.

        Returns:
            dict: The data stored in the data manager.
        """
        pass

    @abstractmethod
    def save_data(self):
        """
        Save data to the data manager.

        Returns:
            str: A success message indicating the data has been saved.
        """
        pass

    @abstractmethod
    def generate_user_id(self):
        """
        Generate a new unique user ID.

        Returns:
            int: The newly generated user ID.
        """
        pass

    @abstractmethod
    def find_user_id(self):
        """
        Find a user's ID.

        Returns:
            list or None: A list of found user IDs or None if not found.
        """
        pass

    @abstractmethod
    def generate_movie_id(self):
        """
        Generate a new unique movie ID.

        Returns:
            int: The newly generated movie ID.
        """
        pass

    @abstractmethod
    def add_movie(self, movie_name, user_id):
        """
        Add a new movie to a user's collection.

        Args:
            movie_name (str): The name of the movie.
            user_id (int): The ID of the user.

        Returns:
            str or None: A success message or an error message.
        """
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """
        Delete a movie from a user's collection.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to be deleted.

        Returns:
            str or None: A success message or an error message.
        """
        pass

    @abstractmethod
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
        pass
