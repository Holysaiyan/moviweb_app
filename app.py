from flask import Flask, render_template, request, redirect, url_for
from DataManager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('movie.json')


def generate_user_id():
    data = data_manager.get_data()
    new_id = max([user['id'] for user in data]) + 1
    return new_id


@app.route('/')
def home():
    return 'WELCOME TO MOVIEWEB APP'


@app.route('/users')
def get_users():
    users = data_manager.get_data()
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    """
    Adds user to json database. Generates ID and
    gives empty movies list
    :return:
    """
    if request.method == 'POST':
        user_name = request.form.get('new_user')
        data_manager.add_user(user_name)
        return redirect(url_for('success'))
    return render_template('add_user.html')


@app.route('/success')
def success():
    return 'Successfully added user'


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    data = data_manager.get_data()
    return render_template('user_movies.html', user_id=user_id, user=data)


@app.route('/users/<int:user_id>/add_movie', methods=['POST', 'GET'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        data_manager.add_movie(movie_name=movie_name, user_id=int(user_id))
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['DELETE', 'GET'])
def delete_movie(user_id, movie_id):
    if request.method == 'GET':
        data_manager.delete_movie(user_id=user_id, movie_id=movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    elif request.method == 'DELETE':
        data_manager.delete_movie(user_id=user_id, movie_id=movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        return 'METHOD NOT ALLOWED', 405


@app.route('/users/user_id/update_movie/movie_id', methods=['POST', 'GET'])
def update_movie(user_id, movie_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
