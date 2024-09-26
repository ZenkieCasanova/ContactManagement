import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from contact_manager import ContactManager

class DirectoryWatcher:
    def __init__(self, watch_directory):
        self.watch_directory = watch_directory
        self.manager = ContactManager()
        self.event_handler = FileChangeHandler(self.manager)
        self.observer = Observer()

    def start(self):
        self.observer.schedule(self.event_handler, self.watch_directory, recursive=False)
        self.observer.start()
        print(f"Watching directory: {self.watch_directory}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, manager):
        self.manager = manager

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"New file detected: {event.src_path}")
        threading.Thread(target=self.manager.process_contact_file, args=(event.src_path,)).start()

if __name__ == "__main__":
    watcher = DirectoryWatcher('storage/app/contacts/')
    watcher.start()
