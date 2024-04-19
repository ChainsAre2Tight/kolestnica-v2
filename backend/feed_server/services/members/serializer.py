"""Provides serializer for chat members"""


from libraries.database.models import User

from feed_server.services.members.interfaces import MemberSerializerInterface


class MemberSerializer(MemberSerializerInterface):

    @staticmethod
    def to_ids(members: list[User]) -> list[int]:
        return [member.id for member in members]

    @staticmethod
    def id_name_alias(members: list[User]) -> list[dict]:
        return [
            {
                'id': member.id,
                'username': member.username,
                'alias': member.alias,
            }
            for member in members
        ]
