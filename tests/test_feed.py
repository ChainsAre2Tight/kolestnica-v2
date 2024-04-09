import unittest
import requests

default_href: str = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXaoP2F5I4FX1KWv3n_IRajRWfrKli9zESuXTqRgLoa89vsPBTPwEZEVyKstJ_GbXRUQg&usqp=CAU'
corrupted_token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIxMjM0NTY3ODkwIiwiZXhwIjoxMDB9.CAwkokoCzrjvhyMRDaciZO0YSnMys20H4RpF8iGwT3h'
expired_token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIxMjM0NTY3ODkwIiwiZXhwIjoxMDB9.CAwkokoCzrjvhyMRDaciZO0YSnMys20H4RpF8iGwT3Y'
valid_token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIxMjM0NTY3ODkwIiwiZXhwIjoxMDAwMDAwMDAwMH0._XGzlL7svHZnZPM8mg4ZZRZFcPGhDlEEcgUYXSiAviU'
token_pointing_to_user_1: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiJ2M3J5LXVuMXEtdWUxZC0xMTExIiwiZXhwIjoxMDAwMDAwMDAwMH0.jIteq0z276zQAZpofkCIxiUuX8AeezZoeLF3Cq3UZPU'
token_pointing_to_nonexistant_user: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIxLWRvLW5vdC1leGlzdCIsImV4cCI6MTAwMDAwMDAwMDB9.e_KDA2yrnnaGArunSp8WNDmuvWY07IGnWWZ83gp1GjE'
token_pointing_to_user_3: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiJ2M3J5LXVuMXEtdWUxZC0zMzMzIiwiZXhwIjoxMDAwMDAwMDAwMH0.emJ2u5x4BHcmGE71r2gw6IdDcHb7iLk1LriAMrO-Qe8'

class TestAvaliability(unittest.TestCase):

    def test_ping(self):
        r = requests.get('http://127.0.0.1:5010/api/data').status_code
        self.assertEqual(r, 400)
    
    def test_bad_token(self):
        global corrupted_token
        r = requests.get(
            url='http://127.0.0.1:5010/api/data',
            headers={'Authorization': corrupted_token}
        ).status_code
        self.assertEqual(r, 403)
    
    def test_expired_token(self):
        global expired_token
        r = requests.get(
            url='http://127.0.0.1:5010/api/data',
            headers={'Authorization': expired_token}
        ).status_code
        self.assertEqual(r, 401)
    
    def test_good_token(self):
        global valid_token
        r = requests.get(
            url='http://127.0.0.1:5010/api/data',
            headers={'Authorization': valid_token}
        ).status_code
        self.assertEqual(r, 200)

class TestChats(unittest.TestCase):
    
    def test_request_chats_for_existing_user(self):
        global token_pointing_to_user_1
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats',
            headers={'Authorization': token_pointing_to_user_1}
        )
    
        self.assertEqual(
            (r.json(), r.status_code),
            ([{'id': 1, 'image_href': None, 'message_ids': [1, 2], 'name': 'test chat #1', 'user_ids': [1, 2]}], 200)
        )
    
    def test_request_chats_for_null_user(self):
        global token_pointing_to_nonexistant_user
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats',
            headers={'Authorization': token_pointing_to_nonexistant_user}
        )
    
        self.assertEqual(
            (r.status_code),
            (401)
        )

class TestUsers(unittest.TestCase):

    def test_request_chats_for_user_in_chat(self):
        global token_pointing_to_user_1
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/users',
            headers={'Authorization': token_pointing_to_user_1}
        )
    
        self.assertEqual(
            (r.json(), r.status_code),
            ([
                {'id': 1, 'username': 'test_1', 'alias': 'test user #1', 'image_href': default_href},
                {'id': 2, 'username': 'test_2', 'alias': 'test user #2', 'image_href': default_href}
            ], 200)
        )
    
    def test_request_chats_for_user_not_in_chat(self):
        global token_pointing_to_user_3
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/users',
            headers={'Authorization': token_pointing_to_user_3}
        )
    
        self.assertEqual(
            (r.json(), r.status_code),
            ([], 200)
        )

class TestMessages(unittest.TestCase):

    def test_request_messages_for_user_in_chat(self):
        global token_pointing_to_user_1
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/1/messages',
            headers={'Authorization': token_pointing_to_user_1}
        )
    
        self.assertEqual(
            (r.json(), r.status_code),
            ([
                {'author_id': 1,'body': 'hello world!','chat_id': 1,'id': 1,'timestamp': 1000000},
                {'author_id': 2,'body': 'go away loser','chat_id': 1,'id': 2,'timestamp': 10000000}
            ], 200)
        )
    
    def test_request_messages_for_user_not_in_chat(self):
        global token_pointing_to_user_3
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/1/messages',
            headers={'Authorization': token_pointing_to_user_3}
        )
    
        self.assertEqual(
            (r.json(), r.status_code),
            ([], 200)
        )

if __name__ == "__main__":
    unittest.main()