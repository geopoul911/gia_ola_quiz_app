from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# create user URL
CREATE_USER_URL = reverse('user:register')
TOKEN_URL = reverse('user:login')


# helper function to create some example users
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# tests for public APIs (without any authentication - eg: create user)
class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    # test creating user with valid payload is successful
    def test_create_valid_user_success(self):
        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'Lebron James'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))  # check correct password was set
        self.assertNotIn('password', res.data)  # ensure password is not returned in response payload

    # test duplicate user creation fails
    def test_user_exists(self):
        payload = {'email': 'test@test.com', 'password':'test123'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Test that a token is created for the user
    def test_create_token_for_user(self):
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Test that token is not created if invalid credentials are given
    def test_create_token_invalid_credentials(self):
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Test that token is not created if user doens't exist
    def test_create_token_no_user(self):
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
