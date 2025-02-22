#!/bin/bash

# This script will install the required dependencies and guide the user through the configuration process

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

# Step 4: Success message
echo "Setup complete. Please review the .env file to ensure it contains your API keys and credentials."

# Optional: Provide a message for the next steps
echo "You can now run the application with: python media-frame.py"
