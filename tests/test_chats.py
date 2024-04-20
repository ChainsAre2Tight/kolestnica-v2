


import time
from unittest import TestCase, mock, main as u_main

from shared import UserData, SessionData, ChatData
import actions


class TestChatCreation(TestCase):
    
    def test_chat_creation(self):
        user = UserData(
            'testchat1',
            'testpwd',
            'test_chat_user_1'
        )
        json, code = actions.register_user(user)
        user_id: int = json['data']['user']['id']
        self.assertEqual(code, 201)
        session = SessionData('testchat1')
        json, code, _ = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        session.access_token = json['data']['tokens']['access']['value']
        chat = ChatData('test chat 1')
        json, code = actions.create_chat(chat, session)
        self.assertDictEqual(
            json,
            {
                'Status': 'Created',
                'data': {
                    'chat': {
                        'id': mock.ANY,
                        'name': chat.name,
                        'image_href': mock.ANY,
                        'user_ids': [user_id],
                        'message_ids': [],
                        'encryption_key': mock.ANY
                    }
                }
            }
        )
        self.assertEqual(code, 201)
    
    def test_get_chat_data(self):
        user = UserData(
            'testchat2',
            'testpwd',
            'test_chat_user_2'
        )
        json, code = actions.register_user(user)
        user.id = json['data']['user']['id']
        self.assertEqual(code, 201)
        session = SessionData('testchat2')
        json, code, _ = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        session.access_token = json['data']['tokens']['access']['value']
        chat = ChatData('test chat 2')
        json, code = actions.create_chat(chat, session)
        self.assertEqual(code, 201)
        chat.id = json['data']['chat']['id']
        
        json, code = actions.get_chat_data(chat, session)
        
        self.assertDictEqual(
            json,
            {
                'Status': 'OK',
                'data': {
                    'chat': {
                        'id': chat.id,
                        'name': chat.name,
                        'image_href': mock.ANY,
                        'user_ids': [user.id],
                        'message_ids': [],
                        'encryption_key': mock.ANY
                    }
                }
            }
        )
    
    # def test_add_user_to_chat(self):
    #     user1 = UserData(
    #         'testchat1',
    #         'testpwd',
    #         'test_chat_user_1'
    #     )
    #     json, code = actions.register_user(user1)
    #     user1_id: int = json['data']['user']['id']
    #     self.assertEqual(code, 201)
    #     session1 = SessionData('testchat1')
    #     json, code, _ = actions.login_user(user=user1, session=session1)
    #     self.assertEqual(code, 201)
    #     session1.access_token = json['data']['tokens']['access']['value']
    #     chat = ChatData('test chat 1')
    #     json, code = actions.create_chat(chat, session1)
    #     self.assertEqual(code, 201)
    #     chat.id = json['data']['chat']['id']
        
    #     user2 = UserData(
    #         'testchat1',
    #         'testpwd',
    #         'test_chat_user_1'
    #     )
    #     json, code = actions.register_user(user2)
    #     user2_id: int = json['data']['user']['id']
    #     self.assertEqual(code, 201)
    #     session2 = SessionData('testchat1')
    #     json, code, _ = actions.login_user(user=user2, session=session2)
    #     self.assertEqual(code, 201)
    #     session2.access_token = json['data']['tokens']['access']['value']
        
        
        
        

if __name__ == "__main__":
    u_main()
        