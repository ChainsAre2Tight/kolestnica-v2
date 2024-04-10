import unittest
import requests
import sys
import inspect

if __name__ == "__main__":
    sys.path.append('../application/database')
    from db_actuator import prepare_test_environment

default_href: str = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXaoP2F5I4FX1KWv3n_IRajRWfrKli9zESuXTqRgLoa89vsPBTPwEZEVyKstJ_GbXRUQg&usqp=CAU'
corrupted_token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIxMjM0NTY3ODkwIiwiZXhwIjoxMDB9.CAwkokoCzrjvhyMRDaciZO0YSnMys20H4RpF8iGwT3h'
expired_token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIxMjM0NTY3ODkwIiwiZXhwIjoxMDB9.CAwkokoCzrjvhyMRDaciZO0YSnMys20H4RpF8iGwT3Y'
valid_token: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIxMjM0NTY3ODkwIiwiZXhwIjoxMDAwMDAwMDAwMH0._XGzlL7svHZnZPM8mg4ZZRZFcPGhDlEEcgUYXSiAviU'
token_pointing_to_user_1: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiJ2M3J5LXVuMXEtdWUxZC0xMTExIiwiZXhwIjoxMDAwMDAwMDAwMH0.jIteq0z276zQAZpofkCIxiUuX8AeezZoeLF3Cq3UZPU'
token_pointing_to_nonexistant_user: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIxLWRvLW5vdC1leGlzdCIsImV4cCI6MTAwMDAwMDAwMDB9.e_KDA2yrnnaGArunSp8WNDmuvWY07IGnWWZ83gp1GjE'
token_pointing_to_user_3: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiJ2M3J5LXVuMXEtdWUxZC0zMzMzIiwiZXhwIjoxMDAwMDAwMDAwMH0.emJ2u5x4BHcmGE71r2gw6IdDcHb7iLk1LriAMrO-Qe8'
token_pointing_to_user_4: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiJ2M3J5LXVuMXEtdWUxZC00NDQ0IiwiZXhwIjoxMDAwMDAwMDAwMH0.Ok6-k8tS8iC8dg1DW2NG_azr4fXxRuLhfJC7ifrrthM'

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
            ([{'id': 1, 'image_href': None, 'message_ids': [1, 2], 'name': 'test chat #1 static', 'user_ids': [1, 2]}], 200)
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
    
        self.assertEqual(
            (r.json(), r.status_code),
            ([
                {'id': 1, 'username': 'test_1', 'alias': 'test user #1', 'image_href': default_href},
                {'id': 2, 'username': 'test_2', 'alias': 'test user #2', 'image_href': default_href}
            ], 200)
        )
    
    def test_request_chats_for_user_in_chat_2(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/users',
            headers={'Authorization': token_pointing_to_user_4}
        )
    
        self.assertEqual(
            (r.json(), r.status_code),
            ([
                {'id': 4, 'username': 'test_4', 'alias': 'test user #4', 'image_href': default_href},
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

class TestStaticMessages(unittest.TestCase):

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
    
        self.assertEqual(
            (r.json(), r.status_code),
            ([{
                'author_id': 4,
                'body': 'static message',
                'chat_id': 2,
                'id': 3,
                'timestamp': 123321123
            }], 200)
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

        self.assertEqual(
            (r.json(), r.status_code),
            ({
                'msg_id': 4,
            }, 201)
        )
    
    def test_get_sent_message_by_user_in_chat(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/2/messages',
            headers={'Authorization': token_pointing_to_user_4}
        )
    
        self.assertEqual(
            (r.json(), r.status_code),
            ([{
                'author_id': 4,
                'body': 'static message',
                'chat_id': 2,
                'id': 3,
                'timestamp': 123321123
            },
            {
                'author_id': 4,
                'body': 'i sent this message ;)',
                'chat_id': 2,
                'id': 4,
                'timestamp': 1234567890
            }], 200)
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
    
        self.assertEqual(
            (r.json(), r.status_code),
            ({'msg_id': 4}, 200)
        )

class TestChatActions(unittest.TestCase):

    def test_create_chat(self):
        global token_pointing_to_user_4
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats',
            headers={'Authorization': token_pointing_to_user_4},
            json={'chat_name': 'dynamically created chat'}
        )
    
        self.assertEqual(
            (r.json()['chat_id'], r.status_code),
            (3, 201)
        )
    
    def test_verify_chat_creation(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats',
            headers={'Authorization': token_pointing_to_user_4}
        )

        self.assertEqual(
            (r.json(), r.status_code),
            ([
                {'id': 2, 'image_href': None, 'message_ids': [3], 'name': 'test chat #2 dynamic', 'user_ids': [4]},
                {'id': 3, 'image_href': None, 'message_ids': [], 'name': 'dynamically created chat', 'user_ids': [4]}
            ], 200)
        )
    
    def test_verify_user_list_before(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/3/users',
            headers={'Authorization': token_pointing_to_user_4}
        )

        self.assertEqual(
            (r.json(), r.status_code),
            ([
                {'id': 4, 'username': 'test_4', 'alias': 'test user #4', 'image_href': default_href}
            ], 200)
        )
    
    def test_add_user_to_chat_user_has_no_access_to(self):
        global token_pointing_to_user_3
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/3/users',
            headers={'Authorization': token_pointing_to_user_3},
            json={'username': 'some_user'}
        )

        self.assertEqual(
            (r.json()['Error'], r.status_code),
            ('Cannot access requested data', 404)
        )

    def test_add_user_that_doesnt_exist(self):
        global token_pointing_to_user_4
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/3/users',
            headers={'Authorization': token_pointing_to_user_4},
            json={'username': 'some_user'}
        )

        self.assertEqual(
            (r.json()['Error'], r.status_code),
            ('Requested user does not exist', 404)
        )
    
    def test_add_user_that_is_already_in_chat(self):
        global token_pointing_to_user_1
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/1/users',
            headers={'Authorization': token_pointing_to_user_1},
            json={'username': 'test_2'}
        )

        self.assertEqual(
            (r.json()['Error'], r.status_code),
            ('Requirement is already fullfilled', 406)
        )
    
    def test_add_yourself(self):
        global token_pointing_to_user_1
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/1/users',
            headers={'Authorization': token_pointing_to_user_1},
            json={'username': 'test_1'}
        )

        self.assertEqual(
            (r.json()['Error'], r.status_code),
            ('Requirement is already fullfilled', 406)
        )
    
    def test_add_valid_user(self):
        global token_pointing_to_user_4
        r = requests.post(
            url='http://127.0.0.1:5010/api/data/chats/3/users',
            headers={'Authorization': token_pointing_to_user_4},
            json={'username': 'test_1'}
        )

        self.assertEqual(
            (r.json(), r.status_code),
            ({'id': 1, 'username': 'test_1', 'alias': 'test user #1', 'image_href': default_href}, 201)
        )

    def test_verify_user_list_after(self):
        global token_pointing_to_user_4
        r = requests.get(
            url='http://127.0.0.1:5010/api/data/chats/3/users',
            headers={'Authorization': token_pointing_to_user_4}
        )

        print(r.json())

        self.assertEqual(
            ({i['id'] for i in r.json()}, r.status_code),
            ({1, 4}, 200)
        )

if __name__ == '__main__':

    def isTestClass(x):
        return inspect.isclass(x) and issubclass(x, unittest.TestCase)


    def isTestFunction(x):
        return inspect.isfunction(x) and x.__name__.startswith("test")

    def suite():

        # get current module object
        module = sys.modules[__name__]

        # get all test className,class tuples in current module
        testClasses = [
            tup for tup in
            inspect.getmembers(module, isTestClass)
        ]

        # sort classes by line number
        testClasses.sort(key=lambda t: inspect.getsourcelines(t[1])[1])

        testSuite = unittest.TestSuite()

        for testClass in testClasses:
            # get list of testFunctionName,testFunction tuples in current class
            classTests = [
                tup for tup in
                inspect.getmembers(testClass[1], isTestFunction)
            ]

            # sort TestFunctions by line number
            classTests.sort(key=lambda t: inspect.getsourcelines(t[1])[1])

            # create TestCase instances and add to testSuite;
            for test in classTests:
                testSuite.addTest(testClass[1](test[0]))

        return testSuite

if __name__ == "__main__":
    # prepare testSuit
    runner = unittest.TextTestRunner()

    # reset database
    dbname = 'koleso2_test'
    prepare_test_environment(dbname)

    # run tests
    runner.run(suite())
