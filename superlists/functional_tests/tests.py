import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase): # 用 `LiveServerTestCase` 來做 Django FT 的話, 會自動幫開 server 以及 產生 alias db for FT ifself.
    def setUp(self) -> None:
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

    # 記得要先開啟django servre才能跑
    def test_can_start_list_and_retrieve_it_later(self):

        # Edith has heard about a cool new online to-do app. She goes to check out its homepage.
        self.browser.get(self.live_server_url) # 不用自己指定測試用的 url 了

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

        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
        time.sleep(3)
        self.fail('Please CONTINUE from HERE to implement this test')

        # The page updates again, and now shows both items on her list.

        # Edith wonders whether the site will remember her list.
        # Then she sees that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')

