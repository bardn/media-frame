import os
import sys
import webbrowser
import requests
from dotenv import load_dotenv

def get_input(prompt):
    """Helper function to safely get user input."""
    return input(prompt).strip()

def populate_env():
    """Populate the .env file with necessary environment variables."""
    trakt_client_id = get_input("Enter your Trakt Client ID: ")
    trakt_client_secret = get_input("Enter your Trakt Client Secret: ")
    trakt_redirect_uri = get_input("Enter your Trakt Redirect URI: ")

    spotify_client_id = get_input("Enter your Spotify Client ID: ")
    spotify_client_secret = get_input("Enter your Spotify Client Secret: ")

    # Writing values to .env file
    with open('.env', 'w') as f:
        f.write(f"TRAKT_CLIENT_ID={trakt_client_id}\n")
        f.write(f"TRAKT_CLIENT_SECRET={trakt_client_secret}\n")
        f.write(f"TRAKT_REDIRECT_URI={trakt_redirect_uri}\n")
        f.write(f"SPOTIFY_CLIENT_ID={spotify_client_id}\n")
        f.write(f"SPOTIFY_CLIENT_SECRET={spotify_client_secret}\n")
        print("\nAll necessary .env values have been written.")

def create_oauth_url(client_id, redirect_uri):
    """Generate the OAuth URL for Trakt authentication."""
    return f"https://trakt.tv/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"

def get_trakt_tokens(client_id, client_secret, redirect_uri, auth_code):
    """Get Trakt tokens after successful authorization."""
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
        print(f"Failed to get tokens. Response status code: {response.status_code}")
        print(f"Response: {response.text}")
        retry = get_input("Would you like to try again? (y/n): ").lower()
        if retry == 'y':
            new_auth_code = get_input("Please enter the authorization code again: ")
            get_trakt_tokens(client_id, client_secret, redirect_uri, new_auth_code)
        else:
            print("Exiting token retrieval process.")
            sys.exit(1)

def main():
    # Load environment variables from .env
    load_dotenv()

    print("Welcome to the Media Frame Setup!")

    # Ask if services should be enabled
    use_trakt = get_input("Do you want to use Trakt? (y/n): ").lower() == 'y'
    use_spotify = get_input("Do you want to use Spotify? (y/n): ").lower() == 'y'

    # Populate .env with basic credentials
    populate_env()

    # Handle the OAuth process for Trakt if needed
    if use_trakt:
        # Retrieve the trakt_client_id, client_secret, and redirect_uri from .env
        trakt_client_id = os.getenv('TRAKT_CLIENT_ID')
        trakt_client_secret = os.getenv('TRAKT_CLIENT_SECRET')
        trakt_redirect_uri = os.getenv('TRAKT_REDIRECT_URI')
        
        # Ensure we have the necessary values before proceeding
        if not trakt_client_id or not trakt_client_secret or not trakt_redirect_uri:
            print("Missing Trakt credentials in .env. Please ensure they are correctly populated.")
            sys.exit(1)

        oauth_url = create_oauth_url(trakt_client_id, trakt_redirect_uri)

        print(f"\nPlease visit the following URL in your browser to authorize the Trakt application:")
        print(oauth_url)

        # Open the URL automatically in the browser
        webbrowser.open(oauth_url)

        # Loop to allow retrying if the auth code is incorrect
        while True:
            auth_code = get_input("\nAfter authorization, you will be redirected to a page with a 'code' parameter in the URL. Please enter the 'code' here: ")

            # Try to fetch the tokens
            get_trakt_tokens(trakt_client_id, trakt_client_secret, trakt_redirect_uri, auth_code)
            break  # Exit the loop if successful
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
