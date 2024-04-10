import unittest
import sys
from globals import *
from preparesuit import suite
import requests

if __name__ == '__main__':

    sys.path.append('../application/database')
    from db_actuator import prepare_test_environment


class TestAvaliability(unittest.TestCase):

    def test_ping(self):
        r = requests.get('http://127.0.0.1:5020/api/auth').status_code
        self.assertEqual(r, 400)
    
    def test_bad_token(self):
        global corrupted_token
        r = requests.get(
            url='http://127.0.0.1:5020/api/auth',
            headers={'Authorization': corrupted_token}
        ).status_code
        self.assertEqual(r, 403)
    
    def test_expired_token(self):
        global expired_token
        r = requests.get(
            url='http://127.0.0.1:5020/api/auth',
            headers={'Authorization': expired_token}
        ).status_code
        self.assertEqual(r, 401)
    
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
            headers={'Authorization': token_pointing_to_nonexistant_user},
            json={'some': 'data', 'is': 'missing'}
        ).status_code
        self.assertEqual(r, 400)

    def test_duplicate_login(self):
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/register',
            headers={'Authorization': token_pointing_to_nonexistant_user},
            json={
                'username': 'some_uniaue_username',
                'login': 'not-so-very-unique-login',
                'pdwh': '12345678901234567890123456789012'
            }
        ).status_code
        self.assertEqual(r, 409)

    def test_duplicate_username(self):
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/register',
            headers={'Authorization': token_pointing_to_nonexistant_user},
            json={
                'username': 'test_1',
                'login': 'very-unique-login',
                'pdwh': '12345678901234567890123456789012'
            }
        ).status_code
        self.assertEqual(r, 406)

    def test_valid_data(self):
        r = requests.post(
            url='http://127.0.0.1:5020/api/auth/register',
            headers={'Authorization': token_pointing_to_nonexistant_user},
            json={
                'username': 'very-unique-username',
                'login': 'very-unique-login',
                'pdwh': '12345678901234567890123456789012'
            }
        ).status_code
        self.assertEqual(r, 201)

    
if __name__ == "__main__":
    # prepare testSuit
    runner = unittest.TextTestRunner()

    # reset database
    dbname = 'koleso2_test'
    prepare_test_environment(dbname)

    # run tests
    runner.run(suite(__name__))