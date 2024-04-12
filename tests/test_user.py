import unittest
import sys
from globals import *
from preparesuit import suite
import requests

token_new: str = ''
token_new_2: str = ''
token_test_1: str = ''

if __name__ == '__main__':

    sys.path.append('../application/database')
    from db_actuator import prepare_test_environment


class TestAvaliability(unittest.TestCase):

    def test_ping(self):
        r = requests.get('http://127.0.0.1:5020/api/auth').status_code
        self.assertEqual(r, 401)
    
    def test_bad_token(self):
        global corrupted_token
        r = requests.get(
            url='http://127.0.0.1:5020/api/auth',
            headers={'Authorization': corrupted_token}
        ).status_code
        self.assertEqual(r, 401)
    
    def test_expired_token(self):
        global expired_token
        r = requests.get(
            url='http://127.0.0.1:5020/api/auth',
            headers={'Authorization': expired_token}
        ).status_code
        self.assertEqual(r, 403)
    
    def test_good_token(self):
        global token_pointing_to_nonexistant_user
        r = requests.get(
            url='http://127.0.0.1:5020/api/auth',
            headers={'Authorization': token_pointing_to_nonexistant_user}
        ).status_code
        self.assertEqual(r, 200)

class TestUserCreation(unittest.TestCase):

    def test_missing_data(self):
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/register',
            json={'some': 'data', 'is': 'missing'}
        ).status_code
        self.assertEqual(r, 400)

    def test_duplicate_login(self):
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/register',
            json={
                'username': 'some_unique_username',
                'login': 'not-so-very-unique-login',
                'pwdh': '12345678901234567890123456789012'
            }
        ).status_code
        self.assertEqual(r, 409)

    def test_duplicate_username(self):
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/register',
            json={
                'username': 'test_1',
                'login': 'very-unique-login',
                'pwdh': '12345678901234567890123456789012'
            }
        ).status_code
        self.assertEqual(r, 406)

    def test_valid_data(self):
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/register',
            json={
                'username': 'very-unique-username',
                'login': 'very-unique-login',
                'pwdh': '12345678901234567890123456789012'
            }
        ).status_code
        self.assertEqual(r, 201)

class TestUserLogin(unittest.TestCase):

    def test_login_to_nonexistant_account(self):
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/login',
            json={
                'login': 'I_do_not_exist',
                'pwdh': '12345678901234567890123456789012',
                'fingerprint': 'doesnt-matter-but-unique'
            }
        ).status_code
        self.assertEqual(r, 404)
    
    def test_fresh_login_to_existing_account(self):
        global token_new
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/login',
            json={
                'login': 'very-unique-login',
                'pwdh': '12345678901234567890123456789012',
                'fingerprint': 'matters-and-is-unique'
            }
        )
        self.assertEqual(r.status_code, 201)

        token_new = r.json()['data']['access']
        self.assertEqual(
            set(list(r.json()['data'].keys())),
            {'access', 'expiry'}
        )
    
        r = requests.get(
            url='http://127.0.0.1:5020/api/auth/account/sessions',
            headers={'Authorization': token_new}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            len(r.json()['data']['sessions']),
            1
        )
        self.assertEqual(
            r.json()['data']['sessions'][0]['uuid'],
            'matters-and-is-unique'
        )
    
    def test_login_to_the_same_account_from_another_device(self):
        global token_new_2
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/login',
            json={
                'login': 'very-unique-login',
                'pwdh': '12345678901234567890123456789012',
                'fingerprint': 'matters-but-isnt-unique'
            }
        )
        self.assertEqual(r.status_code, 201)

        token_new_2 = r.json()['data']['access']
        self.assertEqual(
            set(list(r.json()['data'].keys())),
            {'access', 'expiry'}
        )

        r = requests.get(
            url='http://127.0.0.1:5020/api/auth/account/sessions',
            headers={'Authorization': token_new_2}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
                len(r.json()['data']['sessions']),
                2
        )
        self.assertEqual(
            set(el['uuid'] for el in r.json()['data']['sessions']),
            {
                'matters-and-is-unique',
                'matters-but-isnt-unique'
            }
        )

    def test_login_to_test_1_from_the_same_browser(self):
        global token_new, token_test_1

        # relogin
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/login',
            json={
                'login': 'not-so-very-unique-login',
                'pwdh': '12345678901234567890123456789012',
                'fingerprint': 'matters-but-isnt-unique'
            }
        )
        self.assertEqual(r.status_code, 201)

        # check that response included tokens
        token_test_1 = r.json()['data']['access']
        self.assertEqual(
            set(list(r.json()['data'].keys())),
            {'access', 'expiry'}
        )

        # check session was terminated
        r = requests.get(
            url='http://127.0.0.1:5020/api/auth/account/sessions',
            headers={'Authorization': token_new}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
                len(r.json()['data']['sessions']),
                1
        )
        self.assertEqual(
            set(el['uuid'] for el in r.json()['data']['sessions']),
            {
                'matters-and-is-unique',
            }
        )

        # check that new session appeared
        r = requests.get(
            url='http://127.0.0.1:5020/api/auth/account/sessions',
            headers={'Authorization': token_test_1}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
                len(r.json()['data']['sessions']),
                2
        )
        self.assertEqual(
            set(el['uuid'] for el in r.json()['data']['sessions']),
            {
                'matters-but-isnt-unique',
                'v3ry-un1q-ue1d-1111'
            }
        )
    
    def test_logout_user_1(self):
        # check that new session appeared
        r = requests.get(
            url='http://127.0.0.1:5020/api/auth/account/sessions',
            headers={'Authorization': token_test_1}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
                len(r.json()['data']['sessions']),
                2
        )
        self.assertEqual(
            set(el['uuid'] for el in r.json()['data']['sessions']),
            {
                'matters-but-isnt-unique',
                'v3ry-un1q-ue1d-1111'
            }
        )

        # logout once
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/logout',
            headers={'Authorization': token_test_1}
        )
        self.assertEqual(r.status_code, 200)

        # check that session dissapeared
        r = requests.get(
            url='http://127.0.0.1:5020/api/auth/account/sessions',
            headers={'Authorization': token_pointing_to_user_1}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
                len(r.json()['data']['sessions']),
                1
        )
        self.assertEqual(
            set(el['uuid'] for el in r.json()['data']['sessions']),
            {
                'v3ry-un1q-ue1d-1111'
            }
        )

        # logout once again
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/logout',
            headers={'Authorization': token_test_1}
        )
        self.assertEqual(r.status_code, 410)
    
    def test_logout_of_nonexistant_account(self):
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/logout',
            headers={'Authorization': token_pointing_to_nonexistant_user}
        )
        self.assertEqual(r.status_code, 410)


class TestRefreshToken(unittest.TestCase):

    def test_no_refresh_token(self):
        self.fail()
    
    def test_refresh_token_pointing_nowhere(self):
        self.fail()
    
    def test_refresh_token_pair(self):
        self.fail()
    
    def test_refresh_check_token_is_replaced(self):
        self.fail()
    
    
if __name__ == "__main__":
    # prepare testSuit
    runner = unittest.TextTestRunner()

    # reset database
    dbname = 'koleso2_test'
    prepare_test_environment(dbname)

    # run tests
    runner.run(suite(__name__))