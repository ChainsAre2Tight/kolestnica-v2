

export default function Message({ message, currentUser, hidePFP, hideAuthor, context, setContext }) {

  const isSent = message.author.id === currentUser.id ? true : false
  if (isSent) {hideAuthor=true; hidePFP=true}
  const containerClasses = 'message-container pl-9 mb-1 relative max-w-full w-fit' + (isSent ? ' self-end' : '').toString()
  const clockClasses = 'message-time text-gray-400 text-xs inline w-fit' + (isSent ? ' self-end' : '').toString()

  const author = !hideAuthor ? <div className='text-blue-600 text-xs w-fit'>{message.author.alias}</div> : ''
  const image = !hidePFP ? <
    img className="author-image w-8 h-8 rounded-full absolute bottom-0 left-0"
    src={message.author.url}
    alt="PFP"
  /> : ''

  const date = new Date(message.timestamp * 1000)
  
  function convert_unix_to_hh_mm() {
    const hours = date.getHours()
    const minutes = '0' + date.getMinutes()
    return hours + ':' + minutes.slice(-2)
  }

  function handleClick(event) {
    const rect = document.getElementById('chatbar').getBoundingClientRect()
    const enabled = context.message.id !== message.id || context.enabled
    const position = {
      'x': Math.floor(event.clientX - rect.left),
      'y': Math.floor(event.clientY - rect.top)
    }
    setContext({
      'enabled': enabled,
      'position': position,
      'message': message
    })
  }

  return (
    <li
    className='w-full h-fit-content flex flex-col max-w-2xl relative'
    key={message.id}
    onClick={(e) => handleClick(e)}
    >
      <div className={containerClasses}>
        <div className='message-bubble p-1 rounded-lg bg-darkgray-400 flex flex-col'>
          {author}
          {image}
          <div className='text-white break-words inline whitespace-pre-line'>
            {message.body}
          </div>
          <div className={clockClasses}>
            {convert_unix_to_hh_mm()}
          </div>
        </div>
      </div>
    </li>
  )
}

export function LastMessage({message, currentUser }) {
  const displayAlias = message.author.id === currentUser.id ? 'You' : message.author.alias
  return (
    <>
      <span>{displayAlias}: </span>
      <span>{message.body}</span>
    </>
  )
}