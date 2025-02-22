import paho.mqtt.client as mqtt
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from threading import Lock
import time
from image_manager import ImageManager
from api_client import APIClient

class MatrixController:
    def __init__(self, api_client: APIClient, image_manager: ImageManager, config: Config):
        self.api_client = api_client
        self.image_manager = image_manager
        self.config = config
        self.matrix = None
        self.matrix_lock = Lock()
        self.brightness = 20
        self.mqtt_client = self._setup_mqtt()
        self.setup_matrix()

    def _setup_mqtt(self) -> mqtt.Client:
        client = mqtt.Client()
        client.on_connect = self._on_connect
        client.on_message = self._on_message

        try:
            client.connect(self.config.mqtt_broker, self.config.mqtt_port, 60)
            client.loop_start()
        except Exception as e:
            print(f"MQTT connection failed: {e}")

        return client

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            client.subscribe(self.config.mqtt_topic)
        else:
            print(f"Failed to connect to MQTT broker: {rc}")

    def _on_message(self, client, userdata, message):
        try:
            self.brightness = int(float(message.payload.decode()))
            print(f"Brightness updated to: {self.brightness}")
        except ValueError:
            print("Invalid brightness value received")

    def setup_matrix(self):
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat-pwm'
        options.brightness = self.brightness
        self.matrix = RGBMatrix(options=options)

    def display_image(self, image):
        if not image or not self.matrix:
            return

        with self.matrix_lock:
            try:
                self.matrix.brightness = self.brightness
                self.matrix.SetImage(image.convert('RGB'))
            except Exception as e:
                print(f"Failed to display image: {e}")
                self.matrix.Clear()
