import { HOST } from "../config"
import validateBeforeRequest from "./request_controller"

export default async function getCurrentUser(setUser) {
    const decoratedRequest = validateBeforeRequest(sendGetCurrentUserRequest)
    const [code, content] = await decoratedRequest()
    if (code === 200) {
        const raw_user = content.data.User
        const user = {
            id: raw_user.id,
            url: raw_user.image_href,
            name: raw_user.username,
            alias: raw_user.alias
        }
        await setUser(user)
    } else {
        console.log(code, content)
    }
}

async function sendGetCurrentUserRequest() {
    try {
        const rawResponse = await fetch(
            `${HOST}/api/users/current`,
            {
                headers:{
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': window.localStorage.getItem('access'),
                },
                method: 'GET',
            }
        )
        const content = await rawResponse.json()
        return [rawResponse.status, content]
    } catch (error) {
        console.log(error)
    }
}