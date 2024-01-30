from login import Login
from getpass import getpass
from search import Search
from source import Source
from submit import Submit

############ LOGIN ############
loginObject = Login()
old_id = input("[0-1] Input original id: ")
old_password = getpass("[0-1] Input password: ")
old_cookie = loginObject.login(old_id, old_password)
print("Login Succeeded!\n")

new_id = input("[0-2] Input new id: ")
new_password = getpass("[0-2] Input password: ")
new_cookie = loginObject.login(new_id, new_password)
print("Login Succeeded!\n")
loginObject.quit()

############ SEARCH ############
while True:
    ans = input("[1] Crawl your submission history from BOJ website?(Y) Or use saved JSON file?(N): ")
    if ans == "Y" or ans == 'y':
        prompt = """[1-1] Please enter the submission_id lower_bound and upper_bound(endpoints included): ex) 1000000 1200000
        (just press ENTER to access all submissions)
        """
        i = input(prompt)
        if i == "":
            searchEngine = Search()
            history = searchEngine.load_from_web(old_id, 0, 0)
        else:
            [a, b] = list(map(int, i.split()))
            if a > b:
                print("ERROR: lower_bound is bigger than upper_bound")
                continue
            searchEngine = Search()
            history = searchEngine.load_from_web(old_id, a, b)
        searchEngine.save_to_file(history)
        break
    elif ans == 'N' or ans == 'n':
        prompt = """[1-1] Please enter the saved JSON file name:
        (just press ENTER to use 'search_result.json')
        """
        file_name = input(prompt)
        if file_name == "":
            file_name = "search_result.json"
        searchEngine = Search(file_name)
        history = searchEngine.load_from_file()
        break

############ MAIN LOOP ############
# sourceEngine = Source()
# submitEngine = Submit(new_cookie)
# for hist in history:
#    old_submission_id, problem_id, old_result, language =\
#        hist['submission_id'], hist['problem_id'], hist['result'], hist['language']
        
#    source_code = sourceEngine.get_source(old_cookie, old_submission_id)
#    res = submitEngine.submit(language, source_code, problem_id)
    
    
    
    