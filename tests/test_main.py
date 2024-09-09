import unittest
import json
from random import randrange

from main import app, db
# from app import app, db  # Assuming `app` is the Flask instance and `db` is your SQLAlchemy instance
from models.user import User
from services.auth_service import AuthService


class AuthTestCase(unittest.TestCase):
    username = 'testuser_' + randrange(0, 10000, 1).__str__()
    password = 'testpassword'
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMywiZXhwIjoxNzI1ODgwOTkwLCJqdGkiOiJhMGVkNWNiNS0yYWM3LTRkNmItOGI2Zi04ODA1YjU3MThkOWUifQ.MR7oKg255CMdaNeTr4JYAgtAkmKSo0IBaL4eWHMMGVc"

    @classmethod
    def setUp(cls):
        # Set up the Flask testing client and database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
        cls.client = app.test_client()
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()  # Create tables

        cls.username = 'testuser_' + randrange(0, 10000, 1).__str__()
        cls.password = 'testpassword'

        response = cls.client.post('/user', data=json.dumps({
            'username': cls.username,
            'password': cls.password
        }), content_type='application/json')
        assert response.status_code == 201

        # Log in to get a token
        response = cls.client.post('/authenticate_user', data=json.dumps({
            'username': cls.username,
            'password': cls.password
        }), content_type='application/json')
        data = json.loads(response.data.decode())
        cls.token = data['access_token']

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_create_user(self):
        response = self.client.post('/user', data=json.dumps({
            'username': 'newuser_' + str(randrange(0, 10000)),
            'password': 'newpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created successfully", response.get_data(as_text=True))

    # def test_login(self):
    #     response = self.client.post('/authenticate_user', data=json.dumps({
    #         'username': self.username,
    #         'password': self.password
    #     }), content_type='application/json')
    #     print("Yes ", response.get_data(as_text=True))
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data.decode())
    #     self.assertIn('access_token', data)
    #     self.token = data['access_token']

    def test_validate_token(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.post('/validate_token', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is valid', response.get_data(as_text=True))
        self.token = json.loads(response.data.decode())['token']

    def test_get_user(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.get('/user', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.username, response.get_data(as_text=True))

    def test_update_user(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.put('/user', data=json.dumps({
            'username': 'newusername',
            'password': 'newpassword'
        }), headers=headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User updated successfully', response.get_data(as_text=True))

    def test_delete_user(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.delete('/user', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted successfully', response.get_data(as_text=True))

    def test_logout(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.post('/logout', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User has been logout. Token has been revoked', response.get_data(as_text=True))

    def test_protected_route_without_token(self):
        response = self.client.get('/user')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token is missing', response.get_data(as_text=True))

    def test_protected_route_with_invalid_token(self):
        invalid_token = 'Bearer invalid_token'
        response = self.client.get('/user', headers={'Authorization': invalid_token})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid or expired token', response.get_data(as_text=True))

    def test_replay_attack(self):
        token = self.token
        headers = {'Authorization': f'Bearer {token}'}  # Valid token
        response = self.client.get('/user', headers=headers)
        self.assertEqual(response.status_code, 200)
        replayed_request = self.client.get('/user', headers=headers)
        self.assertEqual(replayed_request.status_code, 401)


if __name__ == '__main__':
    unittest.main()
