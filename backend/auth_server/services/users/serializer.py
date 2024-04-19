"""Provides serializer for users"""


from libraries.database.models import User

from auth_server.services.users.interfaces import UserSerializatorInterface


class UserSerializer(UserSerializatorInterface):

    @staticmethod
    def to_id(user: User) -> int:
        return user.id

    @staticmethod
    def full(user: User) -> dict:
        return {
            'id': user.id,
            'username': user.username,
            'alias': user.alias,
            'image_href': user.image_href,
        }
