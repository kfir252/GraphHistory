import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# event.src_path
# event.dest_path
def on_created(event):
    fileName = event.src_path.split("\\")[-1]
    print(f"{fileName} created!")

def on_deleted(event):
    fileName = event.src_path.split("\\")[-1]
    print(f"{fileName} deleted!")

def on_moved(event):
    destName = event.dest_path.split("\\")[-1]
    srcName = event.src_path.split("\\")[-1]
    print(f"{srcName} moved to {destName}")

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
    handler.on_moved = on_moved

def main():
    path = "C:/Users/kfirl/Desktop/DataBase work/GraphHistory/GraphHistory/global"
    my_event_handler = createEventHandeler()
    specifyHandlerFunctions(my_event_handler)
    my_observer = createObserver(my_event_handler, path)
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


if __name__ == "__main__":
    main()