"""Provides chat patcher class"""


from libraries.database import models

from feed_server import db, celery
import feed_server.helpers.quiries_helpers as quiry
from feed_server.helpers.access_helpers import verify_user_in_chat


class ChatPatcher:

    @staticmethod
    def update_image(browser_fingerprint: str, chat_id: int, image_href: str) -> models.Chat:

        user_id = quiry.get_user_id_by_browser_fingerprint(browser_fingerprint=browser_fingerprint)
        chat = quiry.get_chat_by_id(chat_id=chat_id)
        verify_user_in_chat(chat=chat, user_id=user_id)

        chat.image_href = image_href
        db.session.commit()

        ChatPatcher._notify(chat_id=chat_id)

        return chat

    @staticmethod
    def _notify(chat_id: int) -> None:
        celery.send_task('update_chat', (chat_id,))
