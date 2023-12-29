from selenium import webdriver
from selenium.webdriver.common.by import By

class Source:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(options = options)
        self.login_cookie = None
        
    def get_source(self, login_cookie, submission_id):
        source_url = "https://www.acmicpc.net/source/" + str(submission_id)
        self.driver.get(source_url)
        if self.login_cookie != login_cookie:
            self.login_cookie = login_cookie
            self.driver.add_cookie(login_cookie)
            self.driver.get(source_url) # retry loading the page with the cookie
        
        textarea = self.driver.find_element(By.NAME, "source")
        source = textarea.get_attribute("value")
        return source


# from login import Login
# from getpass import getpass
# loginObject = Login()
# user_id = input("Input id: ")
# password = getpass("Input password: ")
# login_cookie = loginObject.login(user_id, password)

# sourceEngine = Source()
# print(sourceEngine.get_source(login_cookie, 56892412))
# print(sourceEngine.get_source(login_cookie, 54530876))
        
