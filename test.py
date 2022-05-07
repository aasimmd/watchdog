from time import sleep
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def on_any_event(event):
        print(event)
        filename=event.src_path[index:]
        path=path
    
    def on_created(event):
        print(f"hey, {event.src_path} has been created!")
        filename=event.src_path[index:]
        path=path
        created_time = datetime.now()
        modified_time = datetime.now()
 
    def on_deleted(event):
        print(f"what the f**k! Someone deleted {event.src_path}!")
        filename=event.src_path[index:]
        path=path
        modified_time = datetime.now()
 
    def on_modified(event):
        print(f"hey buddy, {event.src_path} has been modified")
        filename=event.src_path[index:]
        path=path
        modified_time = datetime.now()
 
    def on_moved(event):
        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
        filename=event.src_path[index:]
        path=path
        modified_time = datetime.now()


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