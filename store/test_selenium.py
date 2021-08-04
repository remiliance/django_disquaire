from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        username_input = self.selenium.find_element_by_name("Chercher un disque")
        username_input.send_keys('myuser')
        self.selenium.find_element_by_xpath('//input[@value="Chercher un disque"]').click()

class PlayerFormTest(LiveServerTestCase):

  def testform(self):
    selenium = webdriver.Chrome()
    #Choose your url to visit
    selenium.get('http://127.0.0.1:8000/')