from login import Login
from getpass import getpass
from search import Search
from source import Source
from submit import Submit
from check_result import Check_Result
import json

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
sourceEngine = Source()
submitEngine = Submit(new_cookie)
checkEngine = Check_Result()

total = len(history)
success_cnt = 0
success_submissions = []
submit_failed_cnt = 0
submit_failed_submissions = []
inconsistent_cnt = 0
inconsistent_submissions = []

for idx, hist in enumerate(history):
    old_submission_id, problem_id, old_result, language =\
        hist['submission_id'], hist['problem_id'], hist['result'], hist['language']
    
    # Current Stat
    print("[2 - Current Stats] {} Success, {} Submit fails, {} Inconsistent results, {} left"\
        .format(success_cnt, submit_failed_cnt, inconsistent_cnt, total - idx))
    print("[{}/{}] Transferring submission id: {}, problem id: {}".format(idx, total, old_submission_id, problem_id))
    
    # Get source code
    source_code = sourceEngine.get_source(old_cookie, old_submission_id)
    
    # Submit
    try:
        new_submission_id, submit_result = submitEngine.submit(language, source_code, problem_id)
        print(submit_result)
    except:
        print('Submit failed to problem id: {}, submission id: {}'.format(problem_id, old_submission_id))
        submit_failed_cnt += 1
        submit_failed_submissions.append({'old_submission_id': old_submission_id})
        continue
    
    # Check result
    check_result = checkEngine.check_result(old_submission_id, new_submission_id)
    if check_result == True:
        print('Result check finished')
        success_cnt += 1
        entry = {'old_submission_id': old_submission_id, 'new_submission_id': new_submission_id}
        success_submissions.append(entry)
    else:
        print(check_result)
        inconsistent_cnt += 1
        entry = {'old_submission_id': old_submission_id, 'new_submission_id': new_submission_id, 'check_result': check_result}
        inconsistent_submissions.append(entry)

print('\n[3] Finished')
print("Total {} Trials => {} Success, {} Submit fails, {} Inconsistent results"\
        .format(total, success_cnt, submit_failed_cnt, inconsistent_cnt))

def save(submissions, filename):
    with open(filename, "w", encoding = 'utf-8') as f:
        json.dump(submissions, f, ensure_ascii = False, indent = 4)

save(success_submissions, "success.json")
save(submit_failed_submissions, "failed.json")
save(inconsistent_submissions, "inconsistent.json")
print("Submission pairs saved to: 'success.json' / 'failed.json' / 'inconsistent.json'")

    
    
    