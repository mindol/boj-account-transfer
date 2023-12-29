from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Login:
    def __init__(self, detach = False):
        self.driver = webdriver.Chrome()
        self.wait10 = WebDriverWait(self.driver, 10)

    def login(self, user_id, password):
        login_url = "https://www.acmicpc.net/login"
        self.driver.get(login_url)

        id_input = self.driver.find_element(By.NAME, "login_user_id")
        id_input.send_keys(user_id)
        
        pw_input = self.driver.find_element(By.NAME, "login_password")
        pw_input.send_keys(password)
        
        login_btn = self.driver.find_element(By.ID, "submit_button")
        login_btn.click()
        self.wait10.until(EC.title_is("Baekjoon Online Judge"))
        if self.driver.title != "Baekjoon Online Judge":
            raise Exception("login failed")
        
        login_cookie = self.driver.get_cookie("OnlineJudge")
        print('login_cookie:', login_cookie)
        
        self.driver.quit()
        return login_cookie
