# import pytest
# from django.urls import reverse, resolve
#
# from sonsuz.users.models import User
#
# pytestmark = pytest.mark.django_db
#
#
# def test_detail(user: User):
#     assert (
#         reverse("users:detail", kwargs={"username": user.username})
#         == f"/users/{user.username}/"
#     )
#     assert resolve(f"/users/{user.username}/").view_name == "users:detail"
#
#
# def test_update():
#     assert reverse("users:update") == "/users/~update/"
#     assert resolve("/users/~update/").view_name == "users:update"
#
#
# def test_redirect():
#     assert reverse("users:redirect") == "/users/~redirect/"
#     assert resolve("/users/~redirect/").view_name == "users:redirect"
from django.urls import reverse, resolve
from test_plus import TestCase


class TestUser(TestCase):
    def setUp(self) -> None:
        self.user = self.make_user(username='testuser', password='password')

    def test_detail_reverse(self):
        self.assertEqual(reverse("users:detail", kwargs={"username": self.user.username}),
                         f"/users/{self.user.username}/")

    def test_detail_resolve(self):
        self.assertEqual(resolve(f"/users/{self.user.username}/").view_name, 'users:detail')

    def test_update_reverse(self):
        self.assertEqual(reverse("users:update"), f"/users/~update/")

    def test_update_resolve(self):
        self.assertEqual(resolve("/users/~update/").view_name, "users:update")

    def test_redirect_reverse(self):
        self.assertEqual(reverse("users:redirect"), f"/users/~redirect/")

    def test_redirect_resolve(self):
        self.assertEqual(resolve("/users/~redirect/").view_name, "users:redirect")
