"""
Movie Management Web Application

This is a Flask-based web application that allows users to manage their movie collections.
Users can add, update, and delete movies associated with their user ID. The application utilizes
a SQLITE data manager to store and retrieve user and movie data.

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
from DataManager.sql_data_manager import SQLiteDataManager

from api_manager.api import api


data_manager = SQLiteDataManager('DataManager/movie.db')

app = Flask(__name__)

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
        email = request.form.get('new_email')
        data_manager.add_user(user_name, email)
        return redirect(url_for('get_users'))
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
    data = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_user_name_by_id(user_id)
    return render_template('user_movies.html', user_id=user_id, user=data, name=user_name)


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
    # data = data_manager.get_user_movies(user_id)

    if request.method == 'POST':
        rating = request.form['rating']

        updated_movie_info = {
            'rating': float(rating)
        }

        data_manager.update_movie_info(user_id, movie_id, updated_movie_info)

        return redirect(url_for('user_movies', user_id=user_id))

    elif request.method == 'GET':
        # Find the specific movie for the given user_id and movie_id
        movie_info = data_manager.get_specific_user_and_movie(user_id, movie_id)

        if not movie_info:
            return 'Movie not found', 404

        return render_template('update_movie.html', movie=movie_info)
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


@app.route('/movies', methods=['GET'])
def show_movies():
    """
    Renders a paginated page of the movies currently in the db

    """
    page = int(request.args.get('page', 1))  # Get the page number from the query parameters (default to 1)
    movies_per_page = 9  # Set the number of movies per page

    # Calculate the offset based on the page number
    offset = (page - 1) * movies_per_page

    # Call data_manager.get_all_movies with the page and limit parameters
    movies_data = data_manager.get_all_movies(page=page, limit=movies_per_page)

    return render_template('movies.html', movies=movies_data, page=page)


@app.route('/movies/<int:movie_id>')
def movie_detail(movie_id):
    """
    Renders the information page about the movie

    :return: The html template of the movie info page
    """
    data = data_manager.get_movie_info(movie_id)
    users = data_manager.get_all_users()
    reviews = data_manager.view_reviews(movie_id)

    return render_template('movie_info.html', movie_info=data, movie_id=movie_id, users=users, reviews=reviews)


@app.route('/add_review', methods=['POST'])
def add_review():
    """
    Enables users to add review about the movie in the movie info page

    """
    if request.method == 'POST':
        selected_user = request.form.get('selected_user')
        selected_movie = request.form.get('movie')
        review = request.form.get('review')
        rating = request.form.get('rating')
        current_movie = data_manager.get_movie_id_by_title(selected_movie)

        data_manager.add_review_to_movie(selected_user, selected_movie, review, rating)

        return redirect(url_for('movie_detail', movie_id=current_movie))


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
    app.run(host="0.0.0.0", debug=True, port=5000)
