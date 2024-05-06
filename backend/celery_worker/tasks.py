"""Provides tasks for notification server"""


from celery_worker import app
from celery_worker.helpers import send_request, fail_on_exception


# chats
@app.task(name='create_chat', bind=True)
@fail_on_exception
def create_chat(self, sid: str, chat_id: int):
    send_request('POST', '/chats/', {'sid': sid, 'chat_id': chat_id}, 201)

@app.task(name='update_chat', bind=True)
@fail_on_exception
def update_chat(self, chat_id: int):  # Unused as it lacks interactor
    send_request('PATCH', f'/chats/{chat_id}', {'a': 'b'})

@app.task(name='delete_chat', bind=True)
@fail_on_exception
def delete_chat(self, chat_id: int):  # Unused as it lacks interactor
    send_request('DELETE', f'/chats/{chat_id}')


# members
@app.task(name='notify_change_member', bind=True)
@fail_on_exception
def notify_change(self, chat_id: int):
    send_request('PATCH', f'/chats/{chat_id}/members/', {'a': 'b'}, 200)

@app.task(name='add_to_chat', bind=True)
@fail_on_exception
def add_to_chat(self, sid: str, chat_id: int):
    send_request('POST', f'/chats/{chat_id}/members/', {'sid': sid}, 201)

@app.task(name='remove_from_chat', bind=True)
@fail_on_exception
def remove_from_chat(self, sid: str, chat_id: int):
    send_request('DELETE', f'/chats/{chat_id}/members/{sid}')


# messages
@app.task(name='add_message', bind=True)
@fail_on_exception
def add_message(self, chat_id: int, message_id: int):
    print(f'--> got task add message {chat_id}/{message_id}')
    send_request('POST', f'/chats/{chat_id}/messages/', {'message_id': message_id}, 201)

@app.task(name='delete_message', bind=True)
@fail_on_exception
def delete_message(self, chat_id: int, message_id: int):
    send_request('DELETE', f'/chats/{chat_id}/messages/{message_id}')

@app.task(name='update_message', bind=True)
@fail_on_exception
def update_message(self, chat_id: int, message_id: int):
    send_request('PATCH', f'/chats/{chat_id}/messages/{message_id}')
