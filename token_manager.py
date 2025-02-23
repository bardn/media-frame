import requests
import base64
from dotenv import set_key
from config import Config

class TokenManager:
    def __init__(self, config: Config):
        self.config = config

    def generate_trakt_token(self):
        # Generate Trakt token using the authorization code
        print("Please open this URL to authorize: https://trakt.tv/oauth/authorize")
        print(f"Client ID: {self.config.trakt_client_id}")
        print(f"Redirect URI: {self.config.redirect_uri}")
        authorization_code = input("Enter the authorization code you received: ")

        response = requests.post(
            'https://trakt.tv/oauth/token',
            json={
                'client_id': self.config.trakt_client_id,
                'client_secret': self.config.trakt_client_secret,
                'redirect_uri': self.config.redirect_uri,
                'code': authorization_code,
                'grant_type': 'authorization_code'
            }
        )

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
            print(f"Trakt token generation failed: {response.status_code}")
            return False

    def generate_spotify_token(self):
        # Generate Spotify token using client credentials
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            data={
                'grant_type': 'client_credentials'
            },
            headers={
                'Authorization': f"Basic {self._encode_spotify_credentials()}"
            }
        )

        if response.status_code == 200:
            data = response.json()
            self.config.spotify_access_token = data['access_token']
            # Store token in .env
            set_key(".env", "SPOTIFY_ACCESS_TOKEN", self.config.spotify_access_token)
            print("Spotify access token generated and stored in .env.")
            return True
        else:
            print(f"Spotify token generation failed: {response.status_code}")
            return False

    def refresh_spotify_token(self):
        # Refresh Spotify token using refresh token
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.config.spotify_refresh_token
            },
            headers={
                'Authorization': f"Basic {self._encode_spotify_credentials()}"
            }
        )

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
            print(f"Spotify token refresh failed: {response.status_code}")
            return False

    def refresh_trakt_token(self):
        # Refresh Trakt token using refresh token
        response = requests.post(
            'https://trakt.tv/oauth/token',
            json={
                'client_id': self.config.trakt_client_id,
                'client_secret': self.config.trakt_client_secret,
                'redirect_uri': self.config.redirect_uri,
                'refresh_token': self.config.trakt_refresh_token,
                'grant_type': 'refresh_token'
            }
        )

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
            print(f"Trakt token refresh failed: {response.status_code}")
            return False

    def _encode_spotify_credentials(self):
        # Base64 encode Spotify client ID and secret for the authorization header
        return base64.b64encode(f"{self.config.spotify_client_id}:{self.config.spotify_client_secret}".encode()).decode()
