from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from dotenv import load_dotenv
import os

load_dotenv()

pnconfig = PNConfiguration()
pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
pnconfig.uuid = os.getenv("PUBNUB_UUID")
pnconfig.ssl = True

pubnub = PubNub(pnconfig)
CHANNEL = os.getenv("PUBNUB_CHANNEL")


def publish_msg(message):
    envelope = pubnub.publish().channel(CHANNEL).message(message).sync()

    if envelope.status.is_error():
        print(f"Publish Error: {envelope.status.error_data}")
    else:
        print(f'Published with timetoken: {envelope.result.timetoken}')
