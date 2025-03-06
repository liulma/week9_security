import logging
import paho.mqtt.client as mqtt
import json
import pprint
from azure.eventhub import EventHubProducerClient, EventData
from config import config

# Topic parts (https://digitransit.fi/en/developers/apis/4-realtime-api/vehicle-positions/high-frequency-positioning/)
topic_parts = ["prefix", "version", "journey_type", "temporal_type", "event_type", "transport_mode", "operator_id",
               "vehicle_number", "route_id", "direction_id", "headsign", "start_time", "next_stop", "geohash_level",
               "geohash", "sid"]


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/hfp/v2/journey/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Try to parse the payload as JSON
    payload = msg.payload
    try:
        payload = json.loads(payload)
    except json.decoder.JSONDecodeError:
        logging.warning("JSON Decoding error")
    # Parse the topic
    topic = msg.topic.split("/")[1:]
    topic_parsed = dict(zip(topic_parts, topic))
    # Construct the Event Hub Event
    event_body = {"topic": topic_parsed, "payload": payload}
    event_data = EventData(json.dumps(event_body))
    producer.send_event(event_data)
    #print(msg.topic + " " + str(msg.payload))


# Setup logging
logging.basicConfig(level=logging.INFO)
# Setup Azure Event Hub connection
db_config = config()
connection_string = db_config['connection-string']
eventhub_name = db_config['eventhub-name']
producer = EventHubProducerClient.from_connection_string(conn_str=connection_string, eventhub_name=eventhub_name)
# Setup MQTT Client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.enable_logger(logging.root)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.tls_set()

# Connect to the MQTT broker
mqttc.connect("mqtt.hsl.fi", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()