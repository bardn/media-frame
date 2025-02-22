import requests
import base64
from threading import Lock
from typing import Optional
from config import Config
import webbrowser

class TokenManager:
    def __init__(self, config: Config):
        self.config = config
        self._lock = Lock()

    def generate_spotify_token(self) -> bool:
        """Generate Spotify token using the authorization code flow."""
        try:
            # Step 1: Generate the authorization URL
            auth_url = f"https://accounts.spotify.com/authorize?client_id={self.config.spotify_client_id}&response_type=code&redirect_uri={self.config.redirect_uri}"
            print(f"Please open this URL to authorize: {auth_url}")
            webbrowser.open(auth_url)
            
            # Step 2: Get the authorization code from the user input
            auth_code = input("Enter the authorization code: ")

            # Step 3: Exchange the authorization code for an access token
            response = requests.post(
                'https://accounts.spotify.com/api/token',
                data={
                    'grant_type': 'authorization_code',
                    'code': auth_code,
                    'redirect_uri': self.config.redirect_uri
                },
                headers={
                    'Authorization': f'Basic {base64.b64encode(f"{self.config.spotify_client_id}:{self.config.spotify_client_secret}".encode()).decode()}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            )
            response.raise_for_status()
            tokens = response.json()

            # Step 4: Save the tokens in the config object
            self.config.spotify_access_token = tokens['access_token']
            self.config.spotify_refresh_token = tokens.get('refresh_token', '')
            print("Spotify access token generated and saved.")
            return True
        except Exception as e:
            print(f"Spotify token generation failed: {e}")
            return False

    def generate_trakt_token(self) -> bool:
        """Generate Trakt token using the authorization code flow."""
        try:
            # Step 1: Generate the authorization URL
            auth_url = f"https://trakt.tv/oauth/authorize?client_id={self.config.trakt_client_id}&redirect_uri={self.config.redirect_uri}&response_type=code"
            print(f"Please open this URL to authorize: {auth_url}")
            webbrowser.open(auth_url)

            # Step 2: Get the authorization code from the user input
            auth_code = input("Enter the authorization code: ")

            # Step 3: Exchange the authorization code for an access token
            response = requests.post(
                'https://trakt.tv/oauth/token',
                json={
                    'client_id': self.config.trakt_client_id,
                    'client_secret': self.config.trakt_client_secret,
                    'code': auth_code,
                    'redirect_uri': self.config.redirect_uri,
                    'grant_type': 'authorization_code'
                }
            )
            response.raise_for_status()
            tokens = response.json()

            # Step 4: Save the tokens in the config object
            self.config.trakt_access_token = tokens['access_token']
            self.config.trakt_refresh_token = tokens.get('refresh_token', self.config.trakt_refresh_token)
            print("Trakt access token generated and saved.")
            return True
        except Exception as e:
            print(f"Trakt token generation failed: {e}")
            return False

    def refresh_spotify_token(self) -> bool:
        with self._lock:
            try:
                response = requests.post(
                    'https://accounts.spotify.com/api/token',
                    data={
                        'grant_type': 'refresh_token',
                        'refresh_token': self.config.spotify_refresh_token
                    },
                    headers={
                        'Authorization': f'Basic {base64.b64encode(f"{self.config.spotify_client_id}:{self.config.spotify_client_secret}".encode()).decode()}',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                )
                response.raise_for_status()
                tokens = response.json()
                self.config.spotify_access_token = tokens['access_token']
                if 'refresh_token' in tokens:
                    self.config.spotify_refresh_token = tokens['refresh_token']
                return True
            except Exception as e:
                print(f"Spotify token refresh failed: {e}")
                return False

    def refresh_trakt_token(self) -> bool:
        with self._lock:
            try:
                response = requests.post(
                    'https://trakt.tv/oauth/token',
                    json={
                        'refresh_token': self.config.trakt_refresh_token,
                        'client_id': self.config.trakt_client_id,
                        'client_secret': self.config.trakt_client_secret,
                        'redirect_uri': self.config.redirect_uri,
                        'grant_type': 'refresh_token'
                    }
                )
                response.raise_for_status()
                tokens = response.json()
                self.config.trakt_access_token = tokens['access_token']
                self.config.trakt_refresh_token = tokens.get('refresh_token', self.config.trakt_refresh_token)
                return True
            except Exception as e:
                print(f"Trakt token refresh failed: {e}")
                return False
