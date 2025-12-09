import pytest
import threading
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "test/topic"
MESSAGE = "Hello, MQTT!"

@pytest.mark.timeout(5)
def test_mqtt_broker():
    message_received = threading.Event()
    received_payload = []

    def on_message(client, userdata, msg):
        received_payload.append(msg.payload.decode())
        message_received.set()

    subscriber = mqtt.Client(client_id="pytest_subscriber")
    subscriber.on_message = on_message
    subscriber.connect(BROKER, PORT)
    subscriber.subscribe(TOPIC)
    subscriber.loop_start()

    publisher = mqtt.Client(client_id="pytest_publisher")
    publisher.connect(BROKER, PORT)
    publisher.loop_start()

    publisher.publish(TOPIC, MESSAGE)

    # Wait for subscriber to receive message (max 3 seconds)
    message_received.wait(timeout=3)

    subscriber.loop_stop()
    publisher.loop_stop()
    subscriber.disconnect()
    publisher.disconnect()

    assert MESSAGE in received_payload
