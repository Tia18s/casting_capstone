# Import necessary modules for testing
import json
import os
import unittest
from app import app, db
from app.models import Actor

# Get the path to the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Load JWT tokens and roles from JSON file
token_file_path = os.path.join(project_root, 'role_token.json')
# Load JWT tokens and roles from JSON file
with open(token_file_path) as f:
    token_data = json.load(f)


class ActorsTestCase(unittest.TestCase):
    """Test case for Actors endpoints."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        # Create some sample actors for testing
        self.actor1 = Actor(name='Actor 1', age=30, gender='Male')
        self.actor2 = Actor(name='Actor 2', age=25, gender='Female')
        db.create_all()
        db.session.add_all([self.actor1, self.actor2])
        db.session.commit()

    def tearDown(self):
        """Tear down test fixtures after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test for successful retrieval of actors
    def test_get_actors_success(self):
        """Test successful retrieval of actors."""
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/actors', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Actor 1', response.data)
        self.assertIn(b'Actor 2', response.data)

    # Test for error behavior when no actors are available
    def test_get_actors_error(self):
        """Test error behavior when no actors are available."""
        # Delete all actors to simulate no actors available
        Actor.query.delete()
        db.session.commit()
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/actors', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'No actors', response.data)

    # Test for successful creation of a new actor
    def test_create_actor_success(self):
        """Test successful creation of a new actor."""
        new_actor_data = {'name': 'New Actor', 'age': 35, 'gender': 'Male'}
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post(
            '/actors', json=new_actor_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data.decode(
            'utf8').replace("'", '"'))['success'])

    # Test for error behavior when required fields are missing during actor
    # creation
    def test_create_actor_error_missing_fields(self):
        """Test error behavior when required fields are missing during actor creation."""
        new_actor_data = {'age': 35, 'gender': 'Male'}
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post(
            '/actors', json=new_actor_data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Name, age, and gender are required', response.data)

    # Test for successful update of an existing actor
    def test_update_actor_success(self):
        """Test successful update of an existing actor."""
        actor_id = self.actor1.id
        updated_actor_data = {'name': 'Updated Actor Name'}
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.patch(
            f'/actors/{actor_id}', json=updated_actor_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data.decode(
            'utf8').replace("'", '"'))['success'])

    # Test for error behavior when trying to update a non-existent actor
    def test_update_actor_error_nonexistent(self):
        """Test error behavior when trying to update a non-existent actor."""
        actor_id = 999  # Non-existent actor ID
        updated_actor_data = {'name': 'Updated Actor Name'}
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.patch(
            f'/actors/{actor_id}', json=updated_actor_data, headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Actor not found', response.data)

    # Test for successful deletion of an actor
    def test_delete_actor_success(self):
        """Test successful deletion of an actor."""
        actor_id = self.actor1.id
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.delete(f'/actors/{actor_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data.decode(
            'utf8').replace("'", '"'))['success'])

    # Test for error behavior when trying to delete a non-existent actor
    def test_delete_actor_error_nonexistent(self):
        """Test error behavior when trying to delete a non-existent actor."""
        actor_id = 999  # Non-existent actor ID
        token = token_data['roles']['Executive Producer']['jwt_token']
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.delete(f'/actors/{actor_id}', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Actor not found', response.data)


if __name__ == '__main__':
    unittest.main()
