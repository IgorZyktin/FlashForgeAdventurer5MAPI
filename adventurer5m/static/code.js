const DEBUG = true;

const intervals = {
    loop: 500,
    info: 30000,
    status: 15000,
    progress: 5000,
    temperature: 5000,
    position: 10000,
}

const nextCheck = {
    info: 0,
    status: 0,
    progress: 0,
    temperature: 0,
    position: 0,
}

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))


async function eventLoop(endpoints) {
    // main loop
    while (true) {
        await sleep(intervals['loop'])
        let now = Date.now()

        if (nextCheck['info'] < now) {
            if (await updateValues('info', endpoints['info'])) {
                nextCheck['info'] = now + 9999999999.0
            } else {
                nextCheck['info'] = now + intervals['info']
                continue
            }
        }

        if (nextCheck['temperature'] < now) {
            if (await updateValues('temperature', endpoints['temperature'])) {
                nextCheck['temperature'] = now + intervals['temperature']
            } else {
                continue
            }
        }

        if (nextCheck['progress'] < now) {
            if (await updateValues('progress', endpoints['progress'])) {
                nextCheck['progress'] = now + intervals['progress']
            } else {
                continue
            }
        }

        if (nextCheck['status'] < now) {
            if (await updateValues('status', endpoints['status'])) {
                nextCheck['status'] = now + intervals['status']
            } else {
                continue
            }
        }

        if (nextCheck['position'] < now) {
            if (await updateValues('position', endpoints['position'])) {
                nextCheck['position'] = now + intervals['position']
            }
        }
    }
}

async function updateValues(element, url) {
    // perform request and alter text values corresponding to response
    const parent = document.getElementById(element);

    try {
        if (DEBUG) {
            console.log(`Asking ${url}`)
        }

        const response = await fetch(url);
        let payload

        try {
            payload = await response.json();
            if (DEBUG) {
                console.log(`Got response: ${JSON.stringify(payload)}`)
            }
        } catch (error) {
            console.log(`Got error: ${error} for response ${response}`)
            parent.style.backgroundColor = 'red'
            return false
        }

        if (response.status !== 200) {
            console.log(`Got error: ${payload['error']}`)
            parent.style.backgroundColor = 'red'
            return false
        }

        for (const [key, value] of Object.entries(payload)) {
            try {
                const elem = document.getElementById(key);
                elem.textContent = String(value);
            } catch (error) {
                parent.style.backgroundColor = 'yellow'
                console.log(`Failed to set ${key} --> ${value}`)
            }
        }
    } catch (error) {
        console.log(`Got error: ${error}`)
        parent.style.backgroundColor = 'red'
        return false
    }

    parent.style.backgroundColor = ''
    return true
}
