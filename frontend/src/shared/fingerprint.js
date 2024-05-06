import FingerprintJS from '@fingerprintjs/fingerprintjs'

// Initialize an agent at application startup.
const fpPromise = FingerprintJS.load()

export default async function get_fingerprint() {
    const fp = await fpPromise
    const result = await fp.get()
    console.log(result.visitorId)
    return result.visitorId
}