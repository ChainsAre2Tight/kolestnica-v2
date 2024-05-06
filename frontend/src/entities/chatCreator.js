import { useState } from "react"
import { validateSemiStrict } from "../validators/loginvalidation"
import { createChat } from "../controllers/chat_controller"

export function ChatCreatorButton({ showCreateChat, setShowCreateChat }) {
    function handleClick() {
        setShowCreateChat(!showCreateChat)
    }

    return (
        <button
        className={"absolute bottom-0 right-0 w-12 h-12 m-2 rounded-full " + (showCreateChat ? 'bg-orange-400' : 'bg-green-400').toString()}
        onClick={handleClick}
        >
            {showCreateChat ? 'Close' : 'Add'}
        </button>
    )
}

export function ChatCreationWindow({chats, setChats, setShowCreateChat, currentUser }) {
    return (
    <div className='w-full h-full backdrop-blur-2xl flex flex-col items-center justify-center'>
        <div className='bg-darkgray-800 border-2 border-green-400 p-5 rounded-2xl flex flex-col \
        items-center'>
            <h1 className="text-white text-xl mb-2">Create a new chat</h1>
            <ChatCreationForm chats={chats} setChats={setChats} setShowCreateChat={setShowCreateChat} currentUser={currentUser}/>
        </div>
    </div>
    )
}

function ChatCreationForm({ chats, setChats, setShowCreateChat, currentUser }) {
    const [name, setName] = useState('')
    const [url, setUrl] = useState('')
    const [message, setMessage] = useState({
        enabled: false,
        level: 'warning',
        message: 'Idle'
    })

    function handleSubmit(event) {
        event.preventDefault()
        setMessage({level: 'warning', enabled: true, message: 'Validating...'})
        const name = event.target.name.value
        const url = event.target.url.value
        if (!validateSemiStrict(name)) {setMessage({
            level: 'failure', enabled: true,
            message: 'Name contains forbidden characters'
        }); return}
        setMessage({level: 'waring', enabled: true, message: 'Sending to server...'})
        createChat(name, url, chats, setChats, setMessage, setShowCreateChat, currentUser)
        setName('')
        setUrl('')
        
    }

    let active = name !== '' && validateSemiStrict(name)

    return (
        <form
        onSubmit={(event) => handleSubmit(event)}
        className="flex flex-col items-start w-min"
        >   
            <FormMessage state={message}/>
            <ChatFormInputField
            name={'name'} placeholder={`Enter a new chat's name`}
            length={32} value={name} setValue={setName}/>
            <ChatFormInputField
            name={'url'} placeholder={`(optional) link to an image`}
            length={1024} value={url} setValue={setUrl}/>

            <ChatCreateSubmitButton active={active} />
        </form>
    )
}

function ChatFormInputField({ name, placeholder, length, value, setValue }) {
    return (
        <input
        className="bg-darkgray-400 h-12 w-64 text-white rounded-lg p-1 m-1"
        onInput={(e) => setValue(e.target.value)}
        name={name}
        placeholder={placeholder}
        value={value}
        maxLength={length}
        type="text"
        />
    )
}


function ChatCreateSubmitButton({ active }) {

    return (
        <button
        type="submit"
        className={"text-white text-lg bg-darkgray-800 self-center p-1 mt-2 rounded-lg border-2 " + (active ? 'border-blue-400' : 'border-red-600').toString()}
        disabled={!active}
        >
            Create
        </button>
    )
}

function FormMessage({ state }) {
    let color = ' bg-white'
    switch (state.level) {
        case 'failure': color = ' bg-red-400'; break
        case 'warning': color = ' bg-orange-400'; break
        case 'success': color = ' bg-green-400'; break
        default: color = ' bg-white'; break
    }
    const res = state.enabled ? (
        <div className={"self-center rounded-lg p-1 text-lg text-center" + color}>
            {state.message}
        </div>
    ) : ''

    return res
}