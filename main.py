from login import Login
from getpass import getpass

loginObject = Login()
user_id = input("Input id: ")
password = getpass("Input password: ")
login_cookie = loginObject.login(user_id, password)