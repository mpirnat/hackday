from django.test import TestCase
from users.models import UserProfile
from django.contrib.auth.models import User


class UserProfileTest(TestCase):

    def test_image_url_generation(self):
        profile = UserProfile(user=User(email="test@example.com"))
        assert profile.image == ("http://gravatar.com/avatar/"
                                 "55502f40dc8b7c769880b10874abc9d0")
