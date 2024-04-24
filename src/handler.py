import os
import requests

from watchdog.events import PatternMatchingEventHandler


class CustomEventHandler(PatternMatchingEventHandler):
    def __init__(self):
        # Only trigger for new files
        super().__init__(patterns=["*"], ignore_directories=True)

    def on_created(self, event):
        print(f"New file {event.src_path} has been created.")
        self.handle_event(event.src_path, event.src_path)

    def handle_event(self, path, file_path):
        # Define actions based on the path
        if 'path1' in path:
            print("Action for path1")
            # self.trigger_synology_download('torrent_link_for_path1', file_path)
        elif 'path2' in path:
            print("Action for path2")
            # self.trigger_synology_download('torrent_link_for_path2', file_path)
        # Add more elif conditions for additional paths as needed

    def trigger_synology_download(self, torrent_link, file_path):
        synology_url = os.getenv('SYNOLOGY_URL')

        username = os.getenv('SYNOLOGY_USERNAME')
        password = os.getenv('SYNOLOGY_PASSWORD')

        try:
            # Login to Synology
            login_url = f"{synology_url}/webapi/entry.cgi?api=SYNO.API.Auth&version=6&method=login&account={username}&passwd={password}&session=DownloadStation&format=sid"
            response = requests.get(login_url)
            response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
            sid = response.json()['data']['sid']

            # Create download task
            download_url = f"{synology_url}/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&method=create&version=1&uri={torrent_link}&_sid={sid}"
            response = requests.get(download_url)
            response.raise_for_status()

            # Logout from Synology
            logout_url = f"{synology_url}/webapi/entry.cgi?api=SYNO.API.Auth&method=Logout&version=1&session=DownloadStation&_sid={sid}"
            response = requests.get(logout_url)
            response.raise_for_status()

            # Delete the file
            os.remove(file_path)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")
