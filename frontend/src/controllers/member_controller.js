import { HOST } from "../config"
import validateBeforeRequest from "./request_controller"

export async function getChatMembers(chat) {
    const decoratedRequest = validateBeforeRequest(sendGetChatMembersRequest)
    const [code, content] = await decoratedRequest(chat.id)
    const raw_members = await content.data.members
    const members = []
    if (code === 200) {
        for (const raw_member of raw_members) {
            let member = {
                id: raw_member.id,
                name: raw_member.username,
                alias: raw_member.alias,
                url: raw_member.image_href
            }
            members.push(member)
        }
    }
    return members
}

async function sendGetChatMembersRequest(chatId) {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/chats/${chatId}/members/`,
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

export async function addChatMember(chat, username) {
    const decoratedRequest = validateBeforeRequest(sendAddChatMemberRequest)
    const [code, content] = await decoratedRequest(chat.id, username)

    if (code === 201) {
        console.log('added user')
    }
}

async function sendAddChatMemberRequest(chatId, username) {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/chats/${chatId}/members/`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': window.localStorage.getItem('access'),
                },
                method: 'POST',
                body: JSON.stringify({
                    username: username
                })
            }
        )
        const content = await rawResponse.json()
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}

export async function updateMembers(chatId, chat, chats, setChat, setChats) {
    const index = await chats.findIndex(element => element.id === chatId)
    if (index === -1) {
        return
    }
    const chatToUpdate = chats[index]
    const new_members = await getChatMembers(chatToUpdate)

    chatToUpdate.members = new_members

    if (chat.id === chatToUpdate.id) {
        setChat(a => chatToUpdate)
    }
    const new_chats = [...chats]
    new_chats[index] = chatToUpdate
    setChats(a => new_chats)
}