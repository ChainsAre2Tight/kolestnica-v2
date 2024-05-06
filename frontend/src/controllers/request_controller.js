import validate_session from "./session_controller"

export default function validateBeforeRequest(requestFunction) {
    return async function(...args) {
        await validate_session()
        const [code, content] = await requestFunction(...args)
        return [code, content]
    }
}