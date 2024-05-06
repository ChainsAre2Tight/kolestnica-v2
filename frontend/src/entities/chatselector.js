import { LastMessage } from "./message"

export default function ChatSelector({ chat, currentUser, setChat }) {

    const lastMessage = chat.messages.length > 0 ? <div className='text-gray-400 h-6 whitespace-nowrap text-sm overflow-hidden mr-5'><LastMessage
    message={chat.messages[chat.messages.length - 1]}
    currentUser={currentUser}
    /></div> : ''

    function handleClick() {
        setChat(chat)
    }

    return (
        <button
        className='text-white h-16 flex flex-row items-start p-1 mr-0 min-w-16 w-fit lg:w-auto rounded-xl mt-2 hover:bg-gray-600 pr-2'
        onClick={handleClick}
        key={chat.id}
        >
            <img src={chat.url} className='chat-image h-12 w-12 top-2 left-2 rounded-full' alt='CHATPFP' />
            <div className="ml-2 flex flex-col items-start">
                <div className='chat-name lg:block hidden h-8 whitespace-nowrap overflow-x-hidden max-w-full'>
                    {chat.name}
                </div>
                {lastMessage}
            </div>
        </button>
    )
}