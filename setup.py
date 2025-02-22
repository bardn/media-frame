import time
from token_manager import TokenManager
from config import Config

def setup():
    config = Config()

    # Get Trakt credentials and authorization code
    if input("Do you want to use Trakt? (y/n): ").lower() == "y":
        config.trakt_client_id = input("Enter your Trakt Client ID: ").strip()
        config.trakt_client_secret = input("Enter your Trakt Client Secret: ").strip()
        config.redirect_uri = input("Enter your Trakt Redirect URI: ").strip()

        # Generate the URL and wait for user input for the code
        trakt_url = f"https://trakt.tv/oauth/authorize?client_id={config.trakt_client_id}&redirect_uri={config.redirect_uri}&response_type=code"
        print(f"Please open this URL to authorize: {trakt_url}")
        authorization_code = TokenManager(config).get_authorization_code("Trakt")
        if not TokenManager(config).generate_trakt_token(authorization_code):
            print("Trakt token generation failed. Please check your credentials.")
            return

    # Get Spotify credentials and authorization code
    if input("Do you want to use Spotify? (y/n): ").lower() == "y":
        config.spotify_client_id = input("Enter your Spotify Client ID: ").strip()
        config.spotify_client_secret = input("Enter your Spotify Client Secret: ").strip()
        config.redirect_uri = input("Enter your Spotify Redirect URI: ").strip()

        # Generate the URL and wait for user input for the code
        spotify_url = f"https://accounts.spotify.com/authorize?client_id={config.spotify_client_id}&redirect_uri={config.redirect_uri}&response_type=code"
        print(f"Please open this URL to authorize: {spotify_url}")
        authorization_code = TokenManager(config).get_authorization_code("Spotify")
        if not TokenManager(config).generate_spotify_token(authorization_code):
            print("Spotify token generation failed. Please check your credentials.")
            return

    print("All necessary .env values have been written.")
