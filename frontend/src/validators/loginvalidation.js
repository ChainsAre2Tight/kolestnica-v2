
function validateString(string, forbiddenSymbols) {
    let result = true
    for (const symbol of forbiddenSymbols) {
        if (string.indexOf(symbol) > -1) {
            result = false
            break
        }
    }
    return result
}

export function validateStrict(string) {
    const forbiddenSymbols = '@!#$%^&*()-+={}[]\'"\\/<>,.| '
    return validateString(string, forbiddenSymbols)
}

export function validateSemiStrict(string) {
    const forbiddenSymbols = '@!#$%^&*()+={}[]\'"\\/<>,.|'
    return validateString(string, forbiddenSymbols)
}