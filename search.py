from selenium import webdriver
from selenium.webdriver.common.by import By
import json

class Search:
    def __init__(self, filename = "search_result.json"):
        self.filename = filename
        
    def load_from_file(self):
        with open(self.filename, "r", encoding = 'utf-8') as f:
            history = json.load(f)
        print("Finish loading", self.filename + ": total {} submissions".format(len(history)))
        print("most recent => \t", history[0])
        print("oldest => \t", history[-1])
        return history
    
    def save_to_file(self, history):
        with open(self.filename, "w", encoding = 'utf-8') as f:
            json.dump(history, f, ensure_ascii = False, indent = 4)
        print("Successfully saved to", self.filename)

    def load_from_web(self, user_id, start = 0, end = 0):
        """Load submission history from BOJ website.
        
        Returns all submissions with submission_id is in [start, end]. (endpoints included)
        
        If end = 0, then returns all submissions to the most recent submission.
        """
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        self.driver = webdriver.Chrome(options = options)
        if end == 0:
            status_url = "https://www.acmicpc.net/status?user_id=" + user_id
        else:
            status_url = "https://www.acmicpc.net/status?user_id=" + user_id + "&top=" + str(end)
        
        print("Start loading submission history from BOJ website...")
        history = []
        while True:
            self.driver.get(status_url)
            table = self.driver.find_element(By.ID, "status-table")
            tbody = table.find_element(By.TAG_NAME, "tbody")
            entries = tbody.find_elements(By.TAG_NAME, "tr")
            if len(entries) == 0:
                break
            
            finished = False
            found = []
            for entry in entries:
                elems = entry.find_elements(By.TAG_NAME, "td")
                submission_id = int(elems[0].text)
                problem_id = int(elems[2].text)
                result = elems[3].text
                language = elems[6].text
                
                if submission_id < start:
                    finished = True
                    break
                    
                found.append({"submission_id": submission_id, "problem_id": problem_id, "result": result, "language": language})
            
            history += found
            print("found: {}~{}({} submissions), now total: {} submissions".format(
                  found[0]["submission_id"], found[-1]["submission_id"], len(found), len(history)))
            if finished:
                break
            
            top = history[-1]["submission_id"] - 1
            status_url = "https://www.acmicpc.net/status?user_id=" + user_id + "&top=" + str(top)
            
        print("Finish loading submission history from BOJ website.")
        self.driver.quit()
        return history
        

# searchEngine = Search()
# history = searchEngine.load_from_web("povwhm", 0, 0)
# searchEngine.save_to_file(history)
# history = searchEngine.load_from_file()