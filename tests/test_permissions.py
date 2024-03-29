# Import necessary modules for testing
import json
import os
import unittest
from app import app, db
from app.models import Actor, Movie

# Get the path to the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Load JWT tokens and roles from JSON file
token_file_path = os.path.join(project_root, 'role_token.json')
# Load JWT tokens and roles from JSON file
with open(token_file_path) as f:
    token_data = json.load(f)


class TestPermissions(unittest.TestCase):
    """Test RBAC for different roles"""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        # Create some sample actors and movies for testing
        self.actor1 = Actor(name='Actor 1', age=30, gender='Male')
        self.actor2 = Actor(name='Actor 2', age=25, gender='Female')
        self.movie1 = Movie(title='Movie 1', release_date='2023-01-01')
        self.movie2 = Movie(title='Movie 2', release_date='2024-01-01')
        db.create_all()
        db.session.add_all(
            [self.actor1, self.actor2, self.movie1, self.movie2])
        db.session.commit()

    def tearDown(self):
        """Tear down test fixtures after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_casting_assistant_permissions_actors(self):
        """Test RBAC for Casting Assistant viewing actors."""
        # Test GET actors endpoint
        token = token_data['roles']['Casting Assistant']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/actors', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_casting_assistant_permissions_movies(self):
        """Test RBAC for Casting Assistant viewing movies."""
        # Test GET movies endpoint
        token = token_data['roles']['Casting Assistant']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/movies', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_casting_director_permissions_actors(self):
        """Test RBAC for Casting Director updating actors."""
        # Test PATCH actors endpoint
        token = token_data['roles']['Casting Director']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        actor_id = self.actor1.id
        updated_actor_data = {'name': 'Updated Actor Name'}
        response = self.app.patch(
            f'/actors/{actor_id}', json=updated_actor_data, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_casting_director_permissions_movies(self):
        """Test RBAC for Casting Director updating movies."""
        # Test PATCH movies endpoint
        token = token_data['roles']['Casting Director']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        movie_id = self.movie1.id
        updated_movie_data = {'title': 'Updated Movie Title'}
        response = self.app.patch(
            f'/movies/{movie_id}', json=updated_movie_data, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_executive_producer_permissions_actors(self):
        """Test RBAC for Executive Producer creating actors."""
        # Test POST actors endpoint
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        new_actor_data = {'name': 'New Actor', 'age': 35, 'gender': 'Male'}
        response = self.app.post(
            '/actors', json=new_actor_data, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_executive_producer_permissions_movies(self):
        """Test RBAC for Executive Producer creating movies."""
        # Test POST movies endpoint
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        new_movie_data = {'title': 'New Movie', 'release_date': '2025-01-01'}
        response = self.app.post(
            '/movies', json=new_movie_data, headers=headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
