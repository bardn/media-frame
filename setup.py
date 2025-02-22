import os
import requests
import time
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def prompt_for_input(prompt):
    return input(prompt).strip()

def create_env_file():
    print("Ensure you have your .env file with the following variables:")
    print("SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, TRAKT_USERNAME, TRAKT_CLIENT_ID, TRAKT_CLIENT_SECRET, TRAKT_REDIRECT_URI, TMDB_API_KEY")
    print("Once you have your .env file set up, the script will automatically fetch and refresh tokens.")

def get_authorization_code(client_id, redirect_uri):
    auth_url = (
        f"https://trakt.tv/oauth/authorize?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
    )
    print(f"Please go to this URL and authorize the app: {auth_url}")
    
    full_redirect_url = input("Enter the full redirected URL: ")
    
    parsed_url = urlparse(full_redirect_url)
    authorization_code = parse_qs(parsed_url.query).get('code', [None])[0]
    
    if not authorization_code:
        raise ValueError("Authorization code not found in the URL")
    
    return authorization_code

def exchange_code_for_token(client_id, client_secret, redirect_uri, code):
    token_url = 'https://trakt.tv/oauth/token'
    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()
    
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    
    return access_token, refresh_token

def save_tokens(access_token, refresh_token):
    # Save the tokens back to the .env file
    with open('.env', 'a') as f:
        f.write(f"\nTRAKT_ACCESS_TOKEN={access_token}")
        f.write(f"\nTRAKT_REFRESH_TOKEN={refresh_token}")
    
    print("Tokens have been saved to the .env file.")

def refresh_access_token(client_id, client_secret, redirect_uri, refresh_token):
    token_url = 'https://trakt.tv/oauth/token'
    data = {
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'refresh_token'
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()
    
    new_access_token = token_data.get('access_token')
    new_refresh_token = token_data.get('refresh_token')

    return new_access_token, new_refresh_token

def main():
    print("Welcome to the Trakt OAuth setup script.")

    # Retrieve values from the .env file
    trakt_username = os.getenv("TRAKT_USERNAME")
    client_id = os.getenv("TRAKT_CLIENT_ID")
    client_secret = os.getenv("TRAKT_CLIENT_SECRET")
    redirect_uri = os.getenv("TRAKT_REDIRECT_URI")
    tmdb_api_key = os.getenv("TMDB_API_KEY")

    if not all([trakt_username, client_id, client_secret, redirect_uri, tmdb_api_key]):
        print("Missing environment variables. Please ensure your .env file is set up properly.")
        return

    # Prompt user if the .env file isn't properly set up
    if not os.getenv("TRAKT_ACCESS_TOKEN") or not os.getenv("TRAKT_REFRESH_TOKEN"):
        print("OAuth tokens are not yet set. Proceeding with authorization...")
        authorization_code = get_authorization_code(client_id, redirect_uri)
        access_token, refresh_token = exchange_code_for_token(client_id, client_secret, redirect_uri, authorization_code)
        save_tokens(access_token, refresh_token)
    else:
        print("OAuth tokens are already available in the .env file.")
    
    # Optionally refresh the token after some time
    print("Waiting for 5 seconds before refreshing token...")
    time.sleep(5)
    
    refresh_token = os.getenv("TRAKT_REFRESH_TOKEN")
    if refresh_token:
        new_access_token, new_refresh_token = refresh_access_token(client_id, client_secret, redirect_uri, refresh_token)
        save_tokens(new_access_token, new_refresh_token)
    else:
        print("No refresh token found in .env. OAuth process will need to be re-run.")

if __name__ == '__main__':
    main()
