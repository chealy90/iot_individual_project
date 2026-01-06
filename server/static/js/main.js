let appChannel = "IotTempSensorChannel"
let pubnub


const DB_WRITE_INTERVAL = 1800 //write temp to db every 30 mins under normal condititions
let lastWrite = new Date()
let sensorsList



const setupPubNub = (sensors) => {
    sensorsList = sensors
    pubnub = new PubNub({
        publishKey: "pub-c-3e946942-f546-48a4-8669-04ddff6b7152",
        subscribeKey: "sub-c-f0db3e16-0d07-4cf1-967f-0fcc888bcf2f",
        userId: "web-user-" + Math.floor(Math.random() * 1000),
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
    console.log("here")
    console.log(message)
    let sensor = sensorsList.filter(sensor => sensor["device_id"] === message["device_id"])[0]

    //always write if out of range
    if (message.temperature > sensor.max_temp || message.temperature < sensor.min_temp){
        fetch("/write_to_db")
    }
    

    document.getElementById("currTemp").innerHTML = message.temperature
    
}

const write_record_to_database = (user_id, scanner_id, temp) => {
    fetch("/write_temp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user: user_id,
            scanner: scanner_id,
            temperature: temp
        })
    })
    .then(res => {
        if (!res.ok){
            console.log("Network response not ok")
        }
        window.location.reload()
    })
    .catch(err => {
        console.log(err)
    })
}

