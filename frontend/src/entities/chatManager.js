import { useState } from "react"
import { validateStrict } from "../validators/loginvalidation"
import { addChatMember } from "../controllers/member_controller"
import { changeChatUrl } from "../controllers/chat_controller"


export function ChatEditorButton({ showEditor, setShowEditor }) {
    return (
        <button
        className="bg-darkgray-400 rounded-full w-8 h-8 min-w-8"
        onClick={() => setShowEditor(!showEditor)}
        >
            {showEditor ? '-' : "+"}
        </button>
    )
}

export function ChatEditor({ chat }) {
    const members = chat.members.map(m => <ChatMember member={m}/>)
    return (
        <div className="h-full w-full flex flex-col items-center">
            <div className="w-full max-w-2xl flex flex-col items-center mt-5">
                <div className="w-fit flex flex-col items-center">
                    <img src={chat.url} className="w-64 h-64 rounded-full" alt="chatpfp"/>
                    <div className="text-white w-fit text-2xl mt-2 mb-2 p-2 rounded-xl bg-darkgray-800">
                        {chat.name}
                    </div>
                </div>

                <ChatURLForm chat={chat}/>

                <div className="bg-darkgray-800 p-1 w-full m-2 rounded-lg flex flex-col items-start">
                    <div className="self-center text-lg">
                        <span className="text-white">Chat members</span>
                        <span className="text-gray-400"> ({chat.members.length})</span>
                    </div>
                    <ol>
                        {members}
                    </ol>
                    <AddMemberForm chat={chat}/>
                </div>
            </div>
        </div>
    )
}

function ChatMember({ member }) {
    return (
        <li className="flex flex-row w-full p-1 m-1 rounded-lg" key={member.id}>
            <img src={member.url} alt="pfp" className="h-8 w-8 rounded-full"/>
            <div className="flex flex-row items-center">
                <span className="text-white text-xl ml-2 mr-1 align-bottom"
                >{member.alias}</span>
                <span className="text-gray-400 text-sm align-bottom"
                >({member.name})</span>
            </div>
        </li>
    )
}

function ChatURLForm({ chat }) {

    const [active, setActive] = useState(false)
    const [url, setUrl] = useState(chat.url)

    function handleSubmit(event) {
        setActive(false)
        event.preventDefault()
        const new_url = event.target.url.value
        changeChatUrl(chat.id, new_url)
    }

    function handleCancel() {
        setActive(false)
        setUrl(chat.url)
    }

    return (
        <form
        onSubmit={(e) => handleSubmit(e)}
        className="flex flex-row justify-items-stretch items-center w-full rounded-lg bg-darkgray-800 h-12"
        >
            <input
            name="url"
            value={url}
            onInput={(e) => setUrl(e.target.value)}
            className="bg-darkgray-800 grow text-middle h-8 pl-2 text-gray-400 mr-2 enabled:text-white"
            disabled={!active}
            placeholder="Chat image URL"
            />

            {active ?
            <>
            <button className="w-10 h-8 bg-green-600"
                type="submit">Set</button>
            <button className="w-10 h-8 mr-2 rounded-r-lg bg-red-600"
                onClick={handleCancel}>No</button>
            </> : <button className="w-20 h-8 mr-2 rounded-r-lg bg-blue-800 text-white"
            onClick={() => setActive(true)}>
                Change
            </button>
            }
        </form>
    )
}

function AddMemberForm({ chat }) {

    const [active, setActive] = useState(false)
    const [username, setUsername] = useState('')

    function handleSubmit(e) {
        e.preventDefault()
        const username = e.target.username.value
        if (username !== '' && validateStrict(username)) {
            addChatMember(chat, username)
            setUsername('')
        } else {
            alert('Username is invalid')
        }
        
    }

    function handleClickEnable(e) {
        e.preventDefault()
        e.stopPropagation()
        setActive(true)
    }

    return (
        <form
        onSubmit={(e) => handleSubmit(e)}
        className="flex flex-row ml-2 w-full items-center justify-content-stretch w-full mb-2"
        >
            {active ? <>
            <button
            type="submit"
            >
                <img
                className="h-8 h-8 w-min-8 rounded-full"
                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvBPuDNLFZRMEO3U2z_YxXSIQYinLlTfnuJQVV54ekng&s" />
            </button>
            <input
            name="username"
            type="text"
            onBlur={() => setTimeout(setActive(false), 100)}
            className="grow bg-darkgray-800 text-white text-lg ml-2 w-max-2xl"
            onInput={(e) => setUsername(e.target.value)}
            placeholder="New member's username"
            value={username}/>
            </>
            :
                <button
                type="button"
                className="flex flex-row items-center w-full"
                onClick={(e) => handleClickEnable(e)}>
                    <img
                    className="h-8 h-8 w-min-8 rounded-full"
                    src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvBPuDNLFZRMEO3U2z_YxXSIQYinLlTfnuJQVV54ekng&s" />
                    <span className="ml-2 text-lg text-white">
                        Add member
                    </span>
                </button>
            }
        </form>
    )
}