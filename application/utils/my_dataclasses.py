from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Token:
    sessionId: str
    exp: int

class ModelDataclassInterface(ABC):

    @staticmethod
    @abstractmethod
    def from_model(model_object) -> object:
        """Constructs a dataclass object from SQLAlcmemy model object"""
        pass

def convert_model_to_dataclass(objects: list, target_dataclass: ModelDataclassInterface) -> list[object]:
    """Attempts to convert provided list of SQLAlchemy model objects to specified dataclass"""

    return [target_dataclass.from_model(obj) for obj in objects]

@dataclass
class Chat(ModelDataclassInterface):
    id: int
    name: str
    image_href: str
    user_ids: list[str]
    message_ids: list[str]

    @staticmethod
    def from_model(model_object) -> object:
        return Chat(
            id=model_object.id,
            name=model_object.name,
            image_href=model_object.image_href,
            message_ids=[msg.id for msg in model_object.messages],
            user_ids=[user.id for user in model_object.users]
        )

@dataclass
class OtherUser(ModelDataclassInterface):
    id: int
    username: str
    alias: str
    image_href: str

    @staticmethod
    def from_model(model_object) -> object:
        return OtherUser(
            id=model_object.id,
            username=model_object.username,
            alias=model_object.alias,
            image_href=model_object.image_href
        )
