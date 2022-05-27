

#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#                               IMPORTS
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import shutil
import json

#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#                           GLOBAL VERABLES
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

#setting content
SETTING = ""

#folders paths
GLOBAL = ""
SPAM = ""
DATA = ""
HISTORY = ""

#loaded data from files
LPC_INFO = {}


#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#                           FILE FUNCTIONS
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

"read line from the setting file"
def readSetting(settingName:str):
    return SETTING.split(settingName+'=')[-1].split(';')[0]

"move file with his path to the spam folder"
def moveToSpam(src:str):
    shutil.move(src, SPAM)

"move file from {src} to the {dest} folder"
def moveFromTo(src:str, dest:str):
    shutil.move(src, dest)

"returns the files full name"
def getFileName(event):
    return event.src_path.split("\\")[-1]

#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#                          LPC_INFO FUNCTIONS
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

"return list of the plc names from the {name._pcl} file"
def readInfo():
    with open(os.path.join(DATA, "fields._lpc"),'r') as f:
        jsonInfo = f.read()
        return json.loads(jsonInfo)

"update the data on {name._pcl} from LPC_INFO"
def pushInfo():
    with open(os.path.join(DATA, "fields._lpc"), 'w') as f:
        f.write(json.dumps(LPC_INFO, indent=2))
    
"add more data to the local {LPC_INFO} veriable"
def appendInfo(name:str, fields:list):
    try:
        path = os.path.join(HISTORY, name)
        os.mkdir(path)
    except OSError as error:
        print(error)

    LPC_INFO[name] = fields
    pushInfo()

"another name for {appenfInfo} function"
def addInfo(name:str, fields:list):
    appendInfo(name, fields)

"remove one data from the local {LPC_INFO} veriable"
def removeInfo(name:str):
    LPC_INFO.pop(name)
    pushInfo()

"chack if the {fields._lpc} is empty"
def IsInfoFileEmpty():
    with open(os.path.join(DATA, "fields._lpc"), 'r') as f:
        return (f.read() == "")

"chack if the pcl is in the {name._pcl} file"
def isKnownLPC(name:str):
    return bool(name in LPC_INFO)



#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#                          EXEL FUNCTIONS 
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

def isExelFile(name:str):
    



#get the path and return the MET of data
def readXLFile(path:str):
    pass
 

 
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#                             FREE SPACE
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -






























































#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#                        TRIGGER FUNCTIONS
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -


#triggerd when somthing moved to the {GLOBAL} folder
def on_created(event):
    #if this LPC name isn't known to the program
    print(getFileName(event).split('_')[0])
    if(not isKnownLPC(getFileName(event).split('_')[0])):
        moveToSpam(event.src_path)
        return
    moveFromTo(event.src_path, os.path.join(HISTORY, getFileName(event).split('_')[0]))

#triggerd when somthing moved form the {GLOBAL} folder
def on_deleted(event):
    print(f"{getFileName(event)} --> SPAM")
    return


#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#                        LISTENING FUNCTIONS
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

#create the action listeners
def createEventHandeler():
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    return PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

#here we choose what to listen to on the {GLOBAL} folder
def specifyHandlerFunctions(handler):
    handler.on_created = on_created
    handler.on_deleted = on_deleted

#create the observer that use all the listeners
def createObserver(handler, path):
    go_recursively = False
    observer = Observer()
    observer.schedule(handler, path, recursive=go_recursively)
    return observer

#start to listen for chenges on the {GOLOBAL} folder
def listenGlobal():
    handler = createEventHandeler()
    specifyHandlerFunctions(handler)
    observer = createObserver(handler, GLOBAL)
    observer.start()
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
        observer.join()

#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -


#here is where the code start running
def main():
    listenGlobal()

#read the setting file to {SETTING}
p = Path(__file__).with_name('setting')
with p.open('r') as f:
    SETTING = f.read()

#setting up all the string Path verables from the setting file
if __name__ == "__main__":
    GLOBAL = readSetting('GLOBAL')
    SPAM = readSetting('SPAM')
    DATA = readSetting('DATA')
    HISTORY = readSetting('HISTORY')

    #load the info
    if not IsInfoFileEmpty():
        print("Loading information from files")
        LPC_INFO = readInfo()


    #addInfo("food", ["temp", "qulity"])
    #removeInfo("food")
    #print(LPC_INFO)

    main()                                                                                                                    