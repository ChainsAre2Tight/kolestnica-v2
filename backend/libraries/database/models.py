"""Defines SQLAlchemy models used in this project"""


from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, BigInteger
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database import db


User_Chats = Table(
    "user_chats",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("chat_id", ForeignKey("chat.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    alias: Mapped[str] = mapped_column(String(32))
    image_href: Mapped[str] = mapped_column(String(300), default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXaoP2F5I4FX1KWv3n_IRajRWfrKli9zESuXTqRgLoa89vsPBTPwEZEVyKstJ_GbXRUQg&usqp=CAU')
    sessions: Mapped[List["Session"]] = relationship(back_populates='user')
    chats: Mapped[List["Chat"]] = relationship(secondary=User_Chats, back_populates='users')


class UserLogin(db.Model):
    __tablename__ = 'userlogin'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship()
    login: Mapped[str] = mapped_column(String(32), unique=True)
    pwdh: Mapped[str] = mapped_column(String(32))


class Session(db.Model):
    __tablename__ = 'session'

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(300), unique=True, nullable=True)
    socketId: Mapped[str] = mapped_column(String(128), unique=True, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates='sessions')


class Chat(db.Model):
    __tablename__ = 'chat'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    image_href: Mapped[str] = mapped_column(String(500), nullable=True)
    messages: Mapped[List["Message"]] = relationship(back_populates="chat")
    users: Mapped[List[User]] = relationship(secondary=User_Chats, back_populates="chats")


class ChatEncryption(db.Model):
    __tablename__ = 'chatencryption'

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(128))
    chat_id: Mapped[int] = mapped_column(ForeignKey('user.id'))


class Message(db.Model):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(1000))
    timestamp: Mapped[int] = mapped_column(type_=BigInteger)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship()
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    chat: Mapped["Chat"] = relationship(back_populates="messages")
