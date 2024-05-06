import { HOST } from "../config"
import { addOrUpdateMessage } from "../data/chatupdator"
import { decipher_message, encipher_message } from "./encryption_controller"
import validateBeforeRequest from "./request_controller"

function constructMessage(raw_message, chat) {
    const author = chat.members.find((element) => element.id === raw_message.author_id)
    const decrypted_body = decipher_message(raw_message.body, chat.key)
    const message = {
        id: raw_message.id,
        body: decrypted_body,
        timestamp: raw_message.timestamp,
        author: author
    }
    return message
}

export async function getChatMessages(chat) {
    const decoratedRequest = validateBeforeRequest(sendGetChatMessagesRequest)
    const [code, content] = await decoratedRequest(chat.id)
    const raw_messages = content.data.messages
    const messages = []
    if (code === 200) {
        for (const raw_message of raw_messages) {
            const message = constructMessage(raw_message, chat)
            messages.push(message)
        }
    }
    return messages
}

async function sendGetChatMessagesRequest(chatId) {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/chats/${chatId}/messages/`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': window.localStorage.getItem('access'),
                },
                method: 'GET',
            }
        )
        console.log(rawResponse)

        const content = await rawResponse.json()
        console.log(rawResponse.status, content)
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}

export async function sendMessage(text, currentUser, chat, setChat, chats, setChats) {
    const decoratedRequest = validateBeforeRequest(sendMessageRequest)

    const encrypted_text = encipher_message(text, chat.key)

    const new_message = {
        'id': undefined,
        'body': text,
        'timestamp': Math.floor(Date.now() / 1000),
        'author': {
            'id': currentUser.id,
            'name': currentUser.name,
            'alias': currentUser.alias,
            'url': currentUser.url
        }
    }

    const [code, content] = await decoratedRequest(encrypted_text, new_message.timestamp, chat.id)
    if (code === 201) {
        new_message.id = content.data.message_id
        // addOrUpdateMessage(chat.id, new_message, chat, chats, setChat, setChats)
    }
}

async function sendMessageRequest(body, timestamp, chatId) {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/chats/${chatId}/messages/`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': window.localStorage.getItem('access'),
                },
                method: 'POST',
                body: JSON.stringify({
                    message: {
                        body: body,
                        timestamp: timestamp
                    }
                })
            }
        )
        console.log(rawResponse)

        const content = await rawResponse.json()
        console.log(rawResponse.status, content)
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}

export async function recieveMessage(chatId, messageId, chat, chats, setChat, setChats) {
    const decoratedRequest = validateBeforeRequest(sendRecieveMessageRequest)
    const [code, content] = await decoratedRequest(chatId, messageId)

    if (code === 200) {
        const chatToUpdate = await chats.find(e => e.id === chatId)
        if (chatToUpdate !== undefined) {
            const raw_message = content.data.message
            const message = constructMessage(raw_message, chatToUpdate)
            addOrUpdateMessage(chatId, message, chat, chats, setChat, setChats)
        } else {
            console.log(`undef ${chat}, ${chats}, ${setChat}, ${setChats}`)
        }
    }
}

async function sendRecieveMessageRequest(chatId, messageId) {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/chats/${chatId}/messages/${messageId}`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Authorization': window.localStorage.getItem('access'),
                },
                method: 'GET',
            }
        )
        console.log(rawResponse)

        const content = await rawResponse.json()
        console.log(rawResponse.status, content)
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}