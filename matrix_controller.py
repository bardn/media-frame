import paho.mqtt.client as mqtt
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from threading import Lock
import time
from image_manager import ImageManager
from api_client import APIClient

class MatrixController:
    def __init__(self, api_client: APIClient = None, image_manager: ImageManager = None, config: Config = None):
        self.api_client = api_client
        self.image_manager = image_manager if image_manager else ImageManager()
        self.config = config if config else Config()
        self.matrix = None
        self.matrix_lock = Lock()
        self.brightness = 20

        # Check if MQTT should be used
        self.use_mqtt = hasattr(self.config, "mqtt_broker") and hasattr(self.config, "mqtt_port")

        if self.use_mqtt:
            self.mqtt_client = self._setup_mqtt()
        else:
            print("MQTT not enabled, using default brightness.")

        self.setup_matrix()

    def setup_matrix(self):
        """Initialize the LED matrix with given configurations."""
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat-pwm'
        options.brightness = self.brightness  
        self.matrix = RGBMatrix(options=options)

    def fetch_api_image(self):
        """Try fetching an image from the API (Trakt, Spotify, etc.), or return None."""
        if not self.api_client:
            return None  # No API configured

        try:
            image_url = self.api_client.get_current_media_image()
            if image_url:
                return self.image_manager.fetch_image(image_url)
        except Exception as e:
            print(f"Error fetching image from API: {e}")

        return None  # Return None if fetching fails

    def display_image(self, image=None):
        """Display an image, or fallback to clock if needed."""
        if not image:
            image = self.image_manager.generate_clock_image()  # Default to clock if no image

        with self.matrix_lock:
            try:
                image = image.convert('RGB')  # Ensure proper format
                self.matrix.brightness = self.brightness
                self.matrix.SetImage(image)
            except Exception as e:
                print(f"Failed to display image: {e}")
                self.matrix.Clear()
