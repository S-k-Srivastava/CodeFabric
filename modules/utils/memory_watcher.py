import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread, Event

class MemoryWatcher:
    def __init__(self, file_path, on_change=None, debounce_seconds=1.0):
        self.file_path = os.path.abspath(file_path)
        self.observer = Observer()
        self.stop_event = Event()  # To signal thread to stop
        self.on_change = on_change
        self.debounce_seconds = debounce_seconds
        self._last_triggered = 0

    def on_modified(self, event):
        time.sleep(1)
        if not event.is_directory and os.path.abspath(event.src_path) == self.file_path:
            now = time.time()
            if now - self._last_triggered >= self.debounce_seconds:
                self._last_triggered = now
                if self.on_change:
                    self.on_change()

    def watch(self):
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = self.on_modified
        self.observer.schedule(event_handler, path=os.path.dirname(self.file_path), recursive=False)
        self.observer.start()
        
        while not self.stop_event.is_set():
            time.sleep(1)
        
        self.observer.stop()
        self.observer.join()

    def start(self):
        self.watch_thread = Thread(target=self.watch)
        self.watch_thread.daemon = True
        self.watch_thread.start()

    def stop(self):
        self.stop_event.set()