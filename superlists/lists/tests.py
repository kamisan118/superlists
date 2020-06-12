from django.test import TestCase
from django.urls import resolve
from .views import homepage

# Create your tests here.

class SmokeTest(TestCase):
    def test_bad_math(self):
        self.assertEqual(1 + 1, 3)

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

