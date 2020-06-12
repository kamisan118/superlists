from django.test import TestCase
from django.urls import resolve
from django.http import HttpResponse, HttpRequest
from .views import home_page

# Create your tests here.

class SmokeTest(TestCase):
    def test_bad_math(self):
        self.assertEqual(1 + 1, 3)

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do list</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
