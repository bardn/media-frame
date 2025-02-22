#!/bin/bash

# This script will install the required dependencies, guide the user through the configuration process,
# and set up the background service for the application.

# Step 1: Install required packages
echo "Installing dependencies..."
pip install -r requirements.txt

# Step 2: Check if .env file exists, if not, copy the example
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
else
    echo ".env file already exists, skipping creation."
fi

# Step 3: Run the setup process (which will ask for Trakt and other required credentials)
echo "Running setup script..."
python setup.py

# Step 4: Install the service to run in the background
echo "Installing systemd service..."
sudo cp media-frame.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable media-frame.service
sudo systemctl start media-frame.service

# Step 5: Success message
echo "Setup complete. The application is now running as a background service."

# Optional: Provide a message for the next steps
echo "You can check the service status with: sudo systemctl status media-frame.service"
echo "The application will automatically start on boot."
