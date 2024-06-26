import React, { useRef, useState, useEffect } from 'react'
import Message from './message.js'
import { sendMessage } from '../controllers/message_controller.js'
import ContentEditable from 'react-contenteditable'
import { date_string, compare_dates, disect_string } from '../shared/utils.js'
import { ChatEditor, ChatEditorButton } from './chatManager.js'

export default function Chat({ chat, setChat, currentUser, chats, setChats }) {
  const [showEditor, setShowEditor] = useState(false)

  return (
    <div className='dialog-container h-screen w-full flex-col justify-stretch flex max-w-full'>
      <ChatHeader chat={chat} showEditor={showEditor} setShowEditor={setShowEditor}/>
      {!showEditor ? 
        (<>
          <ChatBody chat={chat} currentUser={currentUser}/>
          <ChatInput chat={chat} setChat={setChat} currentUser={currentUser} chats={chats} setChats={setChats}/>
        </>) : <ChatEditor chat={chat} />
      }
    </div>
  )
}

function DateSeparator({ string }) {
  return (
    <li key={string} className='text-white self-center rounded-lg mb-2 mt-2'>
      <span>{string}</span>
    </li>
  )
}

function ChatBody({ chat, currentUser }) {

  const [context, setContext] = useState({
    'message': {
      'id': -1
    },
    'position': {
      'x': 0,
      'y': 0
    },
    'active': false,
  })

  const messages = []
  for (let i = 0; i < chat.messages.length; ++i) {
    let hidePFP = false
    if (
      i < chat.messages.length - 1
      && chat.messages[i+1].author.id === chat.messages[i].author.id
      && compare_dates(chat.messages[i+1].timestamp, chat.messages[i].timestamp)
    ) {
      hidePFP = true
    }
    let hideAuthor = false
    if (i > 0 && chat.messages[i-1].author.id === chat.messages[i].author.id) {
      hideAuthor = true
    }
    
    if (i === 0 || (i>1 && !compare_dates(chat.messages[i-1].timestamp, chat.messages[i].timestamp))) {
      messages.push(<DateSeparator string={date_string(chat.messages[i].timestamp)}/>)
      hideAuthor = false
      hidePFP = false
    }

    messages.push(<Message
      message={chat.messages[i]}
      currentUser={currentUser}
      hidePFP={hidePFP}
      hideAuthor={hideAuthor}
      context={context}
      setContext={setContext}
    />)
  }

  return (
    <div className='flex flex-col-reverse grow w-full overflow-hidden relative' id='chatbar'>
      <div className='scrollbar flex flex-col-reverse overflow-y-auto scrollbar-thin'>
        <ul className='flex flex-col items-center overflow-visible'>
          {messages}
        </ul>
      </div>
      {/* <MessageContext selectedMessage context={context} /> */}
    </div>
  )
}

function ChatInputField({ messageText, setSendActive }) {
  function handleChange(e) {
    if (e.target.value !== '' && e.target.value !== '<br>') {
      setSendActive(true)
    } else {
      setSendActive(false)
    }
    messageText.current = e.target.value
  }

  return (
    <ContentEditable
      className='input text-white bg-darkgray-400 h-auto grow rounded-lg p-1 scrollbar-hide overflow-y-scroll active:border-black break-all max-h-60'
      html={messageText.current}
      onChange={(e) => handleChange(e)}
    >
    </ContentEditable>
  )
}

function SendMessageButton({ currentUser, chat, setChat, messageText, sendActive, setSendActive, chats, setChats }) {
  function verify_message(messageText) {
    let result = true
    if (messageText.current === '') {
      result = false
    }
    return result
  }

  function handleSendMessage() {
    messageText.current = ''
    document.getElementsByClassName('input')[0].textContent = ''
    setSendActive(false)
  }

  function handlePress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleClick()
    }
  }

  function handleClick() {
    const verified = verify_message(messageText)
    if (verified) {
      const body = disect_string(messageText.current)
      sendMessage(body, currentUser, chat, setChat, chats, setChats)
      handleSendMessage()
    } else {
      alert('bad message') // TODO remove
    }
  }

  useEffect(() => {
    window.addEventListener("keydown", handlePress)
    return () => window.removeEventListener("keydown", handlePress)
  }, [chat])

  return (
    <button
      className={'send-message-button w-8 h-8 rounded-full self-end m-1 min-w-8' + (sendActive ? ' bg-blue-600' : ' bg-darkgray-800').toString()}
      onClick={handleClick}
      disabled={!sendActive}
    >
    </button>
  )
}
  
function ChatInput({ currentUser, chat, setChat, chats, setChats }) {
  const messageText = useRef('')
  const [sendActive, setSendActive] = useState(false)

  return (
    <div className='h-fit w-full self-center flex flex-row items-center mb-2 max-w-2xl mt-2'>
      <ChatInputField messageText={messageText} setSendActive={setSendActive}/>
      <SendMessageButton
        currentUser={currentUser}
        chat={chat}
        setChat={setChat}
        messageText={messageText}
        sendActive={sendActive}
        setSendActive={setSendActive}
        chats={chats}
        setChats={setChats}
      />
    </div>
  )
}

function ChatHeader({ chat, showEditor, setShowEditor }) {
  return (
    <button
    className='dialog-header h-12 w-full bg-darkgray-800 p-1 pl-2 flex flex-row items-center'
    onClick={() => setShowEditor(!showEditor)}
    >
      <img className='dialog-header-image w-10 h-10 rounded-full' src={chat.url} alt='CHATPFP'></img>
      <div className='ml-4 mb-1 flex flex-col items-start grow'>
        <div className='text-white'><span>{chat.name}</span></div>
        <div className='text-gray-400 text-xs'>{chat.members.length} members</div>
      </div>
      <ChatEditorButton showEditor={showEditor} setShowEditor={setShowEditor}/>
    </button>
  )
}
