const DEBUG = true;
const FAST_UPDATE = 3000;
const SLOW_UPDATE = 15000;

let intervals = {
    loop: 500,
    info: 5000,
    status: 10000,
    progress: FAST_UPDATE,
    temperature: FAST_UPDATE,
}

let nextCheck = {
    info: 0,
    status: 0,
    progress: 0,
    temperature: 0,
}

const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

function debug(text) {
    // optionally print
    if (DEBUG) {
        console.log(text)
    }
}

async function eventLoop(endpoints) {
    // main loop
    while (true) {
        await sleep(intervals['loop'])
        let now = Date.now()

        if (nextCheck['info'] < now) {
            // update it only once
            if (await updateInfo(endpoints['info'])) {
                nextCheck['info'] = now + 9999999999.0
            } else {
                nextCheck['info'] = now + intervals['info']
            }
        }

        if (nextCheck['temperature'] < now) {
            await updateTemperature(endpoints['temperature'])
            nextCheck['temperature'] = now + intervals['temperature']
        }

        if (nextCheck['progress'] < now) {
            await updateProgress(endpoints['progress'])
            nextCheck['progress'] = now + intervals['progress']
        }

        if (nextCheck['status'] < now) {
            await updateStatus(endpoints['status'])
            nextCheck['status'] = now + intervals['status']
        }
    }
}

async function updateInfo(url) {
    // get printer info and update document caption
    let info = await doRequest(url)

    if (info === null) {
        return false
    }

    document.title = info['machine_name'];
    return true
}

async function updateTemperature(url) {
    // request data + alter progress bars
    let failed = false
    let temp_info = await doRequest(url)

    if (temp_info === null) {
        temp_info = {
            t0_current: '???',
            t0_target: '???',
            bed_t_current: '???',
            bed_t_target: '???',
        }
        failed = true
    }

    rewriteText(
        [
            't0_current',
            't0_target',
            'bed_t_current',
            'bed_t_target',
        ],
        temp_info,
    )

    let progress_e = document.getElementById('progress_extruder_t')
    let progress_b = document.getElementById('progress_bed_t')

    if (failed) {
        progress_e.value = '0'
        progress_e.max = '0'
        progress_b.value = '0'
        progress_b.max = '0'
    } else {
        progress_e.value = temp_info['t0_current']
        progress_e.max = temp_info['t0_target']
        progress_b.value = temp_info['bed_t_current']
        progress_b.max = temp_info['bed_t_target']
    }
}

async function updateProgress(url) {
    // request data + alter progress bars
    let failed = false
    let progress_info = await doRequest(url)

    if (progress_info === null) {
        progress_info = {
            layer_current: '???',
            layer_target: '???',
            byte_current: '???',
        }
        failed = true
    }

    rewriteText(
        [
            'layer_current',
            'layer_target',
            'byte_current',
        ],
        progress_info,
    )

    let progress_l = document.getElementById('progress_layer')
    let progress_p = document.getElementById('progress_percent')

    if (failed) {
        progress_l.value = '0'
        progress_l.max = '0'
        progress_p.value = '0'
        progress_p.max = '0'
    } else {
        progress_l.value = progress_info['layer_current']
        progress_l.max = progress_info['layer_target']
        progress_p.value = progress_info['byte_current']
        progress_p.max = '100'
    }
}

async function updateStatus(url) {
    // store info about status and current file name
    let status_info = await doRequest(url)

    if (status_info === null) {
        status_info = {
            machine_status: '???',
            move_mode: '???',
            current_file: '???',
        }
    }

    rewriteText(
        [
            'machine_status',
            'move_mode',
            'current_file',
        ],
        status_info,
    )

    if (status_info['machine_status'] === 'READY') {
        intervals['progress'] = SLOW_UPDATE
        intervals['temperature'] = SLOW_UPDATE
    } else {
        intervals['progress'] = FAST_UPDATE
        intervals['temperature'] = FAST_UPDATE
    }
}

function rewriteText(ids, infoMap) {
    // update elements with given ids using info from given map
    for (const eachId of ids) {
        try {
            let element = document.getElementById(eachId)
            element.textContent = infoMap[eachId]
        } catch (error) {
            console.log(`Failed to set ${eachId}`)
        }
    }
}

async function doRequest(url) {
    // perform request and return JSON result
    let payload = null

    try {
        debug(`Asking ${url}`)
        const response = await fetch(url);

        try {
            payload = await response.json();
            debug(`Got response: ${JSON.stringify(payload)}`)
        } catch (error) {
            console.log(`Got error: ${error} for response ${response}`)
            return null
        }

        if (response.status !== 200) {
            console.log(`Got error: ${payload['error']}`)
            return null
        }
    } catch (error) {
        console.log(`Got error: ${error}`)
        return null
    }

    return payload
}
