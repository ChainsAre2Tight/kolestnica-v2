"""Provides serializer for sessions"""


from libraries.database.models import Session

from auth_server.services.sessions.interfaces import SessionSerializerInterface


class SessionSerializer(SessionSerializerInterface):

    @staticmethod
    def full(session: Session) -> dict:
        return {
            'id': session.id,
            'uuid': session.uuid,
        }

    @staticmethod
    def full_list(sessions: list[Session]) -> list[Session]:
        return [
            SessionSerializer.full(session=session)
            for session in sessions
        ]
