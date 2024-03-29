# This file contains All models used in the application

from app.database_helper import GetAppBoundDBContext

# Get the SQLAlchemy database context bound to the Flask application
db = GetAppBoundDBContext()

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Movie(db.Model):
    """
    Model representing a Movie.

    Attributes:
        id (int): The unique identifier for the movie.
        title (str): The title of the movie.
        release_date (datetime.date): The release date of the movie.
        actors (relationship): Relationship with the Actor model representing the actors in the movie.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    actors = db.relationship(
        'Actor',
        secondary='movie_actors',
        backref=db.backref(
            'movies',
            lazy=True))

    def __repr__(self):
        return f'<Movie {self.title}>'

    def format(self):
        """
        Format the Movie object into a dictionary.

        Returns:
            dict: A dictionary containing the formatted movie data.
        """
        return {
            'id': self.id,
            'title': self.title,
            'release_date': str(self.release_date),
            'actors': [actor.name for actor in self.actors]
        }


class Actor(db.Model):
    """
    Model representing an Actor.

    Attributes:
        id (int): The unique identifier for the actor.
        name (str): The name of the actor.
        age (int): The age of the actor.
        gender (str): The gender of the actor.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Actor {self.name}>'

    def format(self):
        """
        Format the Actor object into a dictionary.

        Returns:
            dict: A dictionary containing the formatted actor data.
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


# Association table for many-to-many relationship between movies and actors
movie_actors = db.Table('movie_actors',
                        db.Column('movie_id', db.Integer, db.ForeignKey(
                            'movie.id'), primary_key=True),
                        db.Column('actor_id', db.Integer, db.ForeignKey(
                            'actor.id'), primary_key=True)
                        )
