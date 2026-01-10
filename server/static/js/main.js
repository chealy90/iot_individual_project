let appChannel = "IotTempSensorChannel"
let pubnub


const DB_WRITE_INTERVAL = 1800 //write temp to db every 30 mins under normal condititions
let lastWrite = new Date()


const setupPubNub = () => {
    pubnub = new PubNub({
        publishKey: "pub-c-3e946942-f546-48a4-8669-04ddff6b7152",
        subscribeKey: "sub-c-f0db3e16-0d07-4cf1-967f-0fcc888bcf2f",
        userId: "web-user-" + Math.floor(Math.random() * 1000),
        ssl: true
    })

    const channel = pubnub.channel(appChannel)
    const subscription = channel.subscription()

    pubnub.addListener({
        status: (s) => {
            console.log("Status", s.category)
        },
        message: (messageEvent) => {
            handleMessage(messageEvent.message)
        }
    })

    subscription.subscribe()
}




const handleMessage = message => {
    //let sensor = sessionStorage["user_scanners"].filter(sensor => sensor["device_id"] === message["device_id"])[0]
    //console.log(sensor)

    /*
    //always write if out of range
    if (message.temperature > sensor.max_temp || message.temperature < sensor.min_temp){
        fetch("/write_to_db")
    }
        */
    if (message.type === "update_sensor"){
        return
    }
    document.getElementById(`currTemp_${message.device_id}`).innerHTML = message.temperature
    write_record_to_database(message.time, message.device_id, message.temperature)

    
}

const write_record_to_database = (time, scanner_id, temp) => {
    fetch("/write_temp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            time: time,
            scanner: scanner_id,
            temperature: temp
        })
    })
    .then(res => {
        if (!res.ok){
            console.log("Network response not ok")
        }
        //window.location.reload()
        console.log("ok")
    })
    .catch(err => {
        console.log(err)
    })
}

const enableEdit = (sensor) => {
    console.log(sensor)
    const editBoxHtml = `
        <form class="sensor-edit-form" action="/update_sensor" method="post">
            <input type="hidden" name="sensor_id" value="${sensor.device_id}" />

            <div class="form-row">
                <label>Device Name</label>
                <input 
                    type="text"
                    value="${sensor.device_name}"
                    name="device_name"
                    required
                />
            </div>

            <div class="form-row">
                <label>Min Temp</label>
                <input 
                    type="number"
                    value="${sensor.min_temp}"
                    name="min_temp"
                    min="-20"
                    max="60"
                    required
                />
            </div>

            <div class="form-row">
                <label>Max Temp</label>
                <input 
                    type="number"
                    value="${sensor.max_temp}"
                    name="max_temp"
                    min="-20"
                    max="60"
                    required
                />
            </div>

            <div class="form-actions">
                <button type="submit" class="save-btn">Save</button>
                <button type="button" class="discard-btn" onClick="discardChanges()">Discard</button>
            </div>
        </form>
    `;
    document.getElementById(`sensor_container_${sensor.device_id}`).innerHTML = editBoxHtml;
}


const discardChanges = () => {
    window.location.reload()
}

document.addEventListener("DOMContentLoaded", function() { setupPubNub() })





