from api_client import APIClient
from matrix_controller import MatrixController
from image_manager import ImageManager
from token_manager import TokenManager
from config import Config


import os
from dotenv import load_dotenv, set_key
from token_manager import generate_trakt_token, generate_spotify_token  # Import the functions

# Load environment variables
load_dotenv()

def check_and_generate_tokens():
    # Check if Trakt and Spotify tokens are in .env
    trakt_token = os.getenv('TRAKT_ACCESS_TOKEN')
    spotify_token = os.getenv('SPOTIFY_ACCESS_TOKEN')

    # If Trakt token is missing, prompt to generate
    if not trakt_token:
        print("Trakt token not found in .env.")
        generate_trakt_token()

    # If Spotify token is missing, prompt to generate
    if not spotify_token:
        print("Spotify token not found in .env.")
        generate_spotify_token()

def main():
    # Ensure tokens are available
    check_and_generate_tokens()
    print("Tokens are ready to use.")
    api_client = APIClient(config)
    image_manager = ImageManager()
    token_manager = TokenManager(config)
    
    matrix_controller = MatrixController(api_client, image_manager, config)
    matrix_controller.setup_matrix()
    
if __name__ == "__main__":
    main()
