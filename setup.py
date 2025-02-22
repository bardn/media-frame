import os
from config import Config
from token_manager import TokenManager

def setup():
    print("Welcome to the Media Frame Setup!")

    # Initialize configuration and token manager
    config = Config()
    token_manager = TokenManager(config)

    # Prompt user for Trakt credentials
    use_trakt = input("Do you want to use Trakt? (y/n): ").lower()
    if use_trakt == "y":
        config.trakt_client_id = input("Enter your Trakt Client ID: ")
        config.trakt_client_secret = input("Enter your Trakt Client Secret: ")
        config.redirect_uri = input("Enter your Trakt Redirect URI: ")

        # Save Trakt details to .env
        with open('.env', 'a') as f:
            f.write(f"TRAKT_CLIENT_ID={config.trakt_client_id}\n")
            f.write(f"TRAKT_CLIENT_SECRET={config.trakt_client_secret}\n")
            f.write(f"REDIRECT_URI={config.redirect_uri}\n")

        # Generate Trakt token
        if not token_manager.generate_trakt_token():
            print("Trakt token generation failed. Please check your credentials.")

    # Prompt user for Spotify credentials
    use_spotify = input("Do you want to use Spotify? (y/n): ").lower()
    if use_spotify == "y":
        config.spotify_client_id = input("Enter your Spotify Client ID: ")
        config.spotify_client_secret = input("Enter your Spotify Client Secret: ")
        config.redirect_uri = input("Enter your Spotify Redirect URI: ")

        # Save Spotify details to .env
        with open('.env', 'a') as f:
            f.write(f"SPOTIFY_CLIENT_ID={config.spotify_client_id}\n")
            f.write(f"SPOTIFY_CLIENT_SECRET={config.spotify_client_secret}\n")

        # Generate Spotify token
        if not token_manager.generate_spotify_token():
            print("Spotify token generation failed. Please check your credentials.")

    # Save all necessary .env values
    with open('.env', 'a') as f:
        f.write("MEDIA_FRAME_SETUP=true\n")

    print("All necessary .env values have been written.")
    print("Setup complete!")

if __name__ == "__main__":
    setup()
