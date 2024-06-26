import { encrypt, decrypt } from "xtea"

import { Buffer } from 'buffer';

// @ts-ignore
window.Buffer = Buffer;


export function encipher_message(message, key) {
    return message
    const plaintext = new Buffer(message, 'utf8');
    const key_ = new Buffer(key, 'utf-8');
    const ciphertext = encrypt(plaintext, key_).toString('hex')
    return ciphertext
}

export function decipher_message(ciphertext, key) {
    return ciphertext
    const ciphertext_ = new Buffer(ciphertext, 'hex')
    const key_ = new Buffer(key, 'utf-8');
    const message = decrypt(ciphertext_, key_).toString()
    return message
}
