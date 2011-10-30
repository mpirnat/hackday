from django.test import TestCase


class TestWhenAccessingHomepage(TestCase):
    fixtures = ['hello']

    def test_displays_recent_blog_posts(self):
        response = self.client.get('/')
        self.assertTrue('Hello World!' in response.content)
