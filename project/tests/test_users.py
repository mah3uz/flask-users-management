# project/tests/test_users.py

import json
from project.tests.base import BaseTestCase
from project.api.models import User
from project import db


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()

    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure new user can be added on database"""
        with self.client:
            response = self.client.post(
                '/users',
                data = json.dumps(dict(
                    username = 'mahfuz',
                    email = 'mah3uz@gmail.com'
                )),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('mah3uz@gmail.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON is empty."""
        with self.client:
            response = self.client.post(
                '/users',
                data = json.dumps(dict()),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_key(self):
        """Ensure error is thrown if JSON object does not have a username key."""
        with self.client:
            response = self.client.post(
                '/users',
                data = json.dumps(dict(email = 'mah3uz@gmail.com')),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_user(self):
        """Ensure error is thrown if the email already exist."""
        with self.client:
            self.client.post(
                '/users',
                data = json.dumps(dict(
                    username = 'mahfuz',
                    email = 'mah3uz@gmail.com',
                )),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='mahfuz',
                    email='mah3uz@gmail.com',
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. that email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behave correctly."""
        user = add_user('mahfuz', 'mah3uz@gmail.com')

        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('mahfuz', data['data']['username'])
            self.assertIn('mah3uz@gmail.com',data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/0')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behave correctly"""
        add_user('mahfuz', 'mah3uz@gmail.com')
        add_user('alamin', 'alamin@gmail.com')

        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn('mahfuz', data['data']['users'][0]['username'])
            self.assertIn('mah3uz@gmail.com', data['data']['users'][0]['email'])
            self.assertIn('alamin', data['data']['users'][1]['username'])
            self.assertIn('alamin@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])
