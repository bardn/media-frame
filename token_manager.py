import requests
import base64
from dotenv import set_key, load_dotenv
import os

# Load the .env file to access configuration values
load_dotenv()

class TokenManager:
    def __init__(self, config):
        self.config = config

    def generate_trakt_token(self, authorization_code=None):
        if authorization_code is None:
            # If no authorization code is provided, prompt for the code
            authorization_code = input("Enter the authorization code you received: ")

        token_url = 'https://trakt.tv/oauth/token'
        data = {
            'client_id': self.config.trakt_client_id,
            'client_secret': self.config.trakt_client_secret,
            'redirect_uri': self.config.redirect_uri,
            'code': authorization_code,
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            data = response.json()
            self.config.trakt_access_token = data['access_token']
            self.config.trakt_refresh_token = data['refresh_token']
            # Store tokens in .env
            set_key(".env", "TRAKT_ACCESS_TOKEN", self.config.trakt_access_token)
            set_key(".env", "TRAKT_REFRESH_TOKEN", self.config.trakt_refresh_token)
            print("Trakt access token generated and stored in .env.")
            return True
        else:
            print(f"Trakt token generation failed: {response.status_code} {response.text}")
            return False

    def generate_spotify_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'client_credentials'
        }

        # Using the same method as your working example to get credentials
        client_id = self.config.spotify_client_id
        client_secret = self.config.spotify_client_secret

        headers = {
            'Authorization': f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(token_url, data=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.config.spotify_access_token = data['access_token']
            # Store token in .env
            set_key(".env", "SPOTIFY_ACCESS_TOKEN", self.config.spotify_access_token)
            print("Spotify access token generated and stored in .env.")
            return True
        else:
            print(f"Spotify token generation failed: {response.status_code} {response.text}")
            return False

    def refresh_trakt_token(self):
        # Refresh Trakt token using refresh token
        token_url = 'https://trakt.tv/oauth/token'
        data = {
            'client_id': self.config.trakt_client_id,
            'client_secret': self.config.trakt_client_secret,
            'redirect_uri': self.config.redirect_uri,
            'refresh_token': self.config.trakt_refresh_token,
            'grant_type': 'refresh_token'
        }

        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            data = response.json()
            self.config.trakt_access_token = data['access_token']
            self.config.trakt_refresh_token = data.get('refresh_token', self.config.trakt_refresh_token)
            # Store updated tokens in .env
            set_key(".env", "TRAKT_ACCESS_TOKEN", self.config.trakt_access_token)
            set_key(".env", "TRAKT_REFRESH_TOKEN", self.config.trakt_refresh_token)
            print("Trakt access token refreshed and stored in .env.")
            return True
        else:
            print(f"Trakt token refresh failed: {response.status_code} {response.text}")
            return False

    def refresh_spotify_token(self):
        # Refresh Spotify token using refresh token
        token_url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.config.spotify_refresh_token
        }

        # Using the same method as your working example to get credentials
        client_id = self.config.spotify_client_id
        client_secret = self.config.spotify_client_secret

        headers = {
            'Authorization': f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(token_url, data=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.config.spotify_access_token = data['access_token']
            if 'refresh_token' in data:
                self.config.spotify_refresh_token = data['refresh_token']
            # Store updated tokens in .env
            set_key(".env", "SPOTIFY_ACCESS_TOKEN", self.config.spotify_access_token)
            set_key(".env", "SPOTIFY_REFRESH_TOKEN", self.config.spotify_refresh_token)
            print("Spotify access token refreshed and stored in .env.")
            return True
        else:
            print(f"Spotify token refresh failed: {response.status_code} {response.text}")
            return False
