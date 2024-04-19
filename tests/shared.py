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

    def __init__(self, login: str, password: str, username: str) -> None:
        self.login = login
        self.password = password
        self.username = username