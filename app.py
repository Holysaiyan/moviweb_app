"""
Movie Management Web Application

This is a Flask-based web application that allows users to manage their movie collections.
Users can add, update, and delete movies associated with their user ID. The application utilizes
a JSON data manager to store and retrieve user and movie data.

Routes:
- `/`: Home page that provides an overview of the application.
- `/users`: Displays a list of users and their associated movies.
- `/add_user`: Allows users to add a new user to the database.
- `/success`: Displays a success message after adding a user.
- `/users/<int:user_id>`: Displays movies associated with a specific user.
- `/users/<int:user_id>/add_movie`: Allows users to add a new movie to their collection.
- `/users/<int:user_id>/delete_movie/<int:movie_id>`: Allows users to delete a movie
   from their collection.
- `/users/<int:user_id>/update_movie/<int:movie_id>`: Allows users to update movie information.
- `/about_us`: Provides information about the application and its creators.

Error Handlers:
- `404`: Custom page for Page Not Found (404) errors.
- `400`: Custom page for Bad Request (400) errors.
- `405`: Custom page for Method Not Allowed (405) errors.
- `500`: Custom page for Internal Server Error (500) errors.


"""
from flask import Flask, render_template, request, redirect, url_for
from DataManager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('DataManager/movie.json')


def generate_user_id():
    """
    This function generates new user ID
    :return:
    """
    data = data_manager.get_data()
    new_id = max([user['id'] for user in data]) + 1
    return new_id


@app.route('/')
def home():
    """
    Renders the home page of the application.

    Returns:
        str: The HTML content of the home page.
    """
    return render_template('home.html')


@app.route('/users')
def get_users():
    """
    Retrieves user data and renders the page displaying a list of users.

    Returns:
        str: The HTML content of the users page.

    """
    users = data_manager.get_data()
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    """
    Adds a new user to the database and redirects to the success page upon successful submission.

    Returns:
        str or redirect: Either the add user page or a redirect to the success page.
    """
    if request.method == 'POST':
        user_name = request.form.get('new_user')
        data_manager.add_user(user_name)
        return redirect(url_for('success'))
    return render_template('add_user.html')


@app.route('/success')
def success():
    """
    Renders a page indicating successful addition of a user.

    Returns:
        str: A success message.
    """
    return 'Successfully added user'


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Renders the page displaying movies associated with a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The HTML content of the user movies page.
    """
    data = data_manager.get_data()
    return render_template('user_movies.html', user_id=user_id, user=data)


@app.route('/users/<int:user_id>/add_movie', methods=['POST', 'GET'])
def add_movie(user_id):
    """
    Adds a new movie to a specific user's collection and redirects to the user's movie page
    upon successful submission.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str or redirect: Either the add movie page or a redirect to the user's movie page.
    """
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        data_manager.add_movie(movie_name=movie_name, user_id=int(user_id))
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['DELETE', 'GET'])
def delete_movie(user_id, movie_id):
    """
    Deletes a movie from a specific user's collection and redirects to the user's movie page
    upon successful deletion.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie.

    Returns:
        redirect: A redirect to the user's movie page.
        str: Either a redirect or an error message for unsupported methods.
    """

    if request.method == 'GET':
        data_manager.delete_movie(user_id=user_id, movie_id=movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    elif request.method == 'DELETE':
        data_manager.delete_movie(user_id=user_id, movie_id=movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    else:
        return 'METHOD NOT ALLOWED', 405


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['POST', 'GET'])
def update_movie(user_id, movie_id):
    """
    Updates movie information and redirects to the user's movie page upon successful update.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie.

    Returns:
        redirect or str: Either a redirect to the user's movie page or an error message
        for unsupported methods.
    """
    data = data_manager.get_data()

    if request.method == 'POST':
        title = request.form['name']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']

        updated_movie_info = {
            'name': title,
            'director': director,
            'year': int(year),
            'rating': float(rating)
        }

        data_manager.update_movie_info(user_id, movie_id, updated_movie_info)

        return redirect(url_for('user_movies', user_id=user_id))

    elif request.method == 'GET':
        # Find the specific movie for the given user_id and movie_id
        movie_info = [movie for data_info in data if user_id == data_info['id']
                      for movie in data_info['movies'] if movie_id == movie['id']]

        if not movie_info:
            return 'Movie not found', 404

        # Get the current movie details
        movie = movie_info[0]

        return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie)
    else:
        return 'METHOD NOT ALLOWED', 405


@app.route('/about_us')
def about_us():
    """
    Renders the about us page of the application.

    Returns:
        str: The HTML content of the about us page.
    """
    return render_template('about_us.html')


# ERROR SECTION
@app.errorhandler(404)
def page_not_found(e):
    """
    Error handler for 404 Page Not Found errors.

    Args:
        e (Exception): The exception object.

    Returns:
        str: The HTML content of the custom 404 error page.
    """
    return render_template('error pages/404.html'), 404


# Error handler for 400 Bad Request
@app.errorhandler(400)
def bad_request(e):
    """
    Error handler for 400 Bad Request errors.

    Args:
        e (Exception): The exception object.

    Returns:
        str: The HTML content of the custom 400 error page.
    """
    return render_template('error pages/400.html'), 400


# Error handler for 405 Method Not Allowed
@app.errorhandler(405)
def method_not_allowed(e):
    """
    Error handler for 405 Method Not Allowed errors.

    Args:
        e (Exception): The exception object.

    Returns:
        str: The HTML content of the custom 405 error page.
    """
    return render_template('error pages/405.html'), 405


# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    """
    Error handler for 500 Internal Server Error errors.

    Args:
        e (Exception): The exception object.

    Returns:
        str: The HTML content of the custom 500 error page.
    """
    return render_template('error pages/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
