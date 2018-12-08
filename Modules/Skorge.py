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
    sys.stdout.write("Skorge says: " + message)

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
# refresh the UI
def refreshUI(self):
  cmds.showWindow(window)

  # refresh the Basemesh mesh preview
  BMSelection = cmds.optionMenu("meshSelectMenu", query = True, value = True)
  cmds.iconTextButton("BMPreview", style = "iconOnly", image1 = iconPath + "BMIcons/{}.jpg".format(BMSelection), e = True)

# query the value of the Basemesh mesh selection dropdown and load that mesh
BMSelection = cmds.optionMenu("meshSelectMenu", query = True, value = True)
def BM_LoadMesh(self):
  BMSelection = cmds.optionMenu("meshSelectMenu", query = True, value = True)
  Basemesh.loadMesh(BMSelection)

# -------- MAIN FUNCTION --------
def main():
  # set up main UI window
  window = cmds.window(title = "Skorge 1.0", topLeftCorner = [300, 1000], backgroundColor = [0.15, 0.15, 0.15], toolbox = True)
  global window
  cmds.columnLayout(adjustableColumn = True)

  # Skorge icon
  cmds.iconTextButton(style = "iconOnly", image1 = iconPath + "SkorgeIcon.png")
  dash()

  # -------- Grid Spacing UI
  frame(label = "Grid Spacing", closed = False)
  testSlider = IntSlider(min = 4, max = 16, increment = 4)

  # -------- Quick Collision UI
  frame(label = "Quick Collision", closed = False, note = "Create properly named collision primitives.")
  cmds.rowColumnLayout(numberOfRows = 2)
  QBWidth = 64
  b(label = "Box", command = "", width = QBWidth)
  b(label = "Capsule", command = "", width = QBWidth)
  b(label = "Sphere", command = "", width = QBWidth)
  b(label = "Convex", command = "", width = QBWidth)
  closeFrame()

  # -------- Basemesh UI
  frame(label = "Mesh Library", closed = False, note = "Load meshes from the Skorge library.")
  # show an icon displaying the currently selected mesh
  cmds.iconTextButton("BMPreview", style = "iconOnly", image1 = iconPath + "BMIcons/{}.jpg".format(BMSelection))
  # create a dropdown menu to select the mesh
  cmds.optionMenu("meshSelectMenu", bgc = color2, cc = partial(refreshUI))
  cmds.menuItem(label = "Human")
  cmds.menuItem(label = "Stove")
  closeFrame()
  # add a button for querying the thing
  b(label = "Create", command = partial(BM_LoadMesh), ann = "Load a copy of the selected mesh into the scene.", width = None)
  closeFrame()

  # -------- Exporter UI
  frame(label = "Exporter", closed = False, note = "")
  b(label = "Export Copy", command = partial(Exporter.export), ann = "Export a copy from the scene origin.", width = None)
  closeFrame()

  # -------- Extras UI
  frame(label = "Extras", closed = True, note = "")
  b(label = "Tell me a joke", command = partial(Joke.tellJoke), ann = "", width = None)
  closeFrame()

  # show main UI window
  cmds.showWindow(window)
