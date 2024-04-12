from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing_extensions import Literal


@dataclass
class Token:
    sessionId: str
    exp: int
    typ: Literal['acc', 'ref']

@dataclass
class SignedTokenPair:
    access: str
    refresh: str
    access_expiry: int
    refresh_expiry: int

class ModelDataclassInterface(ABC):

    @staticmethod
    @abstractmethod
    def from_model(model_object) -> object:
        """
        Constructs a dataclass object from SQLAlcmemy model object
        :param model_object: Specifies a SQLAlchemy object to conver
        """
        pass

    @abstractmethod
    def to_model(self, model) -> object:
        """
        Constructs a SQLAlchemy object from dataclass object
        :param model: Specifies a SQLAlchemy model
        """
        pass

def convert_model_to_dataclass(objects: list, target_dataclass: ModelDataclassInterface) -> list[object]:
    """Attempts to convert provided list of SQLAlchemy model objects to specified dataclass"""

    return [target_dataclass.from_model(obj) for obj in objects]

def convert_dataclass_to_dict(objects: list[ModelDataclassInterface]) -> list[dict]:
    """Converts a list of dataclass objects to dictionary objects"""

    return [obj.__dict__ for obj in objects]

@dataclass
class Chat(ModelDataclassInterface):
    id: int | None
    name: str
    image_href: str | None
    user_ids: list[str]
    message_ids: list[str] | None

    @staticmethod
    def from_model(model_object) -> object:
        return Chat(
            id=model_object.id,
            name=model_object.name,
            image_href=model_object.image_href,
            message_ids=[msg.id for msg in model_object.messages],
            user_ids=[user.id for user in model_object.users]
        )
    
    def to_model(self, model) -> object:
        raise NotImplementedError

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
    
    def to_model(self, model) -> object:
        raise NotImplementedError

class CurrentUser(OtherUser):
    pass

@dataclass
class Message(ModelDataclassInterface):
    id: int | None
    body: str
    timestamp: int
    chat_id: int
    author_id: int | None

    @staticmethod
    def from_model(model_object) -> object:
        return Message(
            id=model_object.id,
            body=model_object.body,
            timestamp=model_object.timestamp,
            chat_id=model_object.chat_id,
            author_id=model_object.author_id
        )
    
    def to_model(self, model) -> object:
        return model(
            body=self.body,
            timestamp=self.timestamp,
            chat_id=self.chat_id,
            author_id=self.author_id
        )

@dataclass
class Session(ModelDataclassInterface):
    uuid: str
    refresh_token: str | None
    socketId: str | None

    @staticmethod
    def from_model(model_object) -> object:
        return Session(
            uuid=model_object.uuid,
            refresh_token=model_object.refresh_token,
            socketId=model_object.socketId
        )
    
    def to_model(self, model) -> object:
        raise NotImplementedError
