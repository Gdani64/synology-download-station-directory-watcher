import os
import requests

from watchdog.events import PatternMatchingEventHandler


class CustomEventHandler(PatternMatchingEventHandler):
    def __init__(self):
        # Only trigger for new files
        super().__init__(patterns=["*"], ignore_directories=True)

    def on_created(self, event):
        print(f"New file {event.src_path} has been created.")
        self.handle_event(event.src_path)

    def handle_event(self, path):
        print(path)
        # Define actions based on the path
        if 'TV Shows' in path:
            print("Action for TV Shows path")
            # self.trigger_synology_download('torrent_link_for_path1', file_path)
        elif 'Movies' in path:
            print("Action for Movies path")
            self.trigger_synology_download(path, '/Media/Movies')
        elif 'Books' in path:
            print("Action for Books path")
            # self.trigger_synology_download('torrent_link_for_path2', file_path)

    def trigger_synology_download(self, file_path, destination):
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
            url_create_task = f'{synology_url}/webapi/DownloadStation/task.cgi'

            # Prepare the multipart/form-data
            files = {'file': ('filename.torrent', open(file_path, 'rb'), 'application/x-bittorrent')}
            data = {
                'api': 'SYNO.DownloadStation.Task',
                'version': '1',
                'method': 'create',
                'destination': destination,
                '_sid': sid
            }

            # Create the task
            response = requests.post(url_create_task, files=files, data=data, verify=False)

            # Check response
            if response.status_code == 200 and response.json()['success']:
                print('Torrent task created successfully.')
            else:
                print('Failed to create torrent task:', response.json())

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
