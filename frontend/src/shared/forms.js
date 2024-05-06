

export function FormBox({ name, message, children }) {
    return (
        <div className="w-screen h-screen flex flex-col items-center justify-center text-lg">
            <div className="bg-darkgray-800 flex flex-col items-center p-5 rounded-xl w-fit">
                <h1 className="text-white text-xl mb-5">
                    {name}
                </h1>
                <FormMessage message={message}/>
                {children}
            </div>
        </div>
    )
}

export function InputField({ name, placeholder, type }) {
    return (
    <input
    className="m-1 text-white bg-black"
    name={name}
    placeholder={placeholder}
    required
    type={type}
    />)
}

function FormMessage({ message }) {
    let messageBox = (
        <div className="bg-red-400 p-1 m-2">
            {message}
        </div>
    )
    if (message === '') {
        messageBox = ''
    }

    return messageBox
}