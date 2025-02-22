# **Media Frame**

A smart media display system that integrates **Spotify**, **Trakt**, and **TMDb** APIs with an **LED matrix display** to show real-time information like album art, movie posters, and a clock overlay. It allows dynamic display changes depending on your media consumption.

---

## **Features**

- Display the currently playing track from **Spotify**.
- Show what you're currently watching (movie/show/episode) from **Trakt**.
- Fetch and display media posters from **TMDb** for movies and TV shows.
- Overlay a real-time clock on the display.
- Interactive **LED matrix** display with brightness control via **MQTT**.
- Efficient token management for Spotify and Trakt using refresh tokens.

- ## **Setup Instructions**

### **1. Clone the Repository**

```
git clone https://github.com/bardn/media-frame.git
cd media-frame
'''

---

# Media Frame

Media Frame is a real-time media display system that integrates with Spotify, Trakt, and TMDb APIs to show information such as album art, song details, and movie/TV show information on a display. It can be easily configured to work with different platforms and displays, with real-time updates for play, pause, and stop events.

## Features

- **Spotify Integration:** Display album art, song details, and artist information from Spotify.
- **Trakt Integration:** Sync with Trakt for movie and TV show tracking.
- **TMDb Integration:** Use TMDb API to fetch movie and show data.
- **Real-time Updates:** Automatically refreshes album art and track details when Spotify play, pause, or stop events occur.
- **Easy Setup:** Just configure your `.env` file and run the setup script to get everything working.
- **Background Service:** Option to run the system as a background service using `systemd` on Linux.

## Requirements

- Python 3.8+
- `pip` for Python package installation
- A Spotify Developer account (for API credentials)
- A Trakt Developer account (for OAuth credentials)
- A TMDb API key (for movie/show details)

## Installation

Follow these steps to install and configure the system.

### 1. Clone the repository
Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/media-frame.git
cd media-frame

2. Install dependencies

Use pip to install the required Python dependencies:

pip install -r requirements.txt

3. Set up the .env file

Copy the .env.example file to .env and configure the necessary API keys and credentials.

cp .env.example .env

Edit the .env file with your Spotify, Trakt, and TMDb credentials:

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

    Replace your_spotify_client_id, your_spotify_client_secret, etc., with your actual API credentials.

4. Set up the Trakt OAuth tokens

Run the setup.py script to authenticate with Trakt and obtain the necessary OAuth tokens:

python setup.py

This will guide you through the process of authenticating with Trakt and will save your TRAKT_ACCESS_TOKEN and TRAKT_REFRESH_TOKEN to the .env file for future use.
5. Run the application

Once everything is set up, run the application:

python main.py

6. Run as a background service (Optional)

To automatically start the system as a background service on boot, you can use the setup.sh script. This script installs dependencies, sets up the .env file, runs the setup process, and installs the systemd service.

Run the setup.sh script:

./setup.sh

This will guide you through the entire process and install a background service for the application. Once set up, the system will start automatically on boot and run in the background.
7. Checking the service status

If you installed the system as a background service, you can check its status using the following command:

sudo systemctl status media-frame.service

File Overview

    main.py: The main entry point for the application. This handles the integration with Spotify, Trakt, and TMDb, as well as the display updates.
    api_client.py: Contains functions to interact with the Spotify and Trakt APIs.
    image_manager.py: Manages album art and other image-related tasks.
    matrix_controller.py: Controls the display, including sending updates for album art and track information.
    token_manager.py: Handles the OAuth flow for obtaining and refreshing Trakt API tokens.
    config.py: Loads configuration settings from the .env file.
    setup.py: A script to set up OAuth for Trakt and generate the necessary tokens.
    requirements.txt: A list of Python dependencies required for the project.
    .env: A configuration file containing sensitive API keys and tokens. This file is not committed to version control.
    README.md: The documentation for setting up and using the project.
    setup.sh: A script to automate the installation and setup process, including creating the .env file and installing the systemd service.
    media-frame-install-service.sh: An optional script to install the systemd service for running the application as a background process.

Troubleshooting

    If you experience any issues with the OAuth flow for Trakt, ensure that your TRAKT_REDIRECT_URI matches the URI registered in your Trakt Developer account.
    If you encounter any issues with Spotify integration, verify that your SPOTIFY_ACCESS_TOKEN is valid and hasn’t expired. You may need to refresh your token.
    Ensure your MQTT broker is set up correctly if you're using it to send updates to other systems like Home Assistant.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Contributing

If you find any bugs or want to contribute to the project, feel free to open an issue or submit a pull request.

Happy coding and enjoy your media frame experience!


### Key Updates:

- **Step 6 (Run as a background service):** Added details about using the `setup.sh` script to automate the installation and setup, including setting up the background service with `systemd`.
- **File Overview:** Mentioned the `setup.sh` and `media-frame-install-service.sh` scripts for users who wish to install the service.

With this updated `README.md`, your users will have a clear guide to automate the setup with the provided shell script and easily install the system as a background service.

Let me know if you'd like to make any more adjustments!

You said:
alter the read me, make sure its all in markdowm so that i can copy it direct, so that the setup is used to automate the generation of the .env variables and run the steup.py and give the option for manual instillation using the setup.py and a new (create this) python script to generate the service
ChatGPT said:

Here's the updated README.md in Markdown format. This version provides an explanation of how to use the setup.sh to automate the process and also offers the option for a manual installation using the setup.py script and a new Python script to generate the service.

# Media Frame

Media Frame is a real-time media display system that integrates with Spotify, Trakt, and TMDb APIs to show information such as album art, song details, and movie/TV show information on a display. It can be easily configured to work with different platforms and displays, with real-time updates for play, pause, and stop events.

## Features

- **Spotify Integration:** Display album art, song details, and artist information from Spotify.
- **Trakt Integration:** Sync with Trakt for movie and TV show tracking.
- **TMDb Integration:** Use TMDb API to fetch movie and show data.
- **Real-time Updates:** Automatically refreshes album art and track details when Spotify play, pause, or stop events occur.
- **Easy Setup:** Just configure your `.env` file and run the setup script to get everything working.
- **Background Service:** Option to run the system as a background service using `systemd` on Linux.

## Requirements

- Python 3.8+
- `pip` for Python package installation
- A Spotify Developer account (for API credentials)
- A Trakt Developer account (for OAuth credentials)
- A TMDb API key (for movie/show details)

## Installation

Follow these steps to install and configure the system.

### 1. Clone the repository

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/media-frame.git
cd media-frame

2. Install dependencies

Use pip to install the required Python dependencies:

pip install -r requirements.txt

3. Setup Script

You can choose to automate the entire setup process using the setup.sh script or manually configure the system.
Option 1: Automated Setup (Recommended)

Run the setup.sh script to automate the setup process. This script will:

    Install dependencies.
    Create and configure the .env file.
    Run the setup.py script to obtain OAuth tokens.
    Install and configure the systemd service to run the application as a background process.

./setup.sh

Option 2: Manual Setup

If you prefer to configure the system manually, follow these steps:

    Create .env File: Copy the .env.example to .env and edit it with your credentials.

cp .env.example .env

Edit the .env file with your Spotify, Trakt, and TMDb credentials:

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

    Replace your_spotify_client_id, your_spotify_client_secret, etc., with your actual API credentials.

Run the Setup Script: Run the setup.py script to authenticate with Trakt and obtain the necessary OAuth tokens.

python setup.py

This will guide you through the process of authenticating with Trakt and will save your TRAKT_ACCESS_TOKEN and TRAKT_REFRESH_TOKEN to the .env file for future use.

Generate the Service (Optional): If you want to run the application as a background service, use the generate_service.py script to generate the systemd service.

python generate_service.py

This will create a service configuration and install it on your system.

Run the application:

Once everything is set up, you can run the application manually:

    python main.py

4. Running as a Background Service (Optional)

To run the application as a background service, follow these steps:

    Use the setup.sh script: This will automate the installation of the systemd service, as well as set up dependencies and .env variables.

./setup.sh

Check the Service Status: If you've installed the service, you can check the status of the background process with:

    sudo systemctl status media-frame.service

    The application will now run automatically in the background, starting with your system.

File Overview

    main.py: The main entry point for the application. This handles the integration with Spotify, Trakt, and TMDb, as well as the display updates.
    api_client.py: Contains functions to interact with the Spotify and Trakt APIs.
    image_manager.py: Manages album art and other image-related tasks.
    matrix_controller.py: Controls the display, including sending updates for album art and track information.
    token_manager.py: Handles the OAuth flow for obtaining and refreshing Trakt API tokens.
    config.py: Loads configuration settings from the .env file.
    setup.py: A script to set up OAuth for Trakt and generate the necessary tokens.
    generate_service.py: A script to generate the systemd service configuration for running the application as a background process.
    requirements.txt: A list of Python dependencies required for the project.
    .env: A configuration file containing sensitive API keys and tokens. This file is not committed to version control.
    README.md: The documentation for setting up and using the project.
    setup.sh: A script to automate the installation and setup process, including creating the .env file and installing the systemd service.

Troubleshooting

    If you experience any issues with the OAuth flow for Trakt, ensure that your TRAKT_REDIRECT_URI matches the URI registered in your Trakt Developer account.
    If you encounter any issues with Spotify integration, verify that your SPOTIFY_ACCESS_TOKEN is valid and hasn’t expired. You may need to refresh your token.
    Ensure your MQTT broker is set up correctly if you're using it to send updates to other systems like Home Assistant.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Contributing

If you find any bugs or want to contribute to the project, feel free to open an issue or submit a pull request.
