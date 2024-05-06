import App from "../shared/App";
import { validateStrict } from "../validators/loginvalidation";
import { processRegister } from "../controllers/register_controller";
import { FormBox, InputField } from "../shared/forms";
import { useState } from "react"

export default function RegisterApp() {
    const [message, setMessage] = useState('')

    return (
        <App>
            <FormBox name='Register' message={message}>
                <RegisterForm setMessage={setMessage}/>
            </FormBox>
        </App>
    )
}

function RegisterForm({ setMessage }) {

    function handleSubmit(e) {
        e.preventDefault()
        setMessage('validating')
        const login = e.target.elements.login.value
        const password = e.target.elements.password.value
        const conf_password = e.target.confirmPassword.value
        const username = e.target.username.value

        if (password !== conf_password) {
            setMessage('Passwords do not match')
            return
        }

        if (!validateStrict(login)) {
            setMessage('Login contains forbidden characters')
            return
        }

        if (!validateStrict(username)) {
            setMessage('Username contains forbidden characters')
            return
        }
        
        setMessage('sending to server...')
        processRegister(login, password, username, setMessage)
    }

    return (
        <form
        className="w-full flex flex-col items-center"
        onSubmit={(e) => handleSubmit(e)}
        >
            <div className="bg-darkgray-400 flex flex-col rounded-lg p-1 w-full">
                <InputField name={'login'} placeholder={"Enter your login"} type={'text'} />
                <InputField name={"password"} placeholder={"Enter your password"} type={'password'} />
                <InputField name={'confirmPassword'} placeholder={"Confirm your password"} type={'password'} />
                <InputField name={"username"} placeholder={"Enter your username"} type={'text'} />
            </div>
            <button
            className="text-white text-xl rounded-lg p-2 bg-blue-800 mt-3"
            type="submit"
            >
                Register
            </button>
            <div className="text-white mt-2">
                <span>Already have an account? </span>
                <a href="/login" className="text-blue-400">Log in</a>
            </div>
        </form>
    )
}