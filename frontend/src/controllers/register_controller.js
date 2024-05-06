import { MD5 } from "crypto-js";
import { HOST } from "../config";
import { redirect_to_login } from "../shared/utils";

export async function processRegister(login, password, username, setMessage) {
    const pwdh = MD5(password).toString()
    try {
        const [code, content] = await sendRegister(login, pwdh, username)
        console.log(content)
        if (code === 409) {
            await setMessage('data collision')
        }
        else if (code === 201) {
            await setMessage('Accout created')
            setTimeout(() => redirect_to_login(), 3000)
        }
    } catch (error) {
        setMessage('unknown error')
        console.log(error)
    }
}

async function sendRegister(login, pwdh, username) {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/users/`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify({
                    username: username,
                    login: login,
                    pwdh: pwdh
                })
            }
        )
        console.log(rawResponse)

        const content = await rawResponse.json()
        console.log(rawResponse.status, content)
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}