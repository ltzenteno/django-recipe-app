from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@fakemail.com', password='hello123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


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

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            # anything that runs inside the `assertRaises` should raise a ValueError, if it does not raise a ValueError then the test fails # noqa: E501
            get_user_model().objects.create_user(
                email=None,
                password='hello123'
            )

    def test_create_new_super_user(self):
        """Test creating a new super user"""
        user = get_user_model().objects.create_superuser(
            email='test@fakemail.com',
            password='hello123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00,
        )

        self.assertEqual(str(recipe), recipe.title)
