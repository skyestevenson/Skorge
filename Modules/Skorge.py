import sys
import maya.cmds as cmds
import maya.mel as mel
from functools import partial

######## END DEBUGGING BULLSHIT ########

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
import Modules.Basemesh as Basemesh
reload(Basemesh)
import Modules.Exporter as Exporter
reload(Exporter)
import Modules.Joke as Joke
reload(Joke)

# -------- HELPFUL FUNCTIONS --------
# alert user function
def alert(message):
    sys.stdout.write("Skorge: " + message)

# -------- UI COLORS --------
color2 = (.2, .2, .2)

# -------- UI FUNCTIONS --------
# just text
def t(label = "Default Text"):
    cmds.text(label = label, align = "left")
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
def b(label, command, width, ann = ""):
    if width is None:
        cmds.button(label = label, command = command, ann = ann, bgc = color2)
    else:
        cmds.button(label = label, command = command, ann = ann, width = width, bgc = color2)
# checkbox UI
def cb(label, inOnCommand, inOffCommand, ann):
    cmds.checkBox(label = label, onCommand = inOnCommand, offCommand = inOffCommand, ann = ann)
# column button group
def bg(buttonWidth = 25):
    cmds.rowColumnLayout(numberOfRows = 1)
    b(label = "2", command = "print(2)", width = buttonWidth)
    b(label = "4", command = "print(4)", width = buttonWidth)
    b(label = "8", command = "print(8)", width = buttonWidth)
    b(label = "16", command = "print(16)", width = buttonWidth)
    closeFrame()
# slider UI
class IntSlider:
    def __init__(self, label = "", isFloat = False, min = 0, max = 10, increment = 1):
        self.value = 4
        if (label != ""):
            self.text = t(label)
        self.slider = cmds.intSliderGrp(cc = self.updateSlider, f = True, cw2 = (25,50), value = self.value, min = min, max = max)

    def updateSlider(self, *_):
        self.value = cmds.intSliderGrp(self.slider, q = True, v = True)

        print(self.value)

# -------- UTILITY FUNCTIONS --------
# we need to query the value of the mesh selection dropdown
def BM_LoadMesh(self):
  selection = cmds.optionMenu("meshSelectMenu", query = True, value = True)
  print(selection)
  Basemesh.loadMesh(selection)

# -------- MAIN FUNCTION --------
def main():
  # set up main UI window
  window = cmds.window(title = "Skorge 1.0", topLeftCorner = [300, 1000], backgroundColor = [0.15, 0.15, 0.15], toolbox = True)
  cmds.columnLayout(adjustableColumn = True)

  # Skorge icon
  cmds.iconTextButton(style = "iconOnly", image1 = iconPath + "SkorgeIcon.png")
  dash()

  # Grid Spacing
  frame(label = "Grid Spacing", closed = False)
  testSlider = IntSlider(min = 4, max = 16, increment = 4)

  # Basemesh UI
  frame(label = "Basemesh", closed = False, note = "Create useful basemeshes for reference or to kickstart modeling.")
  # create a dropdown menu to select the mesh
  cmds.optionMenu("meshSelectMenu", bgc = color2)
  cmds.menuItem(label = "Human")
  cmds.menuItem(label = "Stove")
  closeFrame()
  # add a button for querying the thing
  b(label = "Create", command = partial(BM_LoadMesh), ann = "", width = None)
  closeFrame()

  # Exporter UI
  frame(label = "Exporter", closed = False, note = "")
  b(label = "Export Copy", command = partial(Exporter.export), ann = "Export a copy from the scene origin.", width = None)
  closeFrame()

  # Exporter UI
  frame(label = "Jokes", closed = False, note = "")
  b(label = "Tell me a joke", command = partial(Joke.tellJoke), ann = "", width = None)
  closeFrame()

  # show main UI window
  cmds.showWindow(window)
