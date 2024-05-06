

export function addOrUpdateMessage(chat_id, message, chat, chats, setChat, setChats) {
    const old_chat = chats.find(element => element.id === chat_id)
    const old_messages = old_chat.messages
    const new_messages = [...old_messages]


    const already_present_message_index = old_messages.findIndex(
        element => element.id === message
    )

    if (already_present_message_index === -1) {
        new_messages.push(message)
    } else {
        new_messages[already_present_message_index] = message
    }

    const updated_chat = {
        ...old_chat,
        'messages': new_messages
    }

    const chat_index = chats.findIndex(
        element => element.id === updated_chat.id
    )

    const new_chats = [...chats]
    new_chats[chat_index] = updated_chat

    if (chat.id === updated_chat.id) {
        setChat(a => updated_chat)
    }
    setChats(a => new_chats)
}