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
    target_str = 'A new list item'

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

    def save_new_item_through_post_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = self.target_str
        response = home_page(request) # 直接塞 req. 進去 view 就可以獲得 response
        return response

    def test_home_page_can_save_a_POST_request(self):
        response = self.save_new_item_through_post_request()

        # 檢查有正確塞到db中
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first() # Item 是個自訂的 model 隨時可以叫出來做資料的存儲
        self.assertEqual(new_item.text, self.target_str)
        return response

    def test_home_page_only_saves_items_when_neccessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_can_save_a_POST_request_should_redirect_first(self):
        response = self.save_new_item_through_post_request()

        # check if after POST, can redirect rather than rander directly
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


    def test_home_page_display_all_list_items(self):
        Item.objects.create(text='itemy 1') # 可以直接create 這樣就不用 new then save()
        Item.objects.create(text='itemy 2')  # 可以直接create 這樣就不用 new then save()

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemy 1', response.content.decode())
        self.assertIn('itemy 2', response.content.decode())
