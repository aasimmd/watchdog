from time import sleep

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        print(event)
        filename=event.src_path[index:]
        path=path

path="F:/temp/dir"
index=len(path)+1
event_handler=Handler()
observer=Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()
try:
    while(True):
        sleep(1)
finally:
    observer.stop()
    observer.join()