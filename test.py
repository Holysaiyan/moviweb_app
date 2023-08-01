user = [{"id": 1, "name": "Alice",
         "movies": [{"id": 1, "name": "Inception", "director": "Christopher Nolan", "year": 2010, "rating": 8.8},
                    {"id": 2, "name": "The Dark Knight", "director": "Christopher Nolan", "year": 2008,
                     "rating": 9.0}]}, {"id": 2, "name": "Bob", "movies": [
    {"id": 1, "name": "The Dark Knight", "director": "Christopher Nolan", "year": 2008, "rating": 9.0}]},
        {"id": 3, "name": "David", "movies": []}, {"id": 4, "name": "Olu", "movies": []},
        {"id": 5, "name": "pana", "movies": []}, {"id": 6, "name": "Arsenal", "movies": [
        {"id": 1, "name": "Ghost Rider", "director": "Mark Steven Johnson", "year": 2007, "rating": 5.3},
        {"id": 2, "name": "Iron Man 2", "director": "Jon Favreau", "year": 2010, "rating": 6.9},
        {"id": 3, "name": "Iron Monkey", "director": "Woo-Ping Yuen", "year": 1993, "rating": 7.5},
        {"id": 4, "name": "8 Mile", "director": "Curtis Hanson", "year": 2002, "rating": 7.2}]}]

for user_info in user:
    for index, movie_info in enumerate(user_info['movies'], start=4):
        movie_info['id'] = index


def find_user_id(user_id, target):
    find_user_by_id = [id for id in user_id if target == id]
    if find_user_by_id:
        return find_user_by_id
    return None

id_lst = [1,1,2,3,4,5]

print(find_user_id(id_lst, 6))