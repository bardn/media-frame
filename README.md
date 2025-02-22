# Media Frame

**Media Frame** is a real-time media display system that integrates with **Spotify**, **Trakt**, and **TMDb** APIs to display media information such as album art, song details, and movie/TV show posters on a connected display. It updates in real-time when media is played, paused, or stopped, making it ideal for dynamic displays such as LED matrix screens.

---

## Features

- **Spotify Integration**: Display album art, song details, and artist information from Spotify.
- **Trakt Integration**: Sync with Trakt to display the currently watched movies and TV shows.
- **TMDb Integration**: Fetch movie and show details from the TMDb API for richer media information.
- **Real-time Updates**: The display updates instantly when media is played, paused, or stopped on Spotify.
- **LED Matrix Support**: Control an interactive LED matrix display.
- **Easy Setup**: Automated configuration through the provided scripts.
- **Background Service**: Run the application as a system service in the background.

---

## Requirements

- Python 3.8+
- A Spotify Developer account (for API credentials)
- A Trakt Developer account (for OAuth credentials)
- A TMDb API key (for fetching movie/show data)
- `pip` for Python dependency management

---

## Installation

Follow the steps below to install and configure the Media Frame system.

### 1. Clone the Repository

```
git clone https://github.com/yourusername/media-frame.git
cd media-frame
```

### 2. Install Dependencies

Install the required Python dependencies using pip:
```
pip install -r requirements.txt
```
### 3. Set Up the .env File

The .env file contains sensitive API credentials and configurations. To generate it, you can either use the provided setup script or manually configure it.
### Option 1: Automated Setup (Recommended)

Run the setup.py script to automate the process:

Install dependencies.
Create and configure the .env file.
Run the OAuth authentication for Trakt and store OAuth tokens.
```
python setup.py
```
### Option 2: Manual Setup

If you prefer to manually configure the system, follow these steps:

Copy the .env.example file to .env:
```
cp .env.example .env
```
Edit the .env file with your credentials:
```
# Spotify API credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_ACCESS_TOKEN=your_spotify_access_token
SPOTIFY_REFRESH_TOKEN=your_spotify_refresh_token

# Trakt API credentials
TRAKT_USERNAME=your_trakt_username
TRAKT_CLIENT_ID=your_trakt_client_id
TRAKT_CLIENT_SECRET=your_trakt_client_secret
TRAKT_REDIRECT_URI=your_trakt_redirect_uri

# TMDb API key
TMDB_API_KEY=your_tmdb_api_key

# OAuth tokens (these will be populated after successful OAuth process)
TRAKT_ACCESS_TOKEN=
TRAKT_REFRESH_TOKEN=

# MQTT
MQTT_BROKER=mqtt_broker_local_ip
MQTT_PORT=mqtt_broker_port_number
MQTT_TOPIC=homeassistant/matrix/brightness
```
Run setup.py to authenticate with Trakt and generate OAuth tokens:
```
    python setup.py
```
### 4. Running the Application

Once everything is configured, you can run the application:
```
python media_frame.py
```
### 5. Run as a Background Service (Optional)

If you want the application to run automatically in the background, use the generate_service.py script to create a systemd service:
```
python generate_service.py
```
This will install the service and enable it to start on boot. You can check the status of the service with:
```
sudo systemctl status media-frame.service
```
### File Overview

    media_frame.py: The main entry point of the application. Handles media display integration with Spotify, Trakt, and TMDb.
    api_client.py: Contains functions to interact with the Spotify and Trakt APIs.
    image_manager.py: Manages image-related tasks like fetching album art and posters.
    matrix_controller.py: Controls the LED matrix display, sending updates for media information.
    token_manager.py: Handles OAuth flow for obtaining and refreshing Trakt tokens.
    config.py: Loads configuration settings from the .env file.
    generate_service.py: A script to generate and configure the systemd service for running the application in the background.
    setup.py: A script to set up Trakt OAuth tokens and other initial configurations.
    requirements.txt: A list of required Python dependencies.
    .env: Configuration file storing sensitive API keys and credentials.
    README.md: This file, which explains how to set up and use the project.

### Troubleshooting



### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Contributing

If you encounter any issues or want to contribute, feel free to open an issue or submit a pull request. All contributions are welcome!
