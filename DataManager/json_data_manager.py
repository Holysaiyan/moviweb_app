import json
from DataManager.data_manager_interface import DataManagerInterface
from DataManager.movie_api import search_movie


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as file:
            data = json.load(file)
        self.data = data

    def get_all_users(self) -> list:
        """
        get all the user from the database
        :return: a list of users
        """
        users = []
        for item in self.data:
            users.append(item['name'])
        return users

    def get_data(self):
        return self.data

    def save_data(self, new_data):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(new_data, file)
        return 'Successfully written the new data'

    def generate_user_id(self):
        new_id = max([user['id'] for user in self.get_data()]) + 1
        return new_id

    def find_user_id(self, user_id):
        find_user_by_id = [user['id'] for user in self.get_data() if user_id == user['id']]
        if user_id in find_user_by_id:
            return find_user_by_id
        return None

    def generate_movie_id(self, user_id):
        movie_id = len([movies for user in self.get_data() if user['id']
                        in self.find_user_id(user_id) for movies in user['movies']]) + 1
        return movie_id

    def get_user_movies(self, user_id) -> [list, str]:
        for item in self.get_data():
            if item['id'] == user_id:
                if not item['movies']:
                    return []
                else:
                    return item['movies']
        return 'User does not exist'

    def add_user(self, name):
        data = self.get_data()
        new_id = self.generate_user_id()
        new_user = {'id': new_id,
                    'name': name,
                    'movies': []}
        data.append(new_user)
        with open('movie.json', 'w', encoding='utf-8') as file:
            json.dump(data, file)

    def add_movie(self, movie_name, user_id):
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
                         'year': int(movie_data["Year"]),
                         'rating': float(movie_data["imdbRating"])}

            [item['movies'].append(new_movie) for item in data if item['id'] == user_id]
            self.save_data(data)

    def delete_movie(self, user_id, movie_id):
        """
        This function deletes the movie targeted through movie_id in the user_id.
        It then modifies the movie_id in the user_id in the ascending order, filling
        the gap.
        """
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

    def update_movie(self, user_id, movie_id):
        pass


# a = JSONDataManager('../movie.json')
# print(a.find_user_id(8))
# print(a.add_movie('Ghost Rider', 6))
# print(a.generate_movie_id(1))
# print(a.delete_movie(1, 1))
