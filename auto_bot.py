import requests
import json
import random

BASE_URL = 'http://127.0.0.1:8000/'

with open('snavi/config.json', 'r') as f:
    cnfg = json.load(f)

NUMBER_OF_USERS = int(cnfg['number_of_users'])
MAX_POSTS_PER_USER = int(cnfg['max_posts_per_user'])
MAX_LIKES_PER_USER = int(cnfg['max_likes_per_user'])
tmp_auth_list = []


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
        print(r)
        return r

    def login_user(passw, username, email='ex@ex.com'):

        r = session.post(data={'password': passw, 'username': username, 'email': email}, url=LOGIN_URL).json()
        return r['token']

    def logout_user(to_ken):

        csrf_token = session.get(url=LOGOUT_URL, data={'token': to_ken}).request.headers['Cookie'].split('=')[1].split(';')[0]
        r = session.post(url=LOGOUT_URL, data={'csrfmiddlewaretoken': csrf_token})
        print(r.json())
        return r.json()

    def create_rand_num_of_posts(to_ken):

        posts_amount = random.randint(1, MAX_POSTS_PER_USER)
        user = session.get(url=USERS_URL, data={'token': to_ken}).json()['results'][0]['url']
        csrf_token = session.get(url=POSTS_URL, data={'token': to_ken}).request.headers['Cookie'].split('=')[1].split(';')[0]
        print(f'posts_amount -----------------------------------:  {posts_amount}')

        for post in range(posts_amount):

            title = 'post' + '_' + str(post) + 'user' + user
            content = 'content' + '_' + str(post)

            r = session.post(url=POSTS_URL, data={
                'csrfmiddlewaretoken': csrf_token,
                'user': user,
                'title': title,
                'content': content
            })
            print(r.json())
            print(f'created {posts_amount} posts by user {user}')
        return f'created {posts_amount} posts by user {user}'

    def like_posts_randomly(to_ken):
        posts_list = session.get(url=POSTS_URL, data={'token': to_ken}).json()['results']
        for _ in range(MAX_LIKES_PER_USER):
            rand_post = posts_list[random.randint(0, len(posts_list)-1)]
            url = rand_post['url']
            posts_likes_amount = rand_post['like']
            print(posts_likes_amount)
            title = rand_post['title']
            content = rand_post['content']
            user = rand_post['user']
            csrf_token = session.get(url=url, data={'token': to_ken}).request.headers['Cookie'].split('=')[1].split(';')[0]
            posts_likes_amount += 1

            session.headers.update({'X-CSRFToken': csrf_token})

            r = session.put(
                url=url,
                data={
                    'user': user,
                    'content': content,
                    'title': title,
                    'like': posts_likes_amount,
                    }
            )
            print(r)
            print(r.json())

        return f'liked {MAX_LIKES_PER_USER} posts!'

    for user_number in range(NUMBER_OF_USERS):

        pass_word = 100 + user_number
        user_name = 'user' + '_' + str(user_number)
        tmp_auth_list.append({user_name: pass_word})
        sign_up_user(pass_word, user_name)

        token = login_user(pass_word, user_name)

        create_rand_num_of_posts(token)

        logout_user(token)

    for user_number in range(NUMBER_OF_USERS):

        print(f'tmp_auth_list ===========   {tmp_auth_list}')
        u_ser = list(tmp_auth_list[user_number].keys())[0]
        p_assword = tmp_auth_list[user_number][u_ser]
        token = login_user(p_assword, u_ser)

        like_posts_randomly(token)

        logout_user(token)

    # print(sign_up_user(123, 'w3'))

    # print(login_user('123', 'w11', 'lens2kymiwa@ya.ru'))
    # print(login_user('123', 'w3', 'ex@ex.com'))

    # token = login_user('123', 'w11', 'lens2kymiwa@ya.ru')
    # print(create_rand_num_of_posts(token))

    # token = login_user('123', 'w11', 'lens2kymiwa@ya.ru')
    # print(logout_user(token))

    # token = login_user('123', 'w11', 'lens2kymiwa@ya.ru')
    # like_posts_randomly(token)


if __name__ == '__main__':
    main()
