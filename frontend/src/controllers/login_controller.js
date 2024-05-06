import { MD5 } from "crypto-js";
import { HOST } from "../config";
import { redirect_to_app, store_access_token } from "../shared/utils";
import get_fingerprint from "../shared/fingerprint";

export async function processLogin(login, password, setMessage) {
    const pwdh = MD5(password).toString()
    const fingerprint = await get_fingerprint()
    try {
        const [code, content] = await sendLogin(login, pwdh, fingerprint)
        console.log(content)
        if (code === 404) {
            await setMessage('Invalid username or password')
        }
        else if (code === 201) {
            await setMessage('Logged in')
            store_access_token(content)
            setTimeout(() => {
                redirect_to_app()
            }, 1000)
        }
    } catch (error) {
        setMessage('unknown error')
        console.log(error)
    }
}

async function sendLogin(login, pwdh, fingerprint) {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/users/current/sessions/`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                credentials: 'include',
                body: JSON.stringify({
                    login: login,
                    pwdh: pwdh,
                    fingerprint: fingerprint
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