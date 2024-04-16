"""Provides functions that check user rights"""


from libraries.database import models
from libraries.utils.exc import NoAcccessException, ConflictingData, NotPermittedException


def verify_user_in_chat(chat: models.Chat, user_id: int) -> None:
    """Verifies that user has access to certain chat

    Args:
        chat (models.Chat): chat in question
        user_id (int): user making the request

    Raises:
        NoAcccessException: if user has no access to this chat
    """
    if user_id not in [user.id for user in chat.users]:
        raise NoAcccessException(f'User #{user_id} has no access to chat #{chat.id}')


def verify_message_belongs_to_chat(chat: models.Chat, message_id: int) -> None:
    """Verifies that message belongs to ccertain chat

    Args:
        chat (models.Chat): chat in question
        message_id (int): message to check

    Raises:
        ConflictingData: if message does not belong to chat
    """
    if message_id not in [message.id for message in chat.messages]:
        raise ConflictingData(f'Message #{message_id} does not belong to chat #{chat.id}')


def verify_message_authorship(message: models.Message, user_id: int) -> None:
    """Verifies that user is an author of this message

    Args:
        message (models.Message): message in question
        user_id (int): id of user to check

    Raises:
        NotPermittedException: If user is not author of the message
    """
    if message.author_id != user_id:
        raise NotPermittedException(f'User #{user_id} is not author of message #{message.id}')
