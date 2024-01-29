from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Check_Result:
    def __init__(self, headless = False):
        if headless:
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            self.driver = webdriver.Chrome(options = options)
        else:
            self.driver = webdriver.Chrome()
        self.status_url = "https://www.acmicpc.net/status?top="

    def get_result(self, submission_id):
        """
        Returns (problem_id, result) for given submission id.
        Do not call this function outside.
        This function WAITS until the submission's result comes out.
        """
        desired_url = self.status_url + submission_id
        self.driver.get(desired_url)

        table = self.driver.find_element(By.ID, "status-table")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        entries = tbody.find_elements(By.TAG_NAME, "tr")

        if len(entries) == 0:
            raise Exception("submission not found")
        
        entry = entries[0]
        elems = entry.find_elements(By.TAG_NAME, "td")

        submission_wid = elems[0].text
        assert(submission_id == submission_wid)

        problem_id = int(elems[2].text)
        wait120 = WebDriverWait(self.driver, 120)
        result_locator = (By.XPATH, '//tr[@id="solution-{}"]//td[@class="result"]//span'.format(submission_id))
        cond1 = EC.text_to_be_present_in_element(result_locator, '기다리는 중')
        cond2 = EC.text_to_be_present_in_element(result_locator, '채점 준비 중')
        cond3 = EC.text_to_be_present_in_element(result_locator, '채점 중')
        wait120.until(EC.none_of(cond1, cond2, cond3))
        result = elems[3].text
        return (problem_id, result)

    def check_result(self, old_submission_id, new_submission_id):
        """
        Checks if the results of two submission ids are equivalent.
        will return True if they are the same,
        or it will return information about incorrect submission results.
        """
        (old_problem_number, old_result) = self.get_result(old_submission_id)
        (new_problem_number, new_result) = self.get_result(new_submission_id)

        if old_problem_number != new_problem_number:
            raise Exception("found mismatching submission pair")
        
        if old_result == new_result:
            return True
        else:
            return "Incorrect submission result for Problem {} : Expected {}, but got {}".format(
                old_problem_number, old_result, new_result)

"""
checkEngine = Check_Result()
old_id = input("Old Submission ID: ")
new_id = input("New Submission ID: ")
result = checkEngine.check_result(old_id, new_id)
print(result)
"""

"""
checkEngine = Check_Result()
while True:
    submission_id = input("Submission ID: ")
    print(checkEngine.get_result(submission_id))
"""
