from selenium import webdriver
from selenium.webdriver.common.by import By

class Submit:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        self.driver = webdriver.Chrome(options = options)
        self.login_cookie = None
        self.all_languages = None
        self.code_open = None
        
    def lang_to_value__(language):
        """Only used when language is not found in the drop list
        """
        
    def submit(self, login_cookie, language, source_code, problem_id):
        # [Step 1-0] Fetch language id list if not yet fetched
        if self.all_languages == None:
            language_setting_url = "https://www.acmicpc.net/setting/language"
            self.driver.get(language_setting_url)
            if self.login_cookie != login_cookie:
                self.login_cookie = login_cookie
                self.driver.add_cookie(login_cookie)
                self.driver.get(language_setting_url) # retry loading the page with the cookie
            show_languages = self.driver.find_element(By.ID, "show_languages")
            l1 = show_languages.find_elements(By.CLASS_NAME, "list-group-item")
            hide_languages = self.driver.find_element(By.ID, "hide_languages")
            l2 = hide_languages.find_elements(By.CLASS_NAME, "list-group-item")
            self.all_languages = l1 + l2
            
        # [Step 1-1] Find language id
        for lang in self.all_languages:
            if lang.text == language:
                found = True
                language_id = lang.get_attribute("data-language-id")
                print("found language_id:", language_id)
                break
        if not found:
            return "Language Not Found"
            
        # [Step 1-2] Fetch source code open policy if not yet fetched
        if self.code_open == None:
            source_setting_url = "https://www.acmicpc.net/setting/solution"
            self.driver.get(source_setting_url)
            if self.login_cookie != login_cookie:
                self.login_cookie = login_cookie
                self.driver.add_cookie(login_cookie)
                self.driver.get(source_setting_url) # retry loading the page with the cookie
            radio = self.driver.find_elements(By.NAME, "code_open")
            for v in radio:
                if v.is_selected:
                    self.code_open = v.get_attribute("value")
                    
        # [Step 2-0] Select language
        
        
        # [Step 2-1] Write source code
        
        
        return "submitted to problem id: {}".format(problem_id)
    
    def get_result(self, submission_id):
        pass
    
    def compare_result(self, old_submission_id, new_submission_id):
        pass


from login import Login
from getpass import getpass
loginObject = Login()
user_id = input("Input id: ")
password = getpass("Input password: ")
login_cookie = loginObject.login(user_id, password)

hello_world_src = '''#include <cstdio>
int main()
{
    printf("Hello, World!\\n");
    return 0;
}
'''

submitEngine = Submit()
res = submitEngine.submit(login_cookie, 'Ruby', hello_world_src, 1001)
print(str(res))