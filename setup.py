import os
from dotenv import load_dotenv, set_key
from token_manager import generate_trakt_token, generate_spotify_token  # Assuming these functions handle OAuth

# Load environment variables
load_dotenv()

def prompt_and_set_env_variable(variable_name, prompt_message):
    value = input(prompt_message)
    set_key('.env', variable_name, value)
    print(f"{variable_name} has been set in .env.")

def setup_trakt():
    # Prompt for Trakt credentials and store them in .env
    print("\nSetting up Trakt credentials...")
    client_id = input("Enter your Trakt Client ID: ")
    client_secret = input("Enter your Trakt Client Secret: ")
    redirect_uri = input("Enter your Trakt Redirect URI: ")
    
    # Set values in .env
    set_key('.env', 'TRAKT_CLIENT_ID', client_id)
    set_key('.env', 'TRAKT_CLIENT_SECRET', client_secret)
    set_key('.env', 'TRAKT_REDIRECT_URI', redirect_uri)

    # Generate and store the access token using the Trakt API (OAuth process)
    print("Now generating the Trakt access token...")
    generate_trakt_token(client_id, client_secret, redirect_uri)

def setup_spotify():
    # Prompt for Spotify credentials and store them in .env
    print("\nSetting up Spotify credentials...")
    client_id = input("Enter your Spotify Client ID: ")
    client_secret = input("Enter your Spotify Client Secret: ")
    
    # Set values in .env
    set_key('.env', 'SPOTIFY_CLIENT_ID', client_id)
    set_key('.env', 'SPOTIFY_CLIENT_SECRET', client_secret)

    # Generate and store the access token using the Spotify API (OAuth process)
    print("Now generating the Spotify access token...")
    generate_spotify_token(client_id, client_secret)

def setup():
    # Ask if the user wants to use Trakt
    use_trakt = input("Do you want to use Trakt? (y/n): ").lower()
    if use_trakt == "y":
        setup_trakt()
    
    # Ask if the user wants to use Spotify
    use_spotify = input("Do you want to use Spotify? (y/n): ").lower()
    if use_spotify == "y":
        setup_spotify()
    
    print("All necessary .env values have been written.")

if __name__ == "__main__":
    setup()
