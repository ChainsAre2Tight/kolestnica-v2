import { redirect_to_login, store_access_token } from "../shared/utils"
import { HOST } from "../config"

export default async function validate_session() {

    if (!check_access_token()) {
        console.log('refreshing')
        await refresh_tokens()
    }
    return true
}

function check_access_token() {
    const access = window.localStorage.getItem('access')
    const expiry = window.localStorage.getItem('expiry')
    if (access === null || typeof access !== 'string') {
        console.log('missing token')
        return false
    }
    if (
        expiry === null
        || isNaN(expiry)
        || !Number.isInteger(parseFloat(expiry))
    ) {
        console.log('missing expiry')
        return false
    }
    if ((expiry-10) < Date.now() / 1000) {
        console.log('expired')
        return false
    }
    return true
}

function logout() {
    window.localStorage.clear()
    redirect_to_login()
}

async function refresh_tokens() {
    // send  request to refresh tokens
    const [code, content] = await send_refresh_request()
    if (code === 401) {
        logout()
    }
    if (code === 200) {
        store_access_token(content)
    }
}

async function send_refresh_request() {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/tokens/`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                method: 'GET'
            }
        )
        const content = await rawResponse.json()
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}