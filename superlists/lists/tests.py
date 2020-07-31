import os
import django
from django.test import TestCase
from django.urls import resolve
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpRequest

from pmlib.django_helper import html_tool
from lists.views import home_page
from lists.models import Item


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(second_saved_item.text, second_item.text)


class SmokeTest(TestCase):
    def test_bad_math(self):
        self.assertNotEqual(1 + 1, 3)

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_returns_correct_html(self):
        # ==============若直接對 response 的 contenct bytes 做解讀
        # request = HttpRequest()
        # response = home_page(request)
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do list</title>', response.content)
        # self.assertTrue(response.content.endswith(b'</html>'))

        # ==============若直接比對 reply 過來的 template content
        expected_html = render_to_string('home.html') # 建立ground truth!
        request = HttpRequest()
        response = home_page(request)

        # should remove forms (因有csrf token field 的關係, 不這麼做的話會出錯...)
        # decoded_respone = response.content.decode()
        decoded_respone = html_tool.forms_remover(response.content.decode())
        expected_html = html_tool.forms_remover(expected_html)

        self.assertEqual(decoded_respone, expected_html) # 記得reponse要先decode才能比對

    def test_home_page_can_save_a_POST_request(self):
        target_str = 'A new list item'
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = target_str
        response = home_page(request)

        # 沒加入 request 的話會沒有 csrf token
        expected_html = render_to_string('home.html', {'new_text_item': target_str})  # 把 home.html 給 render, 並且pass in params. 然後render 成 str (用以比較final html)
        # 就算加入了request, csrf token val.仍會每次render都給不一樣, so得將form remove from 我們的test
        decoded_respone = html_tool.forms_remover(response.content.decode())
        expected_html = html_tool.forms_remover(expected_html)

        self.assertEqual(decoded_respone, expected_html)

