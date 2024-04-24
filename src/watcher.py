import time
from watchdog.observers import Observer
from handler import CustomEventHandler


class Watcher:
    def __init__(self, paths_to_watch):
        self.observer = Observer()
        self.event_handler = CustomEventHandler()  # Use the custom event handler
        self.paths_to_watch = paths_to_watch

    def run(self):
        for path in self.paths_to_watch:
            self.observer.schedule(self.event_handler, path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
