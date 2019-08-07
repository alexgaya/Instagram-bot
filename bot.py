from selenium import webdriver
import os
import time
import configparser


class InstagramBot:
    """
    Initializes an instance of the Instagrambot class. 
    Call the login method to authenticate a user with IG

    Args:
      username:str: The Instagram username
      password:str: The Instagram password

    Attributes:
      driver:Selenium.webdriver.Chrome: The Chromedriver that is used to automate browser actions
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.base_url = "https://instagram.com/"
        self.login()

    def login(self):
        self.driver.get(f'{self.base_url}accounts/login/')
        self.driver.find_element_by_name(
            "username").send_keys(self.username)
        self.driver.find_element_by_name(
            "password").send_keys(self.password)
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button').click()

    def nav_user(self, user):
        self.driver.get(f'{self.base_url}{user}')

    def follow_user(self, user):
        self.nav_user(user)
        time.sleep(3)
        follow_button = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
        follow_button.click()


if __name__ == "__main__":

    cparser = configparser.ConfigParser()
    cparser.read('./config.ini')
    username = cparser.get('auth', 'username')
    password = cparser.get('auth', 'password')

    bot = InstagramBot(username, password)
    time.sleep(3)
    bot.follow_user('garyvee')
