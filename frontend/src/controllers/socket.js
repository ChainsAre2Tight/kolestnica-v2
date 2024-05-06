import { HOST } from "../config"

const io = require('socket.io-client');

export const socket = io(`${HOST}`, {
    query: {
        access_token: window.localStorage.getItem('access')
    },
    reconnectionDelayMax: 10000,
    autoConnect: false
})

socket.on('bad-token', () => (console.log('Socket connection refused due to a bad token')))
socket.on('expired', () => (console.log('Socket connection refused due to an expired token')))