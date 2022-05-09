from time import sleep
from datetime import datetime
from venv import create
import pandas as pd

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):
    # def on_any_event(event):
    #     print(event)
    #     filename = event.src_path[index:]
    #     path = path
    
    @staticmethod
    def on_created(event):
        global i
        print(f"{event.src_path} created")
        filename = event.src_path[index:]
        created_time = datetime.now()
        modified_time = datetime.now()
        logdf.loc[i] = [filename, created_time, modified_time, path, "created"]
        i+=1

    @staticmethod
    def on_deleted(event):
        global i
        print(f"deleted {event.src_path}!")
        filename = event.src_path[index:]
        created_time = datetime.now()
        modified_time = datetime.now()
        logdf.loc[i] = [filename, created_time, modified_time, path, "deleted"]
        i+=1

    @staticmethod
    def on_modified(event):
        global i
        print(f"{event.src_path} has been modified")
        filename = event.src_path[index:]
        created_time = datetime.now()
        modified_time = datetime.now()
        logdf.loc[i] = [filename, created_time, modified_time, path, "modified"]
        i+=1

    @staticmethod
    def on_moved(event):
        global i
        print(f"moved {event.src_path} to {event.dest_path}")
        filename = event.dest_path[index:]
        created_time = datetime.now()
        modified_time = datetime.now()
        logdf.loc[i] = [filename, created_time, modified_time, path, f"moved from {event.src_path[index:]} to {event.dest_path[index:]}"]
        i+=1

# logdf = pd.DataFrame({'FileName':[],'CreatedTime':[],'ModifiedTime':[],'FileLocation':[],'Event':[]})
# logdf.to_csv('log.csv', index=False)
logdf = pd.read_csv('log.csv', index_col=[0])
print(logdf)
path="F:/temp/dir"
index = len(path)+1
i=len(logdf.index)
event_handler = Handler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while(True):
        sleep(1)
finally:
    logdf.to_csv('log.csv')
    observer.stop()
    observer.join()