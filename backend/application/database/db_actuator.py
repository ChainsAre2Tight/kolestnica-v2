from flask import Flask
import database.models as m
import os

def seed(app, db):
    with app.app_context():

        db.drop_all()
        db.create_all()
        db.session.commit()

        """
        User 1 and 2 are in the same chat and both have 1 message sent
        """
        test_user_1 = m.User(
            username='test_1', alias='test user #1',
        )

        test_user_1_session = m.Session(
            uuid='v3ry-un1q-ue1d-1111',
            user=test_user_1
        )

        test_user_1_login = m.UserLogin(
            login='not-so-very-unique-login',
            pwdh='12345678901234567890123456789012',
            user=test_user_1
        )

        test_user_2 = m.User(
            username='test_2', alias='test user #2',
        )

        test_user_2_session = m.Session(
            uuid='v3ry-un1q-ue1d-2222',
            user=test_user_2
        )

        """
        User 3 is in no chat
        """
        test_user_3 = m.User(
            username='test_3', alias='test user #3',
        )

        test_user_3_session = m.Session(
            uuid='v3ry-un1q-ue1d-3333',
            user=test_user_3
        )

        test_chat_1 = m.Chat(
            name='test chat #1 static',
            users=[test_user_1, test_user_2]
        )

        msg_1 = m.Message(
            body='hello world!',
            timestamp='1000000',
            author=test_user_1,
            chat=test_chat_1
        )

        msg_2 = m.Message(
            body='go away loser',
            timestamp='10000000',
            author=test_user_2,
            chat=test_chat_1
        )
        
        """
        User 4 is in a chat with himself and is used to test message sending
        """
        test_user_4 = m.User(
            username='test_4', alias='test user #4',
        )

        test_user_4_session = m.Session(
            uuid='v3ry-un1q-ue1d-4444',
            user=test_user_4
        )
        test_chat_2 = m.Chat(
            name='test chat #2 dynamic',
            users=[test_user_4]
        )
        msg_3 = m.Message(
            body='static message',
            timestamp='123321123',
            author=test_user_4,
            chat=test_chat_2
        )

        to_add = [
            test_user_1, test_user_1_session, test_user_1_login,
            test_user_2, test_user_2_session,
            test_chat_1, msg_1, msg_2,

            test_user_3, test_user_3_session,

            test_user_4, test_user_4_session,
            test_chat_2, msg_3
        ]
        db.session.add_all(to_add)
        db.session.commit()

def prepare_test_environment() -> None:

    app = Flask('db-actuator')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    db = m.db
    db.init_app(app)

    seed(app, db)

if __name__ == "__main__":
    prepare_test_environment('koleso2_test')
