import unittest
import requests
import sys
from preparesuit import suite
from globals import *

if __name__ == "__main__":
    sys.path.append('../application/database')
    from db_actuator import prepare_test_environment


class TestAvaliability(unittest.TestCase):

    def test_ping(self):
        r = requests.get('http://127.0.0.1:5010/api/data').status_code
        self.assertEqual(r, 401)
    
    def test_bad_token(self):
        global corrupted_token
        r = requests.get(
            url='http://127.0.0.1:5010/api/data',
            headers={'Authorization': corrupted_token}
        ).status_code
        self.assertEqual(r, 401)
    
    def test_expired_token(self):
        global expired_token
        r = requests.get(
            url='http://127.0.0.1:5010/api/data',
            headers={'Authorization': expired_token}
        ).status_code
        self.assertEqual(r, 403)
    
    def test_good_token(self):
        global token_pointing_to_nonexistant_user
        r = requests.get(
            url='http://127.0.0.1:5010/api/data',
            headers={'Authorization': token_pointing_to_nonexistant_user}
        ).status_code
        self.assertEqual(r, 200)

class TestChats(unittest.TestCase):
    
    def test_request_chats_for_existing_user(self):
        global token_pointing_to_user_1
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats',
            headers={'Authorization': token_pointing_to_user_1}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            [{'id': 1, 'image_href': None, 'message_ids': [1, 2], 'name': 'test chat #1 static', 'user_ids': [1, 2]}]
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

    def test_request_chats_for_user_in_chat_1(self):
        global token_pointing_to_user_1
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/users',
            headers={'Authorization': token_pointing_to_user_1}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            [
                {'id': 1, 'username': 'test_1', 'alias': 'test user #1', 'image_href': default_href},
                {'id': 2, 'username': 'test_2', 'alias': 'test user #2', 'image_href': default_href}
            ]
        )
    
    def test_request_chats_for_user_in_chat_2(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/users',
            headers={'Authorization': token_pointing_to_user_4}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            [
                {'id': 4, 'username': 'test_4', 'alias': 'test user #4', 'image_href': default_href},
            ]
        )
    
    def test_request_chats_for_user_not_in_chat(self):
        global token_pointing_to_user_3
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/users',
            headers={'Authorization': token_pointing_to_user_3}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), [])

class TestStaticMessages(unittest.TestCase):

    def test_request_messages_for_user_in_chat(self):
        global token_pointing_to_user_1
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/1/messages',
            headers={'Authorization': token_pointing_to_user_1}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            [
                {'author_id': 1,'body': 'hello world!','chat_id': 1,'id': 1,'timestamp': 1000000},
                {'author_id': 2,'body': 'go away loser','chat_id': 1,'id': 2,'timestamp': 10000000}
            ],
        )
    
    def test_request_messages_for_user_not_in_chat(self):
        global token_pointing_to_user_3
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/1/messages',
            headers={'Authorization': token_pointing_to_user_3}
        )
    
        self.assertEqual(
            (r.status_code),
            (404)
        )

class TestDynamicMessage(unittest.TestCase):

    def test_chat_is_empty(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/2/messages',
            headers={'Authorization': token_pointing_to_user_4}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            [{
                'author_id': 4,
                'body': 'static message',
                'chat_id': 2,
                'id': 3,
                'timestamp': 123321123
            }]
        )
    
    def test_send_valid_message(self):
        global token_pointing_to_user_4
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/2/messages',
            headers={'Authorization': token_pointing_to_user_4},
            json={
                'body': 'i sent this message ;)',
                'timestamp': 1234567890,
            }
        )

        self.assertEqual(r.status_code, 201)
        self.assertEqual(
            r.json(),
            {
                'msg_id': 4,
            }
        )
    
    def test_get_sent_message_by_user_in_chat(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/2/messages',
            headers={'Authorization': token_pointing_to_user_4}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            [{
                'author_id': 4,
                'body': 'static message',
                'chat_id': 2,
                'id': 3,
                'timestamp': 123321123
            }, {
                'author_id': 4,
                'body': 'i sent this message ;)',
                'chat_id': 2,
                'id': 4,
                'timestamp': 1234567890
            }]
        )
    
    def test_get_sent_message_by_user_not_in_chat(self):
        global token_pointing_to_user_3
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/2/messages',
            headers={'Authorization': token_pointing_to_user_3}
        )
    
        self.assertEqual(
            (r.status_code),
            (404)
        )

    def test_delete_non_existing_message_by_user_in_chat(self):
        global token_pointing_to_user_4
        r = requests.delete(
            url='http://127.0.0.1:5010/api/data/chats/2/messages/321132',
            headers={'Authorization': token_pointing_to_user_4}
        )
    
        self.assertEqual(
            (r.status_code),
            (404)
        )
    
    def test_delete_existing_message_by_user_not_in_chat(self):
        global token_pointing_to_user_3
        r = requests.delete(
            url='http://127.0.0.1:5010/api/data/chats/2/messages/4',
            headers={'Authorization': token_pointing_to_user_3}
        )
    
        self.assertEqual(
            (r.status_code),
            (404)
        )
    
    def test_delete_existing_message_by_user_in_chat(self):
        global token_pointing_to_user_1
        r = requests.delete(
            url='http://127.0.0.1:5010/api/data/chats/1/messages/2',
            headers={'Authorization': token_pointing_to_user_1}
        )
    
        self.assertEqual(
            (r.status_code),
            (403)
        )
    
    def test_delete_existing_message_by_author(self):
        global token_pointing_to_user_4
        r = requests.delete(
            url='http://127.0.0.1:5010/api/data/chats/2/messages/4',
            headers={'Authorization': token_pointing_to_user_4}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {'msg_id': 4}
        )

