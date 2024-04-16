"""Contains an object that can delete messages"""


from feed_server import db
from feed_server.services.messages.interfaces import MessageDeleterInterface
from feed_server.helpers.quiries_helpers import get_chat_by_id, get_message_by_id
import feed_server.helpers.access_helpers as access

class MesageDeleter(MessageDeleterInterface):

    @staticmethod
    def delete_message(user_id: int, chat_id: int, message_id: int) -> int:

        chat = get_chat_by_id(chat_id=chat_id)
        access.verify_user_in_chat(chat=chat, user_id=user_id)

        access.verify_message_belongs_to_chat(chat=chat, message_id=message_id)
        message = get_message_by_id(message_id=message_id)

        access.verify_message_authorship(message=message, user_id=user_id)
        db.session.remove(message)
        db.session.commit()

        return message.id
