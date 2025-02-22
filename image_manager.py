from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

class ImageManager:
    def __init__(self, font_path: str = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        self.font_path = font_path

    def fetch_image(self, url: str) -> Image.Image:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"Failed to fetch image: {e}")
            return None

    def add_clock_overlay(self, image: Image.Image) -> Image.Image:
        try:
            font = ImageFont.truetype(self.font_path, 18)
        except IOError:
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(image)
        time_str = time.strftime('%H:%M:%S')
        draw.text((10, 10), time_str, font=font, fill="white")
        return image
