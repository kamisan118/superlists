from django.test import TestCase
from django.urls import resolve
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpRequest
from .views import home_page

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UserAdmin.settings")
django.setup()

class SmokeTest(TestCase):
    def test_bad_math(self):
        self.assertNotEqual(1 + 1, 3)

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        # ==============若直接對 response 的 contenct bytes 做解讀
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do list</title>', response.content)
        # self.assertTrue(response.content.endswith(b'</html>'))

        # ==============若直接比對 reply 過來的 template content
        expected_html = render_to_string('home.html') # 建立ground truth!
        request = HttpRequest()
        response = home_page(request)
        self.assertEqual(response.content.decode(), expected_html) # 記得reponse要先decode才能比對

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)

        # expected_html = render_to_string('home.html', {'new_text_item': 'A new list item'}, request=request) # 把 home.html 給 render, 並且pass in params. 然後render 成 str (用以比較final html)
        expected_html = render_to_string('home.html', {'new_text_item': 'A new list item'})  # 把 home.html 給 render, 並且pass in params. 然後render 成 str (用以比較final html)

        # 怎辦--------------csrf token val.不一樣@@
        self.assertEqual(response.content.decode(), expected_html)
