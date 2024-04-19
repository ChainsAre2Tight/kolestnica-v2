"""Contains an object that can delete messages"""


from libraries.database.models import Message

from feed_server import db, celery
from feed_server.services.messages.interfaces import MessageDeleterInterface
import feed_server.helpers.quiries_helpers as quiry
import feed_server.helpers.access_helpers as access

class MessageDeleter(MessageDeleterInterface):

    @staticmethod
    def delete_message(
            chat_id: int,
            message_id: int,
            browser_fingerprint: str
        ) -> Message:

        user_id = quiry.get_user_id_by_browser_fingerprint(browser_fingerprint=browser_fingerprint)
        chat = quiry.get_chat_by_id(chat_id=chat_id)
        access.verify_user_in_chat(chat=chat, user_id=user_id)

        access.verify_message_belongs_to_chat(chat=chat, message_id=message_id)
        message = quiry.get_message_by_id(message_id=message_id)

        access.verify_message_authorship(message=message, user_id=user_id)
        db.session.remove(message)
        db.session.commit()

        MessageDeleter._notify(chat_id=chat_id, message_id=message_id)
        return message

    @staticmethod
    def _notify(chat_id: int, message_id: int) -> None:
        celery.send_task('tasks.delete_message', (chat_id, message_id))
