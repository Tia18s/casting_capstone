from flask import jsonify, request
from app.models import Movie, Actor, db
from app.auth import requires_auth
from datetime import datetime


def setupControllers(appContext):
    """Set up controller endpoints and error handlers for the Flask application.

    Args:
        appContext (Flask): The Flask application instance.

    Returns:
        Flask: The modified Flask application instance with added endpoints and error handlers.
    """

    app = appContext

    @app.route('/', methods=['GET'])
    def get_login_results():
        """Handle login results.

        Returns:
            object: A JSON response indicating successful login.
        """
        return "Welcome to casting capstone app please check readme on https://github.com/Tia18s/casting_capstone"

    @app.route('/login-results', methods=['GET'])
    def get_login_results():
        """Handle login results.

        Returns:
            object: A JSON response indicating successful login.
        """
        return jsonify({"success": True})

    # Custom error handler for 400 Bad Request
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors.

        Args:
            error (str): Error message.

        Returns:
            object: A JSON response indicating a bad request error.
        """
        if not error:
            return jsonify({'error': 'Bad Request', 'message': 'The request cannot be fulfilled due to bad syntax or missing required data'}), 400
        else:
            return jsonify({'error': 'Bad Request', 'message': error}), 400

    # Custom error handler for 401 Unauthorized
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors.

        Args:
            error (str): Error message.

        Returns:
            object: A JSON response indicating an unauthorized error.
        """
        return jsonify({'error': 'Unauthorized', 'message': 'Authorization header is missing or invalid'}), 401

    # Custom error handler for 403 Forbidden
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors.

        Args:
            error (str): Error message.

        Returns:
            object: A JSON response indicating a forbidden error.
        """
        return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to access this resource'}), 403

    # Custom error handler for 404 Not Found
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors.

        Args:
            error (str): Error message.

        Returns:
            object: A JSON response indicating a not found error.
        """
        if error and isinstance(error, str):
            return jsonify({'error': 'Not Found', 'message': error}), 404
        else:
            return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found'}), 404
            
    # Custom error handler for 500 Internal Server Error
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error errors.

        Args:
            error (str): Error message.

        Returns:
            object: A JSON response indicating an internal server error.
        """
        return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500

    # GET request to retrieve all actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def get_actors(payload):
        """Endpoint to retrieve all actors.

        This endpoint requires 'view:actors' permission.

        Args:
            payload (dict): The decoded JWT payload containing user information.

        Returns:
            object: A JSON response containing a list of actors.
        """
        try:
            actors = db.session.query(Actor).all()
            if not actors:
                return not_found('No actors')
            formatted_actors = [actor.format() for actor in actors]
            return jsonify({'actors': formatted_actors})
        except Exception as e:
            return internal_server_error(e)

    # GET request to retrieve all movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('view:movies')
    def get_movies(payload):
        """Endpoint to retrieve all movies.

        This endpoint requires 'view:movies' permission.

        Args:
            payload (dict): The decoded JWT payload containing user information.

        Returns:
            object: A JSON response containing a list of movies.
        """
        try:
            movies = db.session.query(Movie).all()
            if not movies:
                return not_found('No movies')
            formatted_movies = [movie.format() for movie in movies]
            return jsonify({'movies': formatted_movies})
        except Exception as e:
            return internal_server_error(e)

    # DELETE request to delete an actor by ID
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        """Endpoint to delete an actor by ID.

        This endpoint requires 'delete:actors' permission.

        Args:
            payload (dict): The decoded JWT payload containing user information.
            actor_id (int): The ID of the actor to be deleted.

        Returns:
            object: A JSON response indicating the success or failure of the deletion operation.
        """
        try:
            actor = db.session.get(Actor, actor_id)
            if actor:
                db.session.delete(actor)
                db.session.commit()
                return jsonify({'success': True, 'message': f'Actor {actor_id} deleted'})
            else:
                return not_found('Actor not found')
        except Exception as e:
            db.session.rollback()
            raise Exception("Error deleting actor: " + str(e))

    # DELETE request to delete a movie by ID
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        """Endpoint to delete a movie by ID.

        This endpoint requires 'delete:movies' permission.

        Args:
            payload (dict): The decoded JWT payload containing user information.
            movie_id (int): The ID of the movie to be deleted.

        Returns:
            object: A JSON response indicating the success or failure of the deletion operation.
        """
        try:
            movie = db.session.get(Movie, movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
                return jsonify({'success': True, 'message': f'Movie {movie_id} deleted'})
            else:
                return not_found('Movie not found')
        except Exception as e:
            db.session.rollback()
            raise Exception("Error deleting movie: " + str(e))

    # POST request to create a new actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        """Endpoint to create a new actor.

        This endpoint requires 'post:actors' permission.

        Args:
            payload (dict): The decoded JWT payload containing user information.

        Returns:
            object: A JSON response indicating the success or failure of the creation operation,
                    along with the ID of the newly created actor.
        """
        try:
            data = request.json
            name = data.get('name')
            age = data.get('age')
            gender = data.get('gender')

            if name is None or age is None or gender is None:
                return bad_request('Name, age, and gender are required')

            new_actor = Actor(name=name, age=age, gender=gender)
            db.session.add(new_actor)
            db.session.commit()

            return jsonify({'success': True, 'actor_id': new_actor.id})
        except Exception as e:
            db.session.rollback()
            return internal_server_error(e)

    # POST request to create a new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        """Endpoint to create a new movie.

        This endpoint requires 'post:movies' permission.

        Args:
            payload (dict): The decoded JWT payload containing user information.

        Returns:
            object: A JSON response indicating the success or failure of the creation operation,
                    along with the ID of the newly created movie.
        """
        try:
            data = request.json
            title = data.get('title')
            release_date = data.get('release_date')

            if title is None or release_date is None:
                return bad_request('Title and release_date are required')

            new_movie = Movie(title=title, release_date=datetime.now())
            db.session.add(new_movie)
            db.session.commit()

            return jsonify({'success': True, 'movie_id': new_movie.id})
        except Exception as e:
            print(e)
            db.session.rollback()
            return internal_server_error(e)

    # PATCH request to update an existing actor by ID
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(payload, actor_id):
        """Endpoint to update an existing actor by ID.

        This endpoint requires 'update:actors' permission.

        Args:
            payload (dict): The decoded JWT payload containing user information.
            actor_id (int): The ID of the actor to be updated.

        Returns:
            object: A JSON response indicating the success or failure of the update operation,
                    along with the updated actor information.
        """
        try:
            data = request.json
            actor = db.session.get(Actor, actor_id)

            if actor is None:
                return not_found('Actor not found')

            if 'name' in data:
                actor.name = data['name']

            if 'age' in data:
                actor.age = data['age']

            if 'gender' in data:
                actor.gender = data['gender']

            db.session.commit()

            return jsonify({'success': True, 'updated_actor': actor.format()})
        except Exception as e:
            db.session.rollback()
            return internal_server_error(e)

    # PATCH request to update an existing movie by ID
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(payload, movie_id):
        """Endpoint to update an existing movie by ID.

        This endpoint requires 'update:movies' permission.

        Args:
            payload (dict): The decoded JWT payload containing user information.
            movie_id (int): The ID of the movie to be updated.

        Returns:
            object: A JSON response indicating the success or failure of the update operation,
                    along with the updated movie information.
        """
        try:
            data = request.json
            movie = db.session.get(Movie, movie_id)

            if movie is None:
                return not_found('Movie not found')

            if 'title' in data:
                movie.title = data['title']

            if 'release_date' in data:
                movie.release_date = data['release_date']

            db.session.commit()

            return jsonify({'success': True, 'updated_movie': movie.format()})
        except Exception as e:
            db.session.rollback()
            return internal_server_error(e)

    return app
