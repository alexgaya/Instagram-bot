from selenium import webdriver
import os
import time
import configparser

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FamousAccountsScraping:

    def __init__(self):
        self.driver = webdriver.Chrome('chromedriver.exe')

    def socialblade_com(self):
        self.driver.get('https://socialblade.com/instagram/top/100/followers')
        time.sleep(2)

    def fetch_users(self):
        for i in range(6, 106):
            xpath = f'/html/body/div[9]/div[2]/div[{i}]/div[3]/a'
            user = str(self.driver.find_element_by_xpath(
                xpath).get_attribute('href'))
            user = user.replace('https://socialblade.com/instagram/user/', '')
            print(user)
            yield user


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
        self.driver.implicitly_wait(3)
        self.driver.get(f'{self.base_url}accounts/login/')
        self.driver.find_element_by_name(
            "username").send_keys(self.username)
        self.driver.find_element_by_name(
            "password").send_keys(self.password)
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button').click()
        self.driver.implicitly_wait(3)

    def nav_user(self, user):
        self.driver.get(f'{self.base_url}{user}')

    def isFollowing(self, button):
        if button.text == 'Following':
            return True
        return False

    def switched_to_following(self, button):
        return self.isFollowing(button)

    def follow_user(self, user):
        self.nav_user(user)

        time.sleep(5)
        # follow_button = self.driver.find_element_by_xpath(
        #     '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
        # follow_button.click()
        clickable = True
        try:
            element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')))
            if self.isFollowing(element):
                print('already following')
                return
            element.click()
            time.sleep(3)
            # //*[@id="react-root"]/section/main/div/header/section/div[1]/button
            # //*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button
        except:
            print('Element is not clickable, trying with next...')
            clickable = False

        if not clickable:
            try:
                element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/button')))
                if self.isFollowing(element):
                    print('already following')
                    return
                element.click()
                time.sleep(3)
            except:
                print('Element is not clickable, skiping user')

        time.sleep(5)


if __name__ == "__main__":

    botAcc = FamousAccountsScraping()
    botAcc.socialblade_com()

    cparser = configparser.ConfigParser()
    cparser.read('./config.ini')
    username = cparser.get('auth', 'username')
    password = cparser.get('auth', 'password')

    bot = InstagramBot(username, password)
    time.sleep(3)
    bot.driver.maximize_window()
    user_generator = botAcc.fetch_users()
    for user in user_generator:
        bot.follow_user(user)
