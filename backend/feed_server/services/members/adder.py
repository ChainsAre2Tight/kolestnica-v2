"""Provides class that adds members to chat"""


from libraries.utils.my_dataclasses import OtherUser
from libraries.utils.exc import NoAcccessException, RequestAlreadyFullfilled

from feed_server.services.members.interfaces import MemberAdderInterface
import feed_server.helpers.quiries_helpers as quiry
from feed_server.helpers.access_helpers import verify_user_in_chat
from feed_server.helpers.decorators import commit


class MemberAdder(MemberAdderInterface):

    @staticmethod
    @commit
    def add_member(chat_id: int, target_id: int, broser_fingerprint: str) -> list[OtherUser]:

        user_id = quiry.get_user_id_by_browser_fingerprint(browser_fingerprint=broser_fingerprint)
        chat = quiry.get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat=chat, user_id=user_id)

        try:
            verify_user_in_chat(chat=chat, user_id=target_id)
            raise RequestAlreadyFullfilled('Requested user TBA is already a chat member')
        except NoAcccessException:
            pass

        target_user = quiry.get_user_by_id(user_id=target_id)
        chat.users.append(target_user)

        result = [OtherUser.from_model(user) for user in chat.users]
        return result
