import requests
from typing import Optional
from config import Config
import time

class APIClient:
    def __init__(self, config: Config):
        self.config = config
        self._last_watching_data = None
        self._last_watching_time = 0
        self.CACHE_DURATION = 5  # seconds

    def get_spotify_current_track(self) -> Optional[dict]:
        try:
            response = requests.get(
                'https://api.spotify.com/v1/me/player/currently-playing',
                headers={'Authorization': f'Bearer {self.config.spotify_access_token}'}
            )

            if response.status_code == 204:
                return None
            elif response.status_code == 401:
                if self.refresh_spotify_token():
                    return self.get_spotify_current_track()
                return None

            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to fetch Spotify track: {e}")
            return None

    def get_trakt_watching(self) -> Optional[dict]:
        if time.time() - self._last_watching_time < self.CACHE_DURATION:
            return self._last_watching_data

        try:
            response = requests.get(
                f'https://api.trakt.tv/users/{self.config.trakt_username}/watching',
                headers={
                    'Authorization': f'Bearer {self.config.trakt_access_token}',
                    'trakt-api-key': self.config.trakt_client_id,
                    'trakt-api-version': '2'
                }
            )

            if response.status_code == 401:
                if self.refresh_trakt_token():
                    return self.get_trakt_watching()
                return None

            response.raise_for_status()
            self._last_watching_data = response.json()
            self._last_watching_time = time.time()
            return self._last_watching_data
        except Exception as e:
            print(f"Failed to fetch Trakt watching: {e}")
            return self._last_watching_data if time.time() - self._last_watching_time < self.CACHE_DURATION else None

    def get_tmdb_poster(self, tmdb_id: int, is_movie: bool = True, season_number: Optional[int] = None) -> Optional[str]:
        try:
            endpoint = f"{'movie' if is_movie else 'tv'}/{tmdb_id}"
            if not is_movie and season_number:
                endpoint += f"/season/{season_number}"

            response = requests.get(
                f'https://api.themoviedb.org/3/{endpoint}',
                params={'api_key': self.config.tmdb_api_key}
            )
            response.raise_for_status()

            poster_path = response.json().get('poster_path')
            return f'https://image.tmdb.org/t/p/original{poster_path}' if poster_path else None
        except Exception as e:
            print(f"Failed to fetch TMDB poster: {e}")
            return None
