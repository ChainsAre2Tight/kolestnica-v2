"""Shared data"""


class SessionData:
    fingerprint: str
    access_token: str
    refresh_token: str

    def __init__(self, fingerprint) -> None:
        self.fingerprint = fingerprint
        self.access_token = None
        self.access_token = None


class UserData:
    login: str
    password: str
    username: str
    sessions: list[SessionData]
    id: int

    def __init__(self, login: str, password: str, username: str) -> None:
        self.login = login
        self.password = password
        self.username = username


class ChatData:
    name: str
    id: int

    def __init__(self, name: str) -> None:
        self.name = name


class MessageData:
    body: str
    id: int
    timestamp: int
    author_id: int

    def __init__(self, body: str, timestamp: int) -> None:
        self.body = body
        self.timestamp = timestamp
