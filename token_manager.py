import requests
import base64
from threading import Lock
from typing import Optional
from config import Config

class TokenManager:
    def __init__(self, config: Config):
        self.config = config
        self._lock = Lock()

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

    def generate_spotify_token(self, authorization_code: str) -> bool:
        """Handles the generation of Spotify token using the authorization code."""
        with self._lock:
            try:
                response = requests.post(
                    'https://accounts.spotify.com/api/token',
                    data={
                        'grant_type': 'authorization_code',
                        'code': authorization_code,
                        'redirect_uri': self.config.redirect_uri
                    },
                    headers={
                        'Authorization': f'Basic {base64.b64encode(f"{self.config.spotify_client_id}:{self.config.spotify_client_secret}".encode()).decode()}',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                )
                response.raise_for_status()
                tokens = response.json()
                self.config.spotify_access_token = tokens['access_token']
                self.config.spotify_refresh_token = tokens.get('refresh_token', self.config.spotify_refresh_token)
                return True
            except Exception as e:
                print(f"Spotify token generation failed: {e}")
                return False

    def generate_trakt_token(self, authorization_code: str) -> bool:
        """Handles the generation of Trakt token using the authorization code."""
        with self._lock:
            try:
                response = requests.post(
                    'https://trakt.tv/oauth/token',
                    json={
                        'code': authorization_code,
                        'client_id': self.config.trakt_client_id,
                        'client_secret': self.config.trakt_client_secret,
                        'redirect_uri': self.config.redirect_uri,
                        'grant_type': 'authorization_code'
                    }
                )
                response.raise_for_status()
                tokens = response.json()
                self.config.trakt_access_token = tokens['access_token']
                self.config.trakt_refresh_token = tokens.get('refresh_token', self.config.trakt_refresh_token)
                return True
            except Exception as e:
                print(f"Trakt token generation failed: {e}")
                return False

    def get_authorization_code(self, service: str) -> str:
        """Prompts the user to enter the authorization code from the service (Trakt/Spotify)."""
        while True:
            code = input(f"Enter the authorization code for {service}: ").strip()
            if code.startswith("https://"):
                # Extract only the code part from the URL
                code = code.split('code=')[-1]  # Get the part after 'code='
            if code:
                return code
            else:
                print(f"Invalid code for {service}. Please try again.")
