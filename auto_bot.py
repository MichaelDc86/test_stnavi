import requests
import json
import random

BASE_URL = 'http://127.0.0.1:8000/'

with open('snavi/config.json', 'r') as f:
    cnfg = json.load(f)

NUMBER_OF_USERS = cnfg['number_of_users']
MAX_POSTS_PER_USER = cnfg['max_posts_per_user']
MAX_LIKES_PER_USER = cnfg['max_likes_per_user']


def main():

    session = requests.session()

    menu = session.get(BASE_URL).json()

    LOGIN_URL = menu['login']
    LOGOUT_URL = menu['logout']
    SIGNUP_URL = menu['register']
    POSTS_URL = menu['posts']
    USERS_URL = menu['users']

    def sign_up_user(passw, username, email='ex@ex.com'):
        r = session.post(data={'password': passw, 'username': username, 'email': email}, url=SIGNUP_URL).json()
        password = r['password']
        username = r['username']
        return username, password

    def login_user(passw, username, email='ex@ex.com'):
        r = session.post(data={'password': passw, 'username': username, 'email': email}, url=LOGIN_URL).json()
        return r['token']

    def logout_user():
        pass

    def create_rand_num_of_posts():
        pass

    def like_posts_randomly():
        pass

    # for user_number in range(NUMBER_OF_USERS):
    #     sign_up_user('user'+str(user_number), 'user'+str(user_number))
    #
    #     login_user(passw_tmp, username_tmp)
    #
    #     create_rand_num_of_posts()
    #
    #     logout_user()

    like_posts_randomly()

    # print(login_user('123', 'w11', 'lens2kymiwa@ya.ru'))

    # print(sign_up_user(123, 'wer3'))

    # print(login_user('123', 'w11', 'lens2kymiwa@ya.ru'))

    r = session.get(url=USERS_URL, data={'token': login_user('123', 'w11', 'lens2kymiwa@ya.ru')}).json()
    print(r)


    # print(menu.json())
    # print(menu.json()['login'])
    return menu


main()
