from pydantic import BaseModel, Field
import os

class Config(BaseModel):
    # Feature toggles
    use_trakt: bool = Field(default=os.getenv('USE_TRAKT', 'false').lower() == 'true', env='USE_TRAKT')
    use_spotify: bool = Field(default=os.getenv('USE_SPOTIFY', 'false').lower() == 'true', env='USE_SPOTIFY')
    use_mqtt: bool = Field(default=os.getenv('USE_MQTT', 'false').lower() == 'true', env='USE_MQTT')

    # Spotify credentials
    spotify_client_id: str = Field(default=os.getenv('SPOTIFY_CLIENT_ID', ''), env='SPOTIFY_CLIENT_ID')
    spotify_client_secret: str = Field(default=os.getenv('SPOTIFY_CLIENT_SECRET', ''), env='SPOTIFY_CLIENT_SECRET')
    spotify_access_token: str = Field(default=os.getenv('SPOTIFY_ACCESS_TOKEN', ''), env='SPOTIFY_ACCESS_TOKEN')
    spotify_refresh_token: str = Field(default=os.getenv('SPOTIFY_REFRESH_TOKEN', ''), env='SPOTIFY_REFRESH_TOKEN')
    spotify_redirect_uri: str = Field(default=os.getenv('SPOTIFY_REDIRECT_URI', ''), env='SPOTIFY_REDIRECT_URI')

    # Trakt credentials
    trakt_username: str = Field(default=os.getenv('TRAKT_USERNAME', ''), env='TRAKT_USERNAME')
    trakt_client_id: str = Field(default=os.getenv('TRAKT_CLIENT_ID', ''), env='TRAKT_CLIENT_ID')
    trakt_client_secret: str = Field(default=os.getenv('TRAKT_CLIENT_SECRET', ''), env='TRAKT_CLIENT_SECRET')
    trakt_access_token: str = Field(default=os.getenv('TRAKT_ACCESS_TOKEN', ''), env='TRAKT_ACCESS_TOKEN')
    trakt_refresh_token: str = Field(default=os.getenv('TRAKT_REFRESH_TOKEN', ''), env='TRAKT_REFRESH_TOKEN')
    trakt_redirect_uri: str = Field(default=os.getenv('TRAKT_REDIRECT_URI', ''), env='TRAKT_REDIRECT_URI')

    # TMDb API key
    tmdb_api_key: str = Field(default=os.getenv('TMDB_API_KEY', ''), env='TMDB_API_KEY')

    # MQTT settings
    mqtt_broker: str = Field(default=os.getenv('MQTT_BROKER', ''), env='MQTT_BROKER')
    mqtt_port: int = Field(default=int(os.getenv('MQTT_PORT', 1883)), env='MQTT_PORT')
    mqtt_topic: str = Field(default=os.getenv('MQTT_TOPIC', ''), env='MQTT_TOPIC')

    class Config:
        env_file = ".env"  # Read from .env file

