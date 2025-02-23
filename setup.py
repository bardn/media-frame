import os
from dotenv import load_dotenv, set_key
from config import Config
from token_manager import TokenManager
import re  # for extracting the code from URL

def extract_code_from_url(url: str) -> str:
    """Extract the authorization code from the URL."""
    match = re.search(r'code=([a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Authorization code not found in URL")

def update_env_and_reload(key: str, value: str):
    """Update .env, reload it, and return a fresh Config instance."""
    set_key(".env", key, value)  # Update the .env file
    load_dotenv(override=True)  # Reload environment variables
    return Config()

def setup():
    load_dotenv()  # Initial load

    print("Welcome to the Media Frame Setup!")

    # ?? Handle Trakt setup
    print("Do you want to use Trakt? (y/n): ", end="")
    use_trakt = input().strip().lower() == 'y'
    update_env_and_reload("USE_TRAKT", str(use_trakt).lower())

    if use_trakt:
        trakt_client_id = input("Enter your Trakt Client ID: ").strip()
        config = update_env_and_reload("TRAKT_CLIENT_ID", trakt_client_id)

        trakt_client_secret = input("Enter your Trakt Client Secret: ").strip()
        config = update_env_and_reload("TRAKT_CLIENT_SECRET", trakt_client_secret)

        trakt_redirect_uri = input("Enter your Trakt Redirect URI: ").strip()
        config = update_env_and_reload("TRAKT_REDIRECT_URI", trakt_redirect_uri)

        print(f"Authorize here: https://trakt.tv/oauth/authorize?client_id={config.trakt_client_id}&redirect_uri={config.trakt_redirect_uri}&response_type=code")

        # Get the authorization URL and extract the authorization code
        authorization_url = input("Enter the full URL after authorization: ").strip()
        try:
            authorization_code = extract_code_from_url(authorization_url)
            print(f"Extracted Authorization Code: {authorization_code}")

            # ?? Use the latest config with the correct redirect_uri
            token_manager = TokenManager(config)
            token_manager.generate_trakt_token(authorization_code)
        except ValueError as e:
            print(f"Error: {e}")

    # ?? Handle Spotify setup
    print("Do you want to use Spotify? (y/n): ", end="")
    use_spotify = input().strip().lower() == 'y'
    update_env_and_reload("USE_SPOTIFY", str(use_spotify).lower())

    if use_spotify:
        spotify_client_id = input("Enter your Spotify Client ID: ").strip()
        config = update_env_and_reload("SPOTIFY_CLIENT_ID", spotify_client_id)

        spotify_client_secret = input("Enter your Spotify Client Secret: ").strip()
        config = update_env_and_reload("SPOTIFY_CLIENT_SECRET", spotify_client_secret)

        spotify_redirect_uri = input("Enter your Spotify Redirect URI: ").strip()
        config = update_env_and_reload("SPOTIFY_REDIRECT_URI", spotify_redirect_uri)

        print(f"Authorize here: https://accounts.spotify.com/authorize?client_id={config.spotify_client_id}&redirect_uri={config.spotify_redirect_uri}&response_type=code")

        # Get the authorization URL and extract the authorization code
        authorization_url = input("Enter the full URL after authorization: ").strip()
        try:
            authorization_code = extract_code_from_url(authorization_url)
            print(f"Extracted Authorization Code: {authorization_code}")

            # ?? Use the latest config with the correct redirect_uri
            token_manager = TokenManager(config)
            token_manager.generate_spotify_token(authorization_code)
        except ValueError as e:
            print(f"Error: {e}")

    print("Do you want to use MQTT? (y/n): ", end="")
    use_mqtt = input().strip().lower() == 'y'
    update_env_and_reload("USE_MQTT", str(use_mqtt).lower())

    if use_mqtt:
        mqtt_broker = input("Enter your MQTT Broker: ").strip()
        config = update_env_and_reload("MQTT_BROKER", mqtt_broker)

        mqtt_port = input("Enter your MQTT Port: ").strip()
        config = update_env_and_reload("MQTT_PORT", mqtt_port)

        mqtt_topic = input("Enter your MQTT Topic: ").strip()
        config = update_env_and_reload("MQTT_TOPIC", mqtt_topic)

    print("? All necessary .env values have been written.")

if __name__ == "__main__":
    setup()
