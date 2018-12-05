import sys
import maya.cmds as cmds
import maya.mel as mel

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
import Modules.Exporter as Exporter
import Modules.Joke as Joke

# -------- HELPFUL FUNCTIONS --------
# alert user function
def alert(message):
    sys.stdout.write("Skorge: " + message)

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
def b(inLabel, inCommand, inAnn):
    cmds.button(label = inLabel, command = inCommand, ann = inAnn)
# checkbox UI
def cb(inLabel, inOnCommand, inOffCommand, inAnn):
    cmds.checkBox(label = inLabel, onCommand = inOnCommand, offCommand = inOffCommand, ann = inAnn)
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


# -------- MAIN FUNCTION --------
def main():
  # set up main UI window
  window = cmds.window(title = "Skorge 1.0", topLeftCorner = [300, 1000], backgroundColor = [0.15, 0.15, 0.15], toolbox = True)
  cmds.columnLayout(adjustableColumn = True)

  # Skorge icon
  cmds.iconTextButton(style = "iconOnly", image1 = iconPath + "SkorgeIcon.png")
  dash()

  frame(label = "Grid Spacing", closed = False)
  testSlider = IntSlider(min = 4, max = 16, increment = 4)

  # Basemesh UI
  frame(label = "Basemesh", closed = False, note = "Create useful basemeshes for reference or to kickstart modeling.")
  b("Create Human", "from Modules.Basemesh import human; human()", "Create a human basemesh. Default height is 180cm.")
  closeFrame()

  # Exporter UI
  frame(label = "Exporter", closed = False, note = "")
  b("Export Copy", "print('fuck')", "Export a copy from the scene origin.")
  closeFrame()

  # Exporter UI
  frame(label = "Jokes", closed = False, note = "")
  b("Tell me a joke", "from Modules.Joke import tellJoke; tellJoke()", "")
  closeFrame()

  # show main UI window
  cmds.showWindow(window)
