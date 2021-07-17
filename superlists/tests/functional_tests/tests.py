import unittest
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

# 用 `LiveServerTestCase` 來做 Django FT 的話,
# 會自動幫開 server 以及 產生 alias db for FT ifself.
class NewVisitorTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_url = None
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                break
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super.tearDownClass()

    def setUp(self) -> None:
        if(self.server_url == None):
            self.server_url = self.live_server_url
        self.browser = webdriver.Firefox(log_path=r"C:\DBoxs\prim\Dropbox\repo\tdd-lern-proj\p1\geckodriver.log")

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(any(row.text == "1: Buy peacock feathers" for row in rows),
        #                 f"New to-do item did not appear in the table -- its text was:\n{table.text}")
        # 更簡潔的寫法
        self.assertIn(row_text, [row.text for row in rows])

    # 記得要先開啟django server才能跑
    def test_can_start_list_and_retrieve_it_later(self):

        # Edith has heard about a cool new online to-do app. She goes to check out its homepage.
        self.browser.get(self.server_url) # 不用自己指定測試用的 url & port 了

        # She notices the page title and header mention to-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Enter a to-do item")
        # She types "Buy peacock feathers" into a text box (Edith's hobby is tying fly-fishing lures)
        inputbox.send_keys("Buy peacock feathers")
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+/')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 沒裝這個的話會碰到 `selenium.common.exceptions.StaleElementReferenceException`
        # 因為你撈到前一個 page 的 id, 但 page 被 refresh 結果就變成 DOM 消失 找不到
        time.sleep(1)

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Enter a to-do item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list.
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Now a new user, Francis, comes along to the site.
        ## We use a new browser session to make sure that no information
        ## of Edith is coming through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There's no sign of Edith's list
        # list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item.
        # He is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+/')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep.

        # TODO ====================>
        print("DONE. Please CONTINUE from HERE to implement this test.")
        # self.fail('Please CONTINUE from HERE to implement this test')



        # Edith wonders whether the site will remember her list.
        # Then she sees that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

# 用 `StaticLiveServerTestCase` 來做 Django FT 的話, 才能夠認得到static files...
class NewVisitorStaticTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_url = None
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                break
        super().setUpClass()

    def setUp(self) -> None:
        if(self.server_url == None):
            self.server_url = self.live_server_url
        self.browser = webdriver.Firefox(log_path=r"C:\DBoxs\prim\Dropbox\repo\tdd-lern-proj\p1\geckodriver.log")

    def tearDown(self) -> None:
        self.browser.quit()

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)
        # 限制windows size (才能夠比較accurate的做location-based的assertertion...)
        self.browser.set_window_size(1024, 768)

        # She notice the input box is nicely centered.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10 # almost, 的tolerance
        )

        # She starts a new list and see the input is nicely centered there too,
        inputbox.send_keys('testing\n')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10 # almost, 的tolerance
        )




if __name__ == '__main__':
    unittest.main(warnings='ignore')

