from api_client import APIClient
from matrix_controller import MatrixController
from image_manager import ImageManager
from token_manager import TokenManager
from config import Config

def main():
    config = Config()

    api_client = APIClient(config)
    image_manager = ImageManager()
    token_manager = TokenManager(config)
    
    matrix_controller = MatrixController(api_client, image_manager, config)
    matrix_controller.setup_matrix()

    # Add your main loop or event-driven logic to update the display here.

if __name__ == "__main__":
    main()
