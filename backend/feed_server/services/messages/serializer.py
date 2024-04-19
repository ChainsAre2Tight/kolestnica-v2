"""Provides serializer for messages"""


from libraries.database.models import Message

from feed_server.services.messages.interfaces import MessageSerializerInterface


class MessageSerializer(MessageSerializerInterface):

    @staticmethod
    def to_id(message: Message) -> int:
        return message.id

    @staticmethod
    def full(message: Message) -> dict:
        return {
            'id': message.id,
            'body': message.body,
            'timestamp': message.timestamp,
            'author_id': message.author_id
        }

    @staticmethod
    def full_list(messages: list[Message]) -> list[dict]:
        return [
            MessageSerializer.full(message=message)
            for message in messages
        ]
