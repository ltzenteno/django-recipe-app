from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Helper function to create a user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test the users API (public)
    (each method refreshes the test DB data)
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid pyload is successful"""
        payload = {
            'email': 'test@fakemail.com',
            'password': 'testpass',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        # assert that it returns a 201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # assert that the user was created
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))

        # assert that the password field is not returned in the created object
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@fakemail.com',
            'password': 'testpass',
            'name': 'Test Name'
        }

        # first create the user via `create_user`
        create_user(**payload)

        # try to create the user via POST
        res = self.client.post(CREATE_USER_URL, payload)

        # asserting that the endpoint returns a 400
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@fakemail.com',
            'password': 'pw',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)
