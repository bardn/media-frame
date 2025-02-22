from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config(BaseModel):
    spotify_client_id: str = Field(..., env='SPOTIFY_CLIENT_ID')
    spotify_client_secret: str = Field(..., env='SPOTIFY_CLIENT_SECRET')
    spotify_access_token: str = Field(..., env='SPOTIFY_ACCESS_TOKEN')
    spotify_refresh_token: str = Field(..., env='SPOTIFY_REFRESH_TOKEN')
    trakt_username: str = Field(..., env='TRAKT_USERNAME')
    trakt_client_id: str = Field(..., env='TRAKT_CLIENT_ID')
    trakt_client_secret: str = Field(..., env='TRAKT_CLIENT_SECRET')
    trakt_access_token: str = Field(..., env='TRAKT_ACCESS_TOKEN')
    trakt_refresh_token: str = Field(..., env='TRAKT_REFRESH_TOKEN')
    tmdb_api_key: str = Field(..., env='TMDB_API_KEY')
    redirect_uri: str = Field(..., env='REDIRECT_URI')
    mqtt_broker: str = Field(..., env='MQTT_BROKER')
    mqtt_port: int = Field(..., env='MQTT_PORT')
    mqtt_topic: str = Field(..., env='MQTT_TOPIC')

    class Config:
        env_file = ".env"
