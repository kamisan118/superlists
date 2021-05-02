import os
import django
from django.test import TestCase
from django.urls import resolve
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpRequest

from pmlib.django_helper import html_tool
from lists.views import home_page
from lists.models import Item, List


class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_item.text)
        self.assertEqual(second_saved_item.list, list_)


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

    def test_home_page_does_not_add_any_items(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


    # # TDD book-p.118 說要刪掉但我決定不刪 因為她是比較基礎的在DjangoTestClient jump in 前的 更基礎的寫法
    # def test_home_page_display_all_list_items(self):
    #     Item.objects.create(text='itemy 1') # 可以直接create 這樣就不用 new then save()
    #     Item.objects.create(text='itemy 2')  # 可以直接create 這樣就不用 new then save()
    #
    #     request = HttpRequest()
    #     response = home_page(request)
    #
    #     self.assertIn('itemy 1', response.content.decode())
    #     self.assertIn('itemy 2', response.content.decode())


class NewListTest(TestCase):
    target_str = 'A new list item'

    def save_new_list_through_post_request(self):
        response = self.client.post(
            '/lists/new',
            data={
                'item_text': self.target_str
            }
        )
        return response

    def test_saving_a_POST_request(self):
        response = self.save_new_list_through_post_request()

        # 檢查有正確塞到db中
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first() # Item 是個自訂的 model 隨時可以叫出來做資料的存儲
        self.assertEqual(new_item.text, self.target_str)
        return response

    # def test_home_page_can_save_a_POST_request_should_redirect_first(self):
    def test_redirects_after_POST(self):
        response = self.save_new_list_through_post_request()
        list_ = List.objects.first()

        # check if after POST, can redirect rather than render directly
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/%d/' % (list_.id,))


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={
                'item_text': 'A new item for an existing list'
            }
        )
        self.assertNotEqual(response.status_code, 404)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={
                'item_text': 'A new item for an existing list'
            }
        )

        # check if after POST, can redirect rather than render directly
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/%d/' % (correct_list.id,))
        # self.assertRedirects(response, 'list/%d/' % (correct_list.id,))


# 利用 DjangoTestClient, 同時測試 view, model, url mapping (比個別測試要來的更方便..., 是Djago當中特有的寫法)
class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'lists.html')

    def test_display_all_items_for_that_list(self):
        list_ = List.objects.create()

        Item.objects.create(text='itemy 1', list=list_) # 可以直接create 這樣就不用 new then save()
        Item.objects.create(text='itemy 2', list=list_)  # 可以直接create 這樣就不用 new then save()

        response = self.client.get('/lists/%d/' % (list_.id,))

        self.assertContains(response, 'itemy 1')
        self.assertContains(response, 'itemy 2')
        self.assertNotContains(response, 'other list itemy 1')
        self.assertNotContains(response, 'other list itemy 2')