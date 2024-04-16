"""Provides class that lists members of chat"""


from libraries.utils.my_dataclasses import OtherUser

from feed_server.services.members.interfaces import MemberListerInterface
from feed_server.helpers.quiries_helpers import get_chat_by_id
from feed_server.helpers.access_helpers import verify_user_in_chat


class MemberLister(MemberListerInterface):

    @staticmethod
    def list_members(chat_id: int, issuer_id: int) -> list[OtherUser]:
        chat = get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat=chat, user_id=issuer_id)

        result = [OtherUser.from_model(user) for user in chat.users]
        return result