class TestChatActions(unittest.TestCase):

    def test_create_chat(self):
        global token_pointing_to_user_4
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats',
            headers={'Authorization': token_pointing_to_user_4},
            json={'chat_name': 'dynamically created chat'}
        )

        self.assertEqual(r.status_code, 201)
        self.assertEqual(
            r.json()['chat_id'],
            3
        )
    
    def test_verify_chat_creation(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats',
            headers={'Authorization': token_pointing_to_user_4}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            [
                {'id': 2, 'image_href': None, 'message_ids': [3], 'name': 'test chat #2 dynamic', 'user_ids': [4]},
                {'id': 3, 'image_href': None, 'message_ids': [], 'name': 'dynamically created chat', 'user_ids': [4]}
            ]
        )
    
    def test_verify_user_list_before(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/3/users',
            headers={'Authorization': token_pointing_to_user_4}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            [
                {'id': 4, 'username': 'test_4', 'alias': 'test user #4', 'image_href': default_href}
            ]
        )
    
    def test_add_user_to_chat_user_has_no_access_to(self):
        global token_pointing_to_user_3
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/3/users',
            headers={'Authorization': token_pointing_to_user_3},
            json={'username': 'some_user'}
        )

        self.assertEqual(r.status_code, 404)
        self.assertEqual(
            r.json()['Error'],
            'Cannot access requested data'
        )

    def test_add_user_that_doesnt_exist(self):
        global token_pointing_to_user_4
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/3/users',
            headers={'Authorization': token_pointing_to_user_4},
            json={'username': 'some_user'}
        )

        self.assertEqual(r.status_code, 404)
        self.assertEqual(
            r.json()['Error'],
            'Requested user does not exist'
        )
    
    def test_add_user_that_is_already_in_chat(self):
        global token_pointing_to_user_1
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/1/users',
            headers={'Authorization': token_pointing_to_user_1},
            json={'username': 'test_2'}
        )

        self.assertEqual(r.status_code, 406)
        self.assertEqual(
            r.json()['Error'],
            'Requirement is already fullfilled'
        )
    
    def test_add_yourself(self):
        global token_pointing_to_user_1
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/1/users',
            headers={'Authorization': token_pointing_to_user_1},
            json={'username': 'test_1'}
        )

        self.assertEqual(r.status_code, 406)
        self.assertEqual(
            r.json()['Error'],
            'Requirement is already fullfilled'
        )
    
    def test_add_valid_user(self):
        global token_pointing_to_user_4
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/3/users',
            headers={'Authorization': token_pointing_to_user_4},
            json={'username': 'test_1'}
        )

        self.assertEqual(r.status_code, 201)
        self.assertEqual(
            r.json(),
            {'id': 1, 'username': 'test_1', 'alias': 'test user #1', 'image_href': default_href}
        )

    def test_verify_user_list_after(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/3/users',
            headers={'Authorization': token_pointing_to_user_4}
        )

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            {i['id'] for i in r.json()},
            {1, 4}
        )

if __name__ == "__main__":
    # prepare testSuit
    runner = unittest.TextTestRunner()

    # reset database
    dbname = 'koleso2_test'
    prepare_test_environment(dbname)

    # run tests
    runner.run(suite(__name__))
