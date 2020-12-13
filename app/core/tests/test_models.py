from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        expected_email = 'test@fakemail.com'
        expected_password = 'hello123'

        user = get_user_model().objects.create_user(
            email=expected_email,
            password=expected_password
        )

        self.assertEqual(user.email, expected_email)
        self.assertTrue(user.check_password(expected_password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@FAKEMAIL.COM'
        user = get_user_model().objects.create_user(
            email=email,
            password='hello123'
        )

        self.assertEqual(user.email, email.lower())
