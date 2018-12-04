import sys
import maya.cmds as cmds
import maya.mel as mel

# get SkyeTools folder location
STPath = cmds.internalVar(userScriptDir = True) + "SkyeTools/"
iconPath = STPath + "Icons/"

# get current workspace path
projPath = cmds.workspace(q = True, rd = True)
projScripts = projPath + "scripts/"
print projPath
print projScripts

# get QuickShelf file path
quickShelfPath = projScripts + "QuickShelf.mel"

# save shelf to file
def exportShelf():
    cmds.saveShelf("QuickShelf", projScripts + "QuickShelf")
    sys.stdout.write("QuickShelf saved to project file.")
    
# load saved shelf
shelfFileExists = cmds.file(quickShelfPath, q = True, ex = True)

#print shelfFileExists
def importShelf():
    # check if file already exists
    if (shelfFileExists):
        mel.eval("source \"" + projScripts + "QuickShelf.mel\"")
        mel.eval("QuickShelf")
        alert("I found a QuickShelf file and loaded it automatically.")
    else:
        exportShelf()
        alert("I couldn't find a QuickShelf file, so I made a new one for you.")
        
# delete QuickShelf file and reload