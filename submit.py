from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains, Keys
import pyperclip
import time

class Submit:
    def __init__(self, login_cookie):
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        self.driver = webdriver.Chrome(options = options)
        self.login_cookie = login_cookie
        self.fetch_language_ids()
        self.fetch_source_code_open_policy()
        
    def lang_to_value__(language):
        """Only used when language is not found in the drop list
        """
        
    def fetch_language_ids(self):
        language_setting_url = "https://www.acmicpc.net/setting/language"
        self.driver.get(language_setting_url)
        self.driver.add_cookie(self.login_cookie)
        self.driver.get(language_setting_url) # retry loading the page with the cookie
        show_languages = self.driver.find_element(By.ID, "show_languages")
        l1 = show_languages.find_elements(By.CLASS_NAME, "list-group-item")
        hide_languages = self.driver.find_element(By.ID, "hide_languages")
        l2 = hide_languages.find_elements(By.CLASS_NAME, "list-group-item")
        l = l1 + l2
        
        self.all_languages = []
        for lang in l:
            self.all_languages.append({'name': lang.text, 'id': lang.get_attribute("data-language-id")})
        
    def fetch_source_code_open_policy(self):
        # open, close, onlyaccepted
        source_setting_url = "https://www.acmicpc.net/setting/solution"
        self.driver.get(source_setting_url)
        radio = self.driver.find_elements(By.NAME, "code_open")
        for v in radio:
            if v.is_selected:
                self.code_open = v.get_attribute("value")
        
    def submit(self, language, source_code, problem_id, code_open = None):
        # [Step 1-1] Find language id
        for lang in self.all_languages:
            if lang['name'] == language:
                found = True
                language_id = lang['id']
                print("found language_id:", language_id)
                break
        if not found:
            return "Language Not Found"

        # [Step 2-0] Open submit url
        submit_url = "https://www.acmicpc.net/submit/" + str(problem_id)
        self.driver.get(submit_url)

        # [Step 2-1] Select language
        select = Select(self.driver.find_element(By.ID, "language"))
        self.driver.execute_script("""document.getElementById('language').style.display='block';""")
        try:
            a = 2 / 0
            select.select_by_value(language_id)
        except:
            add_option_script = """
                document.getElementById('language').innerHTML+='<option value="{}" selected>{}</option>';
            """.format(language_id, language)
            self.driver.execute_script(add_option_script)
            select.select_by_value(language_id)

        # [Step 2-2] Select source code open policy
        policy = self.code_open if code_open == None else code_open
        radio = self.driver.find_elements(By.NAME, "code_open")
        for v in radio:
            if v.get_attribute("value") == policy:
                v.click()
        
        # [Step 2-3] Write source code
        # [참고: https://steins-gate.tistory.com/entry/%EB%B0%B1%EC%A4%80-%EC%9E%90%EB%8F%99-%EC%A0%9C%EC%B6%9C-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8]        
        cm = self.driver.find_element(By.CLASS_NAME, "CodeMirror")
        cm.find_elements(By.CLASS_NAME, "CodeMirror-line")[0].click()
        textarea = cm.find_element(By.CSS_SELECTOR, "textarea")
        pyperclip.copy(source_code)
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        
        # [Step 2-4] Click submit button
        self.driver.find_element(By.ID, "submit_button").click()
        
        return "submitted to problem id: {}".format(problem_id)
    
    def get_result(self, submission_id):
        pass
    
    def compare_result(self, old_submission_id, new_submission_id):
        pass


# from login import Login
# from getpass import getpass
# loginObject = Login()
# user_id = input("Input id: ")
# password = getpass("Input password: ")
# login_cookie = loginObject.login(user_id, password)

hello_world_src = '''#include <cstdio>
int main()
{
    printf("Hello, World!\\n");
    return 0;
}
'''

test_src = '''#include <cstdio>
int main()
{
    // TEST!
    return 0;
}
'''

# submitEngine = Submit(login_cookie)
# res = submitEngine.submit('Ruby', hello_world_src, 1001)
# print(str(res))
# res = submitEngine.submit('OCaml', test_src, 1004)
# print(str(res))