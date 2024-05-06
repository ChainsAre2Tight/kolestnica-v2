const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

export function compare_dates(timestamp_one, timestamp_two) {
    const date_one = new Date(timestamp_one * 1000)
    const date_two = new Date(timestamp_two * 1000)
    return date_one.toDateString() === date_two.toDateString()
}

export function date_string(timestamp) {
    const date = new Date(timestamp * 1000)
    const day = date.getDate().toString()
        
    let appendix = 'th'
    if (day % 10 === 1) {
        appendix = 'st'
    }
    else if (day % 10 === 2) {
        appendix = 'nd'
    }
    else if (day % 10 === 3) {
        appendix = 'rd'
    }

    const month = months[date.getMonth()]
    return `${month}, ${day}${appendix}`
}

export function disect_string(input) {
    // Replace <div>(my data)</div> with \n
    var newText = input.replace(/<div>(.*?)<\/div>/g, '$1\n');

    // Remove <br> tags
    newText = newText.replace(/<br>/g, '');
    return newText
}

export function redirect_to_login() {
    window.location.replace('/login')
}

export function redirect_to_app() {
    window.location.replace('/app')
}

export function store_access_token(content) {
    const tokens = content.data.tokens.access
    window.localStorage.setItem('access', tokens.value)
    window.localStorage.setItem('expiry', tokens.expiry)
}