

import time
from unittest import TestCase, mock, main as u_main

from shared import UserData, SessionData
import actions


class TestRegistartion(TestCase):

    def test_registration(self):
        user = UserData(
            'testregistration1',
            'testpwd',
            'test_registration_user_1'
        )
        json, code = actions.register_user(user)
        self.assertEqual(code, 201)
        self.assertDictEqual(
            json,
            {
                'Status': 'Created',
                'data': {'user': {
                    'id': mock.ANY,
                    'username': user.username,
                    'alias': user.username,
                    'image_href': mock.ANY,
                }}
            }
        )

    def test_login(self):
        user = UserData(
            'testregistration2',
            'testpwd2',
            'test_registration_user_2'
        )
        _, code = actions.register_user(user)
        self.assertEqual(code, 201)
        session = SessionData('test_2')
        json, code, refresh = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        self.assertDictEqual(
            json,
            {
                'Status': 'Logged in',
                'data': {
                    'User': {
                        'id': mock.ANY,
                        'username': user.username,
                        'alias': user.username,
                        'image_href': mock.ANY,
                    },
                    'tokens': {
                        'access': {
                            'value': mock.ANY,
                            'expiry': mock.ANY
                        }
                    }
                }
            }
        )
        self.assertEqual(refresh, mock.ANY)

    def test_refresh(self):
        user = UserData(
            'testregistration3',
            'testpwd3',
            'test_registration_user_3'
        )
        _, code = actions.register_user(user)
        self.assertEqual(code, 201)
        session = SessionData('test_3')
        _, code, refresh = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        time.sleep(2)
        # session.access_token = json['data']['tokens']['access']['value']
        json, code, new_refresh = actions.refresh_tokens(refresh_token=refresh)
        self.assertEqual(code, 200)
        self.assertDictEqual(
            json,
            {
                'Status': 'Refreshed tokens',
                'data': {
                    'tokens': {
                        'access': {
                            'value': mock.ANY,
                            'expiry': mock.ANY
                        }
                    }
                }
            }
        )
        self.assertNotEqual(new_refresh, refresh)

    def test_read_current_user(self):
        user = UserData(
            'testregistration4',
            'testpwd4',
            'test_registration_user_4'
        )
        _, code = actions.register_user(user)
        self.assertEqual(code, 201)
        session = SessionData('test_4')
        json, code, _ = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        session.access_token = json['data']['tokens']['access']['value']
        json, code = actions.get_current_user(access=session.access_token)
        self.assertEqual(code, 200)
        self.assertDictEqual(
            json,
            {
                'Status': 'OK',
                'data': {
                    'User': {
                        'id': mock.ANY,
                        'username': user.username,
                        'alias': user.username,
                        'image_href': mock.ANY,
                    }
                }
            }
        )

    def test_relogin_user(self):
        user = UserData(
            'testregistration5',
            'testpwd5',
            'test_registration_user_5'
        )
        _, code = actions.register_user(user)
        self.assertEqual(code, 201)
        session = SessionData('test_2')
        json, code, _ = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        session.access_token = json['data']['tokens']['access']['value']
        json, code = actions.get_current_user(access=session.access_token)
        self.assertEqual(code, 200)
        self.assertDictEqual(
            json,
            {
                'Status': 'OK',
                'data': {
                    'User': {
                        'id': mock.ANY,
                        'username': user.username,
                        'alias': user.username,
                        'image_href': mock.ANY,
                    }
                }
            }
        )

    def test_logout(self):
        user = UserData(
            'testregistration6',
            'testpwd6',
            'test_registration_user_6'
        )
        _, code = actions.register_user(user)
        self.assertEqual(code, 201)
        session = SessionData('test_6')
        json, code, _ = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        session.access_token = json['data']['tokens']['access']['value']
        json, code = actions.get_current_user(access=session.access_token)
        self.assertEqual(code, 200)
        self.assertDictEqual(
            json,
            {
                'Status': 'OK',
                'data': {
                    'User': {
                        'id': mock.ANY,
                        'username': user.username,
                        'alias': user.username,
                        'image_href': mock.ANY,
                    }
                }
            }
        )
        json, code = actions.logout(access=session.access_token)
        self.assertEqual(code, 200)
        self.assertDictEqual(
            json,
            {
                'Status': 'Deleted',
                'Details': 'Session successfully terminated'
            }
        )
        json, code = actions.get_current_user(access=session.access_token)
        self.assertEqual(code, 401)

    def test_double_refresh(self):
        user = UserData(
            'testregistration7',
            'testpwd7',
            'test_registration_user_7'
        )
        _, code = actions.register_user(user)
        self.assertEqual(code, 201)
        session = SessionData('test_7')
        _, code, refresh = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        time.sleep(1)
        _, code, _ = actions.refresh_tokens(refresh_token=refresh)
        self.assertEqual(code, 200)
        time.sleep(1)
        _, code, _ = actions.refresh_tokens(refresh_token=refresh)
        self.assertEqual(code, 401)

    def test_duplicate_login(self):
        user = UserData(
            'testregistration_8',
            'testpwd',
            'test_registration_user_8'
        )
        _, code = actions.register_user(user)
        self.assertEqual(code, 201)
        user_2 = UserData(
            'testregistration_8',
            'testpwd',
            'test_registration_user_lox'
        )
        json, code = actions.register_user(user_2)
        self.assertEqual(code, 409)
        self.assertDictEqual(
            json,
            {
                'Status': 'Error',
                'Error': 'An account assosiated with this login already exists',
                'Details': mock.ANY
            }
        )

    def test_duplicate_username(self):
        user = UserData(
            'testregistration_9',
            'testpwd',
            'test_registration_user_9'
        )
        _, code = actions.register_user(user)
        self.assertEqual(code, 201)
        user_2 = UserData(
            'testregistration_lox',
            'testpwd',
            'test_registration_user_9'
        )
        json, code = actions.register_user(user_2)
        self.assertEqual(code, 409)
        self.assertDictEqual(
            json,
            {
                'Status': 'Error',
                'Error': 'This username was already taken by another user',
                'Details': mock.ANY
            }
        )

    def test_bad_access_token(self):
        user = UserData(
            'testregistration10',
            'testpwd4',
            'test_registration_user_10'
        )
        _, code = actions.register_user(user)
        self.assertEqual(code, 201)
        session = SessionData('test_10')
        json, code, _ = actions.login_user(user=user, session=session)
        self.assertEqual(code, 201)
        session.access_token = json['data']['tokens']['access']['value'][:-1]
        json, code = actions.get_current_user(access=session.access_token)
        self.assertEqual(code, 401)
        self.assertDictEqual(
            json,
            {
                'Status': 'Error',
                'details': 'Access token is missing or is invalid'
            }
        )

if __name__ == "__main__":
    u_main()
