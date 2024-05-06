import App from "../shared/App";
import { useState } from "react";
import {  validateStrict } from "../validators/loginvalidation";
import { InputField, FormBox } from "../shared/forms";
import { processLogin } from "../controllers/login_controller";

export default function LoginApp() {
    const [message, setMessage] = useState('')

    return (
        <App>
            <FormBox name='Login' message={message}>
                <LoginForm setMessage={setMessage}/>
            </FormBox>
        </App>
    )
}

function LoginForm({ setMessage }) {

    function handleSubmit(e) {
        e.preventDefault()
        setMessage('validating')
        const login = e.target.elements.login.value
        const password = e.target.elements.password.value

        if (!validateStrict(login)) {
            setMessage('Login contains forbidden characters')
            return
        }
        
        setMessage('sending to server...')
        processLogin(login, password, setMessage)
    }

    return (
        <form
        className="w-full flex flex-col items-center"
        onSubmit={(e) => handleSubmit(e)}
        >
            <div className="bg-darkgray-400 flex flex-col rounded-lg p-1 w-full">
                <InputField name={'login'} placeholder={"Enter your login"} type={'text'} />
                <InputField name={"password"} placeholder={"Enter your password"} type={'password'} />
            </div>
            <button
            className="text-white text-xl rounded-lg p-2 bg-blue-800 mt-3"
            type="submit"
            >
                Login
            </button>

            <div className="text-white mt-2">
                <span>Don't have an account? </span>
                <a href="/register" className="text-blue-400">Register</a>
            </div>
        </form>
    )
}