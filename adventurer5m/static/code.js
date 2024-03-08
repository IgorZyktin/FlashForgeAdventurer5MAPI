const DEBUG = false;

function isObjectLike(value) {
    return Object.prototype.toString.call(value) === "[object Object]";
}

async function askAPI(url) {
    // perform request and alter text values corresponding to response
    try {
        if (DEBUG) {
            console.log(`Asking ${url}`)
        }

        const response = await fetch(url);
        const payload = await response.json();

        if (DEBUG) {
            console.log(`Got response: ${JSON.stringify(payload)}`)
        }

        if (response.status !== 200) {
            alert(payload['error'])
            clearInterval(intervalID)
            return
        }

        for (const [key, value] of Object.entries(payload)) {
            if (isObjectLike(value)) {
                for (const [sub_key, sub_value] of Object.entries(value)) {
                    maybeSet(`${key}.${sub_key}`, sub_value)
                }
            } else {
                maybeSet(key, value)
            }
        }
    } catch (error) {
        alert(error);
    }
}

function maybeSet(id, text) {
    // try setting value of the object
    try {
        const elem = document.getElementById(id);
        elem.textContent = String(text);
    } catch (error) {
        console.log(`Failed to set ${id} --> ${text}`)
    }
}
