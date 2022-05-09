from time import sleep
from datetime import datetime
import pandas as pd
from getpass import getuser

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def autostart():
    script = 'py '+__file__
    bg_script = 'START /MIN /B CMD.EXE /C watchdog.bat'
    username = getuser()
    bg_bat_path = bat_path = f'C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\bg.bat'
    bat_path = f'C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\watchdog.bat'
    f = open(bg_bat_path, 'w+')
    f.write(bg_script)
    f = open(bat_path, 'w+')
    f.write(script)


def autofill():
    try:
        f = open('log.csv')
        f.close()
    except:
        logdf = pd.DataFrame({'FileName':[],'CreatedTime':[],'ModifiedTime':[],'FileLocation':[],'Event':[]})
        logdf.to_csv('log.csv')

class Handler(FileSystemEventHandler):
    # def on_any_event(event):
    #     print(event)
    #     filename = event.src_path[index:]
    #     path = path
    
    @staticmethod
    def on_created(event):
        print(f"{event.src_path} created")
        fpath = event.src_path
        index = fpath.rfind("\\")
        filename = fpath[index+1:]
        path = fpath[:index]
        created_time = datetime.now()
        modified_time = datetime.now()
        logdf.loc[len(logdf.index)] = [filename, created_time, modified_time, path, "created"]

    @staticmethod
    def on_deleted(event):
        print(f"deleted {event.src_path}!")
        fpath = event.src_path
        index = fpath.rfind("\\")
        filename = fpath[index+1:]
        path = fpath[:index]
        try:
            created_time = logdf.loc[logdf['FileName'] == filename]['CreatedTime'][0]
        except:
            created_time = datetime.now()
        modified_time = datetime.now()
        logdf.loc[len(logdf.index)] = [filename, created_time, modified_time, path, "deleted"]

    @staticmethod
    def on_modified(event):
        if not event.is_directory:
            print(f"{event.src_path} has been modified")
            fpath = event.src_path
            index = fpath.rfind("\\")
            filename = fpath[index+1:]
            path = fpath[:index]
            try:
                created_time = logdf.loc[logdf['FileName'] == filename]['CreatedTime'][0]
            except:
                created_time = datetime.now()
            modified_time = datetime.now()
            logdf.loc[len(logdf.index)] = [filename, created_time, modified_time, path, "modified"]

    @staticmethod
    def on_moved(event):
        print(f"moved {event.src_path} to {event.dest_path}")
        fpath = event.src_path
        index = fpath.rfind("\\")
        filename = fpath[index+1:]
        path = fpath[:index]
        try:
            created_time = logdf.loc[logdf['FileName'] == filename]['CreatedTime'][0]
        except:
            created_time = datetime.now()
        modified_time = datetime.now()
        logdf.loc[len(logdf.index)] = [filename, created_time, modified_time, path, f"moved from {event.src_path[index:]} to {event.dest_path[index:]}"]
        
autostart()
autofill()
logdf = pd.read_csv('log.csv', index_col=0)
# print(logdf)

path="F:/temp/dir"
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