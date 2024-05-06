import validateBeforeRequest from "./request_controller";
import { HOST } from "../config";
import { Chats } from "../data/chats";
import { getChatMembers } from "./member_controller";
import { getChatMessages } from "./message_controller";


export async function getChats(setChats) {
    const chats = []
    await constructChats(chats)
    await setChats(chats)
    console.log(chats)
}

async function constructChats(chats) {
    const chats_ids = await indexChats()
    for (const id of chats_ids) {
        let chat = await getChatData(id)
        chat.members = await getChatMembers(chat)
        chat.messages = await getChatMessages(chat)
        chats.push(chat)
    }
}

async function updateChat(chatId) {
    const chat = await getChatData(chatId)
    chat.members = await getChatMembers(chat)
    chat.messages = await getChatMessages(chat)
    return chat
}

async function indexChats() {
    const decoratedRequest = validateBeforeRequest(sendIndexChatsRequest)
    const [code, content] = await decoratedRequest()
    if (code === 200) {
        const chats_ids = await content.data.chats
        console.log(chats_ids)
        return chats_ids
    } else {
        console.log(code, content)
    }
    return NaN
}

async function sendIndexChatsRequest() {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/chats/`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': window.localStorage.getItem('access'),
                },
                method: 'GET',
            }
        )
        const content = await rawResponse.json()
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}

async function makeChat(raw_chat) {
    return {
        id: raw_chat.id,
        name: raw_chat.name,
        url: raw_chat.image_href,
        key: raw_chat.encryption_key,
        messages: [],
        members: [],
    }
}

async function getChatData(chatId) {
    const decoratedRequest = validateBeforeRequest(sendGetChatDataGequest)
    const [code, content] = await decoratedRequest(chatId)
    if (code === 200) {
        const raw_chat = await content.data.chat
        const chat = await makeChat(raw_chat)
        return chat
    }
    return NaN
}

async function sendGetChatDataGequest(chatId) {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/chats/${chatId}`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': window.localStorage.getItem('access'),
                },
                method: 'GET',
            }
        )
        const content = await rawResponse.json()
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}

export async function createChat(name, url, chats, setChats, setMessage, setShowCreateChat, currentUser) {
    const decoratedRequest = validateBeforeRequest(sendCreateChatRequest)
    const [code, content] = await decoratedRequest(name, url)
    if (code === 201) {
        const raw_chat = await content.data.chat
        const chat = await makeChat(raw_chat)
        chat.members.push(currentUser)
        console.log(chats)
        await setChats([...chats, chat])
        await setMessage({level: 'success', enabled: true, message: 'Created'})
        setTimeout(() => setShowCreateChat(false), 1000)
    } else {
        console.log(code, content)
        await setMessage({level: 'failure', enabled: true, message: 'Error'})
    }
}

async function sendCreateChatRequest(name, url) {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/chats/`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': window.localStorage.getItem('access'),
                },
                method: 'POST',
                body: JSON.stringify({
                    name: name,
                    image_href: url
                })
            }
        )
        const content = await rawResponse.json()
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}

export async function addChat(chatId, chats, setChats) {
    const chat = await updateChat(chatId)
    setChats([...chats, chat])
}

export async function changeChatUrl(chatId, newUrl) {
    const decoratedRequest = validateBeforeRequest(sendChangeChatUrl)
    const [code, content] = await decoratedRequest(chatId, newUrl)
}

async function sendChangeChatUrl(chatId, newUrl) {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/chats/${chatId}`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': window.localStorage.getItem('access'),
                },
                method: 'PATCH',
                body: JSON.stringify({
                    image_href: newUrl
                })
            }
        )
        const content = await rawResponse.json()
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}

export async function recieveChatChange(chatId, chat, chats, setChat, setChats) {
    const updated_chat = await getChatData(chatId)

    const index = chats.findIndex(e => e.id === chatId)
    if (index === -1) {return}

    const chatToUpdate = chats[index]

    updated_chat.messages = chatToUpdate.messages
    updated_chat.members = chatToUpdate.members

    const new_chats = [...chats]
    new_chats[index] = updated_chat

    if (chat.id === chatId) {
        setChat(chatToUpdate)
    }
    setChats(new_chats)
}