"""Provides serializer for chats"""


from libraries.database.models import Chat


class ChatSerializer:

    @staticmethod
    def full(chat: Chat) -> dict:
        return {
            'id': chat.id,
            'name': chat.name,
            'image_href': chat.image_href,
            'message_ids': [msg.id for msg in chat.messages],
            'user_ids': [user.id for user in chat.users],
            'encryption_key': chat.encryption_key,
        }

    @staticmethod
    def to_ids(chats: list[Chat]) -> list[int]:
        return [chat.id for chat in chats]
