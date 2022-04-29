from pickle import GLOBAL
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import shutil

GLOBAL = ""
SPAM = ""

# event.src_path
# event.dest_path
def on_created(event):
    fileName = event.src_path.split("\\")[-1]
    print('+',fileName)
    print(SPAM);
    shutil.move(event.src_path, SPAM)
    return

def on_deleted(event):
    fileName = event.src_path.split("\\")[-1]
    print('-',fileName)
    return

#--------

def createEventHandeler():
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    return PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def createObserver(handler, path):
    go_recursively = False
    observer = Observer()
    observer.schedule(handler, path, recursive=go_recursively)
    return observer

def specifyHandlerFunctions(handler):
    handler.on_created = on_created
    handler.on_deleted = on_deleted

def listenGlobal(path_global_):
    handler = createEventHandeler()
    specifyHandlerFunctions(handler)
    observer = createObserver(handler, path_global_)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

def run():
    listenGlobal(GLOBAL)

def main():
    run()

p = Path(__file__).with_name('setting')
with p.open('r') as f:
    settingStr = f.read()

GLOBAL = settingStr.split('GLOBAL=')[-1].split('\n')[0]
SPAM = settingStr.split('SPAM=')[-1].split('\n')[0]

if __name__ == "__main__":
    main()