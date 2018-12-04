import sys
import maya.cmds as cmds
import maya.mel as mel

# get Skorge folder location
skorgePath = cmds.internalVar(userScriptDir = True) + "Skorge/"
iconPath = skorgePath + "Icons/"

# get current workspace path
projPath = cmds.workspace(q = True, rd = True)
projScripts = projPath + "scripts/"
print projPath
print projScripts

# allow Maya to see the Skorge Modules
sys.path.append(skorgePath)

# -------- Skorge Modules --------
import Modules.SkorgeUI as UI
reload(UI)
import Modules.Basemesh as Basemesh
reload (Basemesh)
import Modules.Exporter as Exporter
reload (Exporter)

# -------- HELPFUL FUNCTIONS --------
# alert user function
def alert(message):
    sys.stdout.write("Skorge: " + message)

# -------- UI FUNCTIONS --------
# a thin horizontal line separator
def dash():
    cmds.separator(horizontal = 1, height = 5, style = "single")
# a collapsable frame that contains UI elements
def frame(label, closed = False, note = ""):
    cmds.frameLayout(label = label, collapsable = True, cl = closed, ann = note)
# close a frame
def closeFrame():
    cmds.setParent( '..' )
# button UI
def b(inLabel, inCommand, inAnn):
    cmds.button(label = inLabel, command = inCommand, ann = inAnn)
# checkbox UI
def cb(inLabel, inOnCommand, inOffCommand, inAnn):
    cmds.checkBox(label = inLabel, onCommand = inOnCommand, offCommand = inOffCommand, ann = inAnn)

# -------- MAIN FUNCTION --------
def main():
    UI.mainWindow()
