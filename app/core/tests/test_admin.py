from django.test import (
    TestCase,
    Client
)
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        # creating client
        self.client = Client()

        # creating admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@fakemail.com',
            password='hello123'
        )
        # login the user with Django authentication with the helper function `force_login` # noqa: E501
        self.client.force_login(self.admin_user)

        # creating normal user
        self.user = get_user_model().objects.create_user(
            email='test@fakemail.com',
            password='hello456',
            name='John Doe'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # `reverse` uses a string composed by: app:named_url
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
