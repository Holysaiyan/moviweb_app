import json
from moviweb_app.DataManager.data_manager_interface import DataManagerInterface
from moviweb_app.DataManager.movie_api import search_movie


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

    def write_data(self, new_data):
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
        for item in self.data:
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
            check_movie_list = [movie_info['name'] for item in data if item['id'] == user_id for movie_info in item[
                'movies']]
            if movie_data['Title'] in check_movie_list:
                return 'Movie already exists'

            # compiles the information of the movie and generates unique id
            new_movie = {'id': self.generate_movie_id(user_id),
                         'name': movie_data['Title'],
                         'director': movie_data['Director'],
                         'year': int(movie_data["Year"]),
                         'rating': float(movie_data["imdbRating"])}

            [item['movies'].append(new_movie) for item in data if item['id'] == user_id]
            self.write_data(data)
            return 'Movie Successfully Added'
        else:
            return 'User does not exist, Create account first'


#a = JSONDataManager('../movie.json')
# print(a.find_user_id(8))
#print(a.add_movie('Ghost Rider', 6))
# print(a.generate_movie_id(1))
