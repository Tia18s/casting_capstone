# Import necessary modules for testing
import json
import os
import unittest
from app import app, db
from app.models import Movie

# Get the path to the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Load JWT tokens and roles from JSON file
token_file_path = os.path.join(project_root, 'role_token.json')
# Load JWT tokens and roles from JSON file
with open(token_file_path) as f:
    token_data = json.load(f)


class MoviesTestCase(unittest.TestCase):
    """Test case for Movies endpoints."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        # Create some sample movies for testing
        self.movie1 = Movie(title='Movie 1', release_date='2023-01-01')
        self.movie2 = Movie(title='Movie 2', release_date='2024-01-01')
        db.create_all()
        db.session.add_all([self.movie1, self.movie2])
        db.session.commit()

    def tearDown(self):
        """Tear down test fixtures after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test for successful retrieval of movies
    def test_get_movies_success(self):
        """Test successful retrieval of movies."""
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/movies', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie 1', response.data)
        self.assertIn(b'Movie 2', response.data)

    # Test for error behavior when no movies are available
    def test_get_movies_error(self):
        """Test error behavior when no movies are available."""
        # Delete all movies to simulate no movies available
        Movie.query.delete()
        db.session.commit()
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/movies', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'No movies', response.data)

    # Test for successful creation of a new movie
    def test_create_movie_success(self):
        """Test successful creation of a new movie."""
        new_movie_data = {'title': 'New Movie', 'release_date': '2025-01-01'}
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post(
            '/movies', json=new_movie_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data.decode(
            'utf8').replace("'", '"'))['success'])

    # Test for error behavior when required fields are missing during movie
    # creation
    def test_create_movie_error_missing_fields(self):
        """Test error behavior when required fields are missing during movie creation."""
        new_movie_data = {'release_date': '2025-01-01'}
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post(
            '/movies', json=new_movie_data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Title and release_date are required', response.data)

    # Test for successful update of an existing movie
    def test_update_movie_success(self):
        """Test successful update of an existing movie."""
        movie_id = self.movie1.id
        updated_movie_data = {'title': 'Updated Movie Title'}
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.patch(
            f'/movies/{movie_id}', json=updated_movie_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data.decode(
            'utf8').replace("'", '"'))['success'])

    # Test for error behavior when trying to update a non-existent movie
    def test_update_movie_error_nonexistent(self):
        """Test error behavior when trying to update a non-existent movie."""
        movie_id = 999  # Non-existent movie ID
        updated_movie_data = {'title': 'Updated Movie Title'}
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.patch(
            f'/movies/{movie_id}', json=updated_movie_data, headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Movie not found', response.data)

    # Test for successful deletion of a movie
    def test_delete_movie_success(self):
        """Test successful deletion of a movie."""
        movie_id = self.movie1.id
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.delete(f'/movies/{movie_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data.decode(
            'utf8').replace("'", '"'))['success'])

    # Test for error behavior when trying to delete a non-existent movie
    def test_delete_movie_error_nonexistent(self):
        """Test error behavior when trying to delete a non-existent movie."""
        movie_id = 999  # Non-existent movie ID
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.delete(f'/movies/{movie_id}', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Movie not found', response.data)


if __name__ == '__main__':
    unittest.main()
