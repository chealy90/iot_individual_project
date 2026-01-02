let pubnub
let appChannel = "IotTempSensorChannel"


const setupPubNub = () => {
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
        }
    })

    pubnub.onMessage = (messageEvent) => {
        handleMessage(messageEvent.message)
    }
    subscription.subscribe()
}

const handleMessage = message => {
    document.write(message)
}

