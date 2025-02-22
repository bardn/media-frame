import os
import shutil

SERVICE_NAME = "media_frame"  # Updated to media_frame
SERVICE_PATH = "/etc/systemd/system/"
PROJECT_PATH = os.getcwd()  # Automatically get the current working directory
MAIN_PY_PATH = os.path.join(PROJECT_PATH, "media_frame.py")  # Updated to media_frame.py
USER = os.getlogin()  # Get the current logged in user
GROUP = os.getlogin()  # Assuming the user and group are the same

SERVICE_FILE = f"""
[Unit]
Description=Media Frame Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 {MAIN_PY_PATH}
WorkingDirectory={PROJECT_PATH}
User={USER}
Group={GROUP}
Restart=always

[Install]
WantedBy=multi-user.target
"""

def create_service():
    # Ensure the service directory exists
    if not os.path.exists(SERVICE_PATH):
        print(f"Error: Directory {SERVICE_PATH} does not exist.")
        return

    # Define the service file path
    service_file_path = os.path.join(SERVICE_PATH, f"{SERVICE_NAME}.service")

    # Write the service file
    with open(service_file_path, "w") as f:
        f.write(SERVICE_FILE)

    # Reload systemd and enable the service
    os.system("sudo systemctl daemon-reload")
    os.system(f"sudo systemctl enable {SERVICE_NAME}.service")
    os.system(f"sudo systemctl start {SERVICE_NAME}.service")
    print(f"{SERVICE_NAME} service installed and started successfully.")

if __name__ == "__main__":
    create_service()
