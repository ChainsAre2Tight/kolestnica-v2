"""Provides class that adds members to chat"""


from libraries.database.models import User
from libraries.utils.exc import NoAcccessException, RequestAlreadyFullfilled

from feed_server import celery
from feed_server.services.members.interfaces import MemberAdderInterface
import feed_server.helpers.quiries_helpers as quiry
from feed_server.helpers.access_helpers import verify_user_in_chat
from feed_server.helpers.decorators import commit


class MemberAdder(MemberAdderInterface):

    @staticmethod
    @commit
    def add_member(chat_id: int, target_username: int, browser_fingerprint: str) -> list[User]:

        user_id = quiry.get_user_id_by_browser_fingerprint(browser_fingerprint=browser_fingerprint)
        chat = quiry.get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat=chat, user_id=user_id)

        target_user = quiry.get_user_by_username(username=target_username)

        try:
            verify_user_in_chat(chat=chat, user_id=target_user.id)
            raise RequestAlreadyFullfilled('Requested user TBA is already a chat member')
        except NoAcccessException:
            pass

        chat.users.append(target_user)

        MemberAdder._notify_newbie(user=target_user, chat_id=chat_id)
        MemberAdder._notify_existing(chat_id=chat_id)

        return chat.users

    @staticmethod
    def _notify_existing(chat_id: int) -> None:
        celery.send_task('notify_change_member', (chat_id,))

    @staticmethod
    def _notify_newbie(user: User, chat_id: int) -> None:
        for session in user.sessions:
            if session.socketId is not None:
                celery.send_task('add_to_chat', (session.socketId, chat_id))
