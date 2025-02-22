import os
import sys
import webbrowser
import requests
from dotenv import load_dotenv

# Load .env file (if exists)
load_dotenv()

def get_input(prompt, env_var=None):
    # Get input from the user or use the existing env variable if it's set
    if env_var and os.getenv(env_var):
        return os.getenv(env_var)
    return input(prompt)

def create_oauth_url(client_id, redirect_uri):
    # URL format for Trakt's OAuth authorization page
    return f"https://trakt.tv/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"

def get_trakt_tokens(client_id, client_secret, redirect_uri, auth_code):
    # Endpoint to exchange the authorization code for access and refresh tokens
    token_url = "https://trakt.tv/oauth/token"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'code': auth_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }

    response = requests.post(token_url, json=data, headers=headers)

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')

        # Append tokens to .env file
        with open('.env', 'a') as f:
            f.write(f"TRAKT_ACCESS_TOKEN={access_token}\n")
            f.write(f"TRAKT_REFRESH_TOKEN={refresh_token}\n")

        print(f"Successfully saved tokens to .env. Access Token: {access_token}\n")
    else:
        print("Failed to get tokens. Please check your credentials and authorization code.")
        print(f"Response: {response.text}")
        sys.exit(1)

def get_spotify_access_token(client_id, client_secret):
    # A simplified example of how to get the Spotify access token
    auth_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {client_id}:{client_secret}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(auth_url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json().get("access_token")

        # Append the token to .env file
        with open('.env', 'a') as f:
            f.write(f"SPOTIFY_ACCESS_TOKEN={access_token}\n")

        print(f"Successfully retrieved Spotify access token: {access_token}")
    else:
        print("Failed to get Spotify access token. Please check your client credentials.")
        sys.exit(1)

def populate_env():
    # Collect initial credentials for the .env file
    spotify_client_id = get_input("Enter your Spotify Client ID: ", "SPOTIFY_CLIENT_ID")
    spotify_client_secret = get_input("Enter your Spotify Client Secret: ", "SPOTIFY_CLIENT_SECRET")
    trakt_client_id = get_input("Enter your Trakt Client ID: ", "TRAKT_CLIENT_ID")
    trakt_client_secret = get_input("Enter your Trakt Client Secret: ", "TRAKT_CLIENT_SECRET")
    trakt_redirect_uri = get_input("Enter your Trakt Redirect URI: ", "TRAKT_REDIRECT_URI")
    tmdb_api_key = get_input("Enter your TMDb API Key: ", "TMDB_API_KEY")

    # Collect MQTT details
    mqtt_broker = get_input("Enter your MQTT Broker IP: ", "MQTT_BROKER")
    mqtt_port = get_input("Enter your MQTT Broker Port: ", "MQTT_PORT")
    mqtt_topic = get_input("Enter your MQTT Topic: ", "MQTT_TOPIC")

    # Write basic values to .env file
    with open('.env', 'w') as f:
        f.write(f"SPOTIFY_CLIENT_ID={spotify_client_id}\n")
        f.write(f"SPOTIFY_CLIENT_SECRET={spotify_client_secret}\n")
        f.write(f"TRAKT_CLIENT_ID={trakt_client_id}\n")
        f.write(f"TRAKT_CLIENT_SECRET={trakt_client_secret}\n")
        f.write(f"TRAKT_REDIRECT_URI={trakt_redirect_uri}\n")
        f.write(f"TMDB_API_KEY={tmdb_api_key}\n")
        f.write(f"MQTT_BROKER={mqtt_broker}\n")
        f.write(f"MQTT_PORT={mqtt_port}\n")
        f.write(f"MQTT_TOPIC={mqtt_topic}\n")

    print("\nBasic environment variables written to .env.")

def main():
    print("Welcome to the Media Frame Setup!")

    # Ask if services should be enabled
    use_trakt = get_input("Do you want to use Trakt? (y/n): ").lower() == 'y'
    use_spotify = get_input("Do you want to use Spotify? (y/n): ").lower() == 'y'

    # Populate .env with basic credentials
    populate_env()

    # Handle the OAuth process for Trakt if needed
    if use_trakt:
        trakt_client_id = os.getenv('TRAKT_CLIENT_ID')
        trakt_redirect_uri = os.getenv('TRAKT_REDIRECT_URI')
        oauth_url = create_oauth_url(trakt_client_id, trakt_redirect_uri)

        print(f"\nPlease visit the following URL in your browser to authorize the Trakt application:")
        print(oauth_url)

        # Open the URL automatically in the browser
        webbrowser.open(oauth_url)

        # Wait for the user to enter the authorization code
        auth_code = input("\nAfter authorization, you will be redirected to a page with a 'code' parameter in the URL. Please enter the 'code' here: ")

        # Get the Trakt access and refresh tokens using the authorization code
        get_trakt_tokens(trakt_client_id, os.getenv('TRAKT_CLIENT_SECRET'), trakt_redirect_uri, auth_code)
    else:
        print("Trakt will not be used. Skipping OAuth token generation.")

    # Handle Spotify access token if needed
    if use_spotify:
        if not os.getenv("SPOTIFY_ACCESS_TOKEN"):
            get_spotify_access_token(os.getenv("SPOTIFY_CLIENT_ID"), os.getenv("SPOTIFY_CLIENT_SECRET"))
        else:
            print("Spotify Access Token already present in .env.")
    else:
        print("Spotify will not be used. Skipping token generation.")

if __name__ == "__main__":
    main()
