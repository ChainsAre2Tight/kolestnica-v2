


import time
from datetime import datetime
from unittest import TestCase, mock, main as u_main

from shared import UserData, SessionData, ChatData, MessageData
import actions


class TestChatCreation(TestCase):

    def test_chat_creation(self):
        user = UserData(
            'testchat1',
            'testpwd',
            'test_chat_user_1'
        )
        json, code = actions.register_user(user)
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
                        'encryption_key': mock.ANY
                    }
                }
            }
        )
        self.assertEqual(code, 200)
    
    def test_get_chat_members(self):
        user = UserData(
            'testchat3',
            'testpwd',
            'test_chat_user_3'
        )
        json, code = actions.register_user(user)
        user.id = json['data']['user']['id']
        self.assertEqual(code, 201)
        session = SessionData('testchat3')
        json, code, _ = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        session.access_token = json['data']['tokens']['access']['value']
        chat = ChatData('test chat 3')
        json, code = actions.create_chat(chat, session)
        self.assertEqual(code, 201)
        chat.id = json['data']['chat']['id']
        json, code = actions.get_chat_members(chat, session)
        self.assertDictEqual(
            json,
            {
                'Status': 'OK',
                'data': {
                    'chat_id': chat.id,
                    'members': [
                        {
                            'id': user.id,
                            'username': user.username,
                            'alias': user.username  # can be replaced
                        }
                    ]
                }
            }
        )
        self.assertEqual(code, 200)

    def test_add_user_to_chat(self):
        user1 = UserData(
            'testchat4',
            'testpwd',
            'test_chat_user_4'
        )
        json, code = actions.register_user(user1)
        user1.id = json['data']['user']['id']
        self.assertEqual(code, 201)
        session1 = SessionData('testchat4')
        json, code, _ = actions.login_user(user=user1, session=session1)
        self.assertEqual(code, 201)
        session1.access_token = json['data']['tokens']['access']['value']
        chat = ChatData('test chat 4')
        json, code = actions.create_chat(chat, session1)
        self.assertEqual(code, 201)
        chat.id = json['data']['chat']['id']
        
        user2 = UserData(
            'testchat5',
            'testpwd',
            'test_chat_user_5'
        )
        json, code = actions.register_user(user2)
        user2.id = json['data']['user']['id']
        self.assertEqual(code, 201)
        session2 = SessionData('testchat5')
        json, code, _ = actions.login_user(user=user2, session=session2)
        self.assertEqual(code, 201)
        session2.access_token = json['data']['tokens']['access']['value']
        json, code = actions.add_user_to_chat(chat_id=chat.id, target_id=user2.id, session=session1)
        self.assertEqual(
            json,
            {
                'Status': 'Added',
                'data': {
                    'chat_id': chat.id,
                    'members': mock.ANY
                }
            }
        )
        self.assertEqual(
            set(json['data']['members']),
            {user1.id, user2.id}
        )
        self.assertEqual(code, 201)

