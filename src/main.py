import os
from watcher import Watcher


def main():
    #  split paths separated by , and remove leading/trailing whitespace
    paths_to_watch = os.getenv('PATHS_TO_WATCH')

    if paths_to_watch is None:
        print("Environment variable PATHS_TO_WATCH is not set.")
        return

    # Split the paths by comma and remove any leading/trailing whitespace
    paths_to_watch = [path.strip() for path in paths_to_watch.split(',')]

    watcher = Watcher(paths_to_watch)
    watcher.run()


if __name__ == "__main__":
    main()
