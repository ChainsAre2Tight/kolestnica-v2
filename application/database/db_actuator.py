from flask import Flask
import models as m

def prepare_test_environment() -> None:

    app = Flask('db-actuator')
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/koleso2"
    db = m.db
    db.init_app(app)

    with app.app_context():

        db.drop_all()
        db.create_all()
        db.session.commit()

        test_user_1 = m.User(
            username='test_1', alias='test user #1',
        )

        test_user_1_login = m.UserLogin(
            login='test1',
            pwdh='99024280cab824efca53a5d1341b9210',
            user=test_user_1
        )

        test_user_1_session = m.Session(
            uuid='v3ry-un1q-ue1d-1111',
            user=test_user_1
        )

        test_user_2 = m.User(
            username='test_2', alias='test user #2',
        )

        test_user_2_login = m.UserLogin(
            login='test2',
            pwdh='36ddda5af915d91549d3ab5bff1bafec',
            user=test_user_2
        )

        test_user_2_session = m.Session(
            uuid='v3ry-un1q-ue1d-2222',
            user=test_user_2
        )

        test_user_3 = m.User(
            username='test_3', alias='test user #3',
        )

        test_user_3_login = m.UserLogin(
            login='test3',
            pwdh='7d7e94f4e318389eb8de80dcaddffb32',
            user=test_user_3
        )

        test_user_3_session = m.Session(
            uuid='v3ry-un1q-ue1d-3333',
            user=test_user_3
        )

        test_chat_1 = m.Chat(
            name='test chat #1',
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

        db.session.add(test_user_1)
        db.session.add(test_user_1_login)
        db.session.add(test_user_1_session)
        db.session.add(test_user_2)
        db.session.add(test_user_2_login)
        db.session.add(test_user_2_session)
        db.session.add(test_user_3)
        db.session.add(test_user_3_login)
        db.session.add(test_user_3_session)
        db.session.add(test_chat_1)
        db.session.add(msg_1)
        db.session.add(msg_2)

        db.session.commit()

if __name__ == "__main__":
    prepare_test_environment()
