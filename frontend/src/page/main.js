import Chat from '../entities/chat.js'
import { current_user } from '../data/users.js'
import ChatSelector from '../entities/chatselector.js'
import { useEffect, useState } from 'react';
import App from '../shared/App.js';
import validate_session from '../controllers/session_controller.js';
import { addChat, getChats, recieveChatChange } from '../controllers/chat_controller.js';
import getCurrentUser from '../controllers/user_controller.js';
import { ChatCreationWindow, ChatCreatorButton } from '../entities/chatCreator.js';
import { socket } from '../controllers/socket.js';
import { recieveMessage } from '../controllers/message_controller.js';
import { updateMembers } from '../controllers/member_controller.js';

export default function MainApp() {

  const [currentUser, setCurrentUser] = useState(current_user)
  const [chats, setChats] = useState([])
  const [chat, setChat] = useState('none')
  const [loaded, setLoaded] = useState(false)

  let connection_attempts = 3

  async function handleLoad() {
      if (loaded) {return}
      await validate_session()
      await getChats(setChats)
      await getCurrentUser(setCurrentUser)
      await socket.connect(':443')
      setLoaded(true)
    }

  if (document.readyState !== 'complete' && !loaded) {
    window.addEventListener('load', handleLoad)
  } else {
    handleLoad()
  }


  useEffect(() => {

    function addMessage(data) {
      console.log(`New message in chat ${data.chat_id}/${data.message_id} `)
      recieveMessage(data.chat_id, data.message_id, chat, chats, setChat, setChats)
      console.log(chat)
    }

    async function onDisconnect() {
      if (connection_attempts > 0) {
        connection_attempts -= 1
        await validate_session()
        await socket.connect(':443')
      } else {
        console.log('Ran out of WS connection attempts')
      }
    }

    function onChangeChatMembers(data) {
      console.log(`Need to update members of chat ${data.chat_id}`)
      updateMembers(data.chat_id, chat, chats, setChat, setChats)
    }

    function onAddChat(data) {
      console.log(`There is a new chat with id ${data.chat_id}`)
      addChat(data.chat_id, chats, setChats)
    }

    function onUpdateChat(data) {
      console.log(`Chat ${data.chat_id} is due to be updated`)
      recieveChatChange(data.chat_id, chat, chats, setChat, setChats)
    }

    socket.on('add-message', addMessage)
    socket.on('disconnect', onDisconnect)
    socket.on('update-members', onChangeChatMembers)
    socket.on('add-chat', onAddChat)
    socket.on('update-chat', onUpdateChat)

    return () => {
      socket.off('add-message', addMessage)
      socket.off('disconnect', onDisconnect)
      socket.off('update-members', onChangeChatMembers)
      socket.off('add-chat', onAddChat)
      socket.off('update-chat', onUpdateChat)
    }
  })

  

  return (
    <App>
      <Interface
      chats={chats}
      chat={chat}
      setChat={setChat}
      currentUser={currentUser}
      setChats={setChats}
      />
    </App>
  )
}

export function Interface({ chats, chat, setChat, currentUser, setChats }) {
  const [showCreateChat, setShowCreateChat] = useState(false)

  return (
    <div className='h-screen w-screen'>
      <div className='md:container w-full mx-auto h-full flex flex-row'>
        <NavBar
        currentUser={currentUser}
        chats={chats}
        setChat={setChat}
        showCreateChat={showCreateChat}
        setShowCreateChat={setShowCreateChat}
        />
        {showCreateChat ? <ChatCreationWindow
          chats={chats}
          setChats={setChats}
          setShowCreateChat={setShowCreateChat}
          currentUser={currentUser}
          /> : chat !== 'none' ? <ChatBar
          currentUser={currentUser}
          chat={chat}
          setChat={setChat}
          chats={chats}
          setChats={setChats}
          /> : <NoChatSelected />}
      </div>
    </div>
  )
}

function ChatBar({ currentUser, chat, setChat, chats, setChats }) {
  return (
    <div className='w-full backdrop-blur-2xl h-screen w-11/12 lg:w-9/12'>
      <Chat chat={chat} currentUser={currentUser} setChat={setChat} chats={chats} setChats={setChats}/>
    </div>
  )
}

function NoChatSelected() {
  return (
    <div className='w-full h-full backdrop-blur-2xl flex flex-col items-center justify-center'>
      <div className='bg-darkgray-800 p-10 text-white text-2xl rounded-2xl text-center'>
        No chat is selected. Create a new chat or ask other users to add you to an existing one
      </div>
    </div>
  )
}



function NavBarHeader({ currentUser, setChatSearchValue }) {
  return (
    <div className='h-12 p-2 flex flex-row items-center justify-center overflow-hidden bg-darkgray-800 w-full'>
      <NavBarPFP currentUser={currentUser}/>
      <NavBarSearch setChatSearchValue={setChatSearchValue}/>
    </div>
  )
}

function NavBarPFP({ currentUser }) {
  return (
    <button className='h-10 w-10 min-w-10 rounded-full'>
      <img
      alt='MYPFP'
      src={currentUser.url}
      className='h-full w-full rounded-full'
      />
    </button>
  )
}

function NavBarSearch({ setChatSearchValue }) {
  function handleInput(e) {
    setChatSearchValue(e.target.value)
  }

  return (
    <div className='lg:flex hidden bg-white grow rounded-lg ml-1 flex-row items-center'>
      <img src='https://www.freeiconspng.com/uploads/magnifying-glass-icon-4.png' alt='mfg' className='w-8 h-8' />
      <input className='h-8 grow bg-transparent pr-2' placeholder='Поиск...' onInput={(e) => {handleInput(e)}}>
        
      </input>
    </div>
  )
}

function ChatsSelectorsContainer({ chats, currentUser, setChat, showCreateChat, setShowCreateChat }) {
  let chats_ = chats.map(chat => 
    <ChatSelector chat={chat} currentUser={currentUser} setChat={setChat} />
  )
  return (
    <>
      <ol className='bg-darkgray-800 border-gray-600 grow flex flex-col items-stretch overflow-y-auto scrollbar-thin pr-1 pl-1 w-full overflow-x-hidden'>
        {chats_}
      </ol>
      <ChatCreatorButton showCreateChat={showCreateChat} setShowCreateChat={setShowCreateChat}/>
    </>
  )
}



function NavBar({ currentUser, setChat, chats, showCreateChat, setShowCreateChat }) {
  const [chatSearchValue, setChatSearchValue] = useState('')

  const showChats = chatSearchValue === '' ? chats : chats.filter(obj => obj.name.toLowerCase().includes(chatSearchValue))

  return (
    <div className='bg-white h-screen w-1/12 lg:w-3/12 flex flex-col relative min-w-16'>
      <NavBarHeader currentUser={currentUser} setChatSearchValue={setChatSearchValue}/>
      <ChatsSelectorsContainer
      chats={showChats}
      currentUser={currentUser}
      setChat={setChat}
      showCreateChat={showCreateChat}
      setShowCreateChat={setShowCreateChat}
      />
    </div>
  )
}