class TestMessages(TestCase):

    def test_get_messages_empty(self):
        user = UserData(
            'testmsg6',
            'testmsgpwd',
            'test_msg_user_6'
        )
        json, code = actions.register_user(user)
        user.id = json['data']['user']['id']
        self.assertEqual(code, 201)
        session = SessionData('testmsg6')
        json, code, _ = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        session.access_token = json['data']['tokens']['access']['value']
        chat = ChatData('test chat 6')
        json, code = actions.create_chat(chat, session)
        self.assertEqual(code, 201)
        chat.id = json['data']['chat']['id']
        json, code = actions.get_chat_messages(chat, session)
        self.assertEqual(
            json,
            {
                'Status': 'OK',
                'data': {
                    'chat_id': chat.id,
                    'messages': []
                }
            }
        )
        self.assertEqual(code, 200)

    def test_send_message(self):
        user = UserData(
            'testmsg_7',
            'testmsgpwd',
            'test_msg_user_7'
        )
        json, code = actions.register_user(user)
        user.id = json['data']['user']['id']
        self.assertEqual(code, 201)
        session = SessionData('testmsg_7')
        json, code, _ = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        session.access_token = json['data']['tokens']['access']['value']
        chat = ChatData('test chat 7')
        json, code = actions.create_chat(chat, session)
        self.assertEqual(code, 201)
        chat.id = json['data']['chat']['id']
        message = MessageData(
            'test message 1',
            timestamp=int(datetime.now().timestamp())
        )
        json, code = actions.send_message(chat, message, session)
        self.assertEqual(
            json,
            {
                'Status': 'Created',
                'data': {
                    'chat_id': chat.id,
                    'message_id': mock.ANY
                }
            }
        )
        self.assertEqual(code, 201)
        message.id = json['data']['message_id']
        json, code = actions.get_chat_messages(chat, session)
        self.assertEqual(
            json,
            {
                'Status': 'OK',
                'data': {
                    'chat_id': chat.id,
                    'messages': [{
                        'author_id': user.id,
                        'body': message.body,
                        'id': message.id,
                        'timestamp': message.timestamp
                    }]
                }
            }
        )
        self.assertEqual(code, 200)

    def test_send_messages_two_sides(self):
        user1 = UserData(
            'testchat_8',
            'testpwd',
            'test_chat_user_8'
        )
        json, code = actions.register_user(user1)
        user1.id = json['data']['user']['id']
        self.assertEqual(code, 201)
        session1 = SessionData('testchat_8')
        json, code, _ = actions.login_user(user=user1, session=session1)
        self.assertEqual(code, 201)
        session1.access_token = json['data']['tokens']['access']['value']
        chat = ChatData('test chat 4')
        json, code = actions.create_chat(chat, session1)
        self.assertEqual(code, 201)
        chat.id = json['data']['chat']['id']
        
        user2 = UserData(
            'testchat_9',
            'testpwd',
            'test_chat_user_9'
        )
        json, code = actions.register_user(user2)
        user2.id = json['data']['user']['id']
        self.assertEqual(code, 201)
        session2 = SessionData('testchat_9')
        json, code, _ = actions.login_user(user=user2, session=session2)
        self.assertEqual(code, 201)
        session2.access_token = json['data']['tokens']['access']['value']
        json, code = actions.add_user_to_chat(chat_id=chat.id, target_id=user2.id, session=session1)
        self.assertEqual(code, 201)
        
        message_1 = MessageData(
            body='sent from user 1',
            timestamp=int(datetime.now().timestamp())
        )
        message_1.author_id = user1.id
        message_2 = MessageData(
            body='sent from user 2',
            timestamp=int(datetime.now().timestamp())
        )
        message_2.author_id = user2.id
        
        json, code = actions.send_message(chat, message_1, session1)
        self.assertEqual(code, 201)
        message_1.id = json['data']['message_id']
        json, code = actions.send_message(chat, message_2, session2)
        self.assertEqual(code, 201)
        message_2.id = json['data']['message_id']

        json, code = actions.get_chat_messages(chat, session1)
        self.assertDictEqual(
            json,
            {
                'Status': 'OK',
                'data': {
                    'chat_id': chat.id,
                    'messages': mock.ANY
                }
            }
        )
        self.assertEqual(
            json['data']['messages'],
            [{
                'author_id': user1.id,
                'body': message_1.body,
                'id': message_1.id,
                'timestamp': message_1.timestamp
            },
            {
                'author_id': user2.id,
                'body': message_2.body,
                'id': message_2.id,
                'timestamp': message_2.timestamp
            }]
        )
        self.assertEqual(code, 200)
        
        json, code = actions.get_chat_messages(chat, session2)
        self.assertDictEqual(
            json,
            {
                'Status': 'OK',
                'data': {
                    'chat_id': chat.id,
                    'messages': mock.ANY
                }
            }
        )
        self.assertEqual(
            json['data']['messages'],
            [{
                'author_id': user1.id,
                'body': message_1.body,
                'id': message_1.id,
                'timestamp': message_1.timestamp
            },
            {
                'author_id': user2.id,
                'body': message_2.body,
                'id': message_2.id,
                'timestamp': message_2.timestamp
            }]
        )
        self.assertEqual(code, 200)

if __name__ == "__main__":
    u_main()
