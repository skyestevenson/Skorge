import sys
import os
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

# make note file path
noteFile = projPath + "data/SkorgeProjectNotes.txt"

# allow Maya to see the Skorge Modules
sys.path.append(skorgePath)

# -------- Skorge Modules --------
import Modules.Basemesh as Basemesh
reload(Basemesh)
import Modules.Exporter as Exporter
reload(Exporter)
import Modules.Joke as Joke
reload(Joke)
import Modules.Colliders as Colliders
reload(Colliders)

# -------- HELPFUL FUNCTIONS --------
# alert user function
def alert(self, message):
    sys.stdout.write(message)

# -------- UI COLORS --------
accentColor = (0, .4, 1)
buttonColor = (.2, .2, .2)

# -------- UI FUNCTIONS --------
# just text
def t(label = "Default Text"):
    cmds.text(label = label, align = "left")
# a thin horizontal line separator
def dash():
    cmds.separator(horizontal = 1, height = 5, style = "single")
# a collapsable frame that contains UI elements
def frame(label, closed = False, note = ""):
    cmds.frameLayout(label = label, collapsable = True, cl = closed, ann = note, w = 128, bgc = accentColor)
# close a frame
def closeFrame():
    cmds.setParent( '..' )
# button UI
def b(label, command, width, ann = ""):
    if width is None:
        cmds.button(label = label, command = command, ann = ann, bgc = buttonColor)
    else:
        cmds.button(label = label, command = command, ann = ann, width = width, bgc = buttonColor)
# checkbox UI
def cb(label, onCommand, offCommand, ann, value = True):
    cmds.checkBox(label = label, onCommand = onCommand, offCommand = offCommand, ann = ann, value = value)
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

class GUI:
    # -------- MAIN FUNCTION --------
    def __init__(self):
        # set up main UI window
        self.UIWidth = 146
        self.UIHeight = 625 
        self.window = cmds.window(title = "Skorge Alpha", topLeftCorner = [350, 1500], backgroundColor = [0.15, 0.15, 0.15], toolbox = True, s = False, w = self.UIWidth, h = self.UIHeight, rtf = False)
        cmds.scrollLayout(hst = 0)

        # Skorge icon
        cmds.iconTextButton(style = "iconOnly", image1 = iconPath + "SkorgeIcon.png")
        dash()

        # Project notes UI
        frame(label = "Notepad", closed = False)
        b(label = "Open project notes", command = partial(self.PNOpen), width = None)
        dash()
        closeFrame()

        # -------- Grid Spacing UI
        frame(label = "Grid Spacing", closed = True)
        self.testSlider = IntSlider(min = 4, max = 16, increment = 4)
        dash()
        closeFrame()

        # -------- UVing UI
        frame(label = "UV Toolbox", closed = True, note = "")
        b(label = "Cut hard edges", command = "mel.eval('polyUVHardEdgesAutoSeams 1;')", width = None)
        dash()
        closeFrame()

        # -------- Quick Collision UI
        frame(label = "Quick Collision", closed = False, note = "Create properly named collision primitives.")
        self.CLMeshNameField = cmds.textField()
        b(label = "Get mesh name", command = partial(self.CLGetName), ann = "", width = None)
        cmds.rowColumnLayout(numberOfRows = 2)
        self.QBWidth = 63
        b(label = "Box", command = partial(self.CLCreateCollider, colliderType = "box"), width = self.QBWidth)
        b(label = "Capsule", command = partial(self.CLCreateCollider, colliderType = "capsule"), width = self.QBWidth)
        b(label = "Sphere", command = partial(self.CLCreateCollider, colliderType = "sphere"), width = self.QBWidth)
        b(label = "Convex", command = partial(self.CLCreateCollider, colliderType = "convex"), width = self.QBWidth)
        closeFrame()
        dash()
        closeFrame()

        # -------- Basemesh UI
        frame(label = "Mesh Library", closed = False, note = "Load meshes from the Skorge library.")
        # show an icon displaying the currently selected mesh
        cmds.iconTextButton("BMPreview", style = "iconOnly", image1 = iconPath + "BMIcons/Human.jpg", height = self.UIWidth)
        # create a dropdown menu to select the mesh
        self.meshSelectMenu = cmds.optionMenu(bgc = buttonColor, cc = partial(self.refreshUI))
        self.BMMenu = self.BMPopulateMenu()
        self.BMRefreshImage()
        # add a button for querying the thing
        b(label = "Load selected", command = partial(self.BM_LoadMesh), ann = "Load a copy of the selected mesh into the scene.", width = None)
        b(label = "Add to library", command = partial(self.BMAddToLibrary), ann = "", width = None)
        dash()
        closeFrame()

        # -------- Exporter UI
        frame(label = "Exporter", closed = False, note = "")
        self.originCB = cmds.checkBox(label = "Export from origin", ann = "Exports the mesh from the world space origin.", value = True)
        self.centimeterCB = cmds.checkBox(label = "Use centimeter scale", ann = "Scales the mesh up 100 times.", value = True)
        b(label = "Export Copy", command = partial(self.EXExport), ann = "Export a copy from the scene origin.", width = None)
        dash()
        closeFrame()

        # -------- Extras UI
        frame(label = "Extras", closed = True, note = "")
        b(label = "Tell me a joke", command = partial(Joke.tellJoke), ann = "", width = None)
        dash()
        closeFrame()

        # show main UI window
        cmds.showWindow(self.window)

    # -------- UTILITY FUNCTIONS --------
    # refresh the UI
    # NOTE: the use of "other" here is because, since these are classed functions being called via partial
    # ...as a result, there are two implicit "self" arguments that have to be passed
    def refreshUI(self, other):
        cmds.showWindow(self.window)
        # refresh the Basemesh mesh preview
        self.BMSelection = cmds.optionMenu(self.meshSelectMenu, query = True, value = True)
        self.BMRefreshImage()

    def PNOpen(self, other):
        self.PNNoteWidth = 250
        self.PNNoteHeight = 300
        self.PNNoteWindow = cmds.window(title = "Project notes", topLeftCorner = [350, 1500], backgroundColor = [0.15, 0.15, 0.15], toolbox = True, s = False, w = self.PNNoteWidth, h = self.PNNoteHeight, sizeable = False)
        cmds.columnLayout(adjustableColumn = True)
        # add textbox
        self.PNNoteField = cmds.scrollField(bgc = buttonColor, height = self.PNNoteHeight, cc = partial(self.PNSave), ww = True, font = "plainLabelFont")
        t("Notes save automatically to your project folder.")
        # load the notes from a file
        self.PNLoad()
        # show notepad window
        cmds.showWindow(self.PNNoteWindow)

    def PNLoad(self):
        # open the noteFile and load it into the scrollfield
        try:
            # import the file as a string
            PNFile = open(noteFile, "r")
            PNFileContents = PNFile.read()
            # assign it to the scrollfield
            cmds.scrollField(self.PNNoteField, e = True, text = PNFileContents)
        except:
            return None


    def PNSave(self, other):
        # get the notes from the scrollfield
        PNScrollText = cmds.scrollField(self.PNNoteField, q = True, text = True)
        # save the notes to disk
        PNFile = open(noteFile, "w")
        PNFile.write(PNScrollText)
        # alert the user that the notes have been saved
        import datetime
        alert(None, "Project notes saved, {}".format(datetime.datetime.now().strftime("%I:%M:%S %p")))

    def EXExport(self, other):
        origin = cmds.checkBox(self.originCB, query = True, value = True)
        centimeter = cmds.checkBox(self.centimeterCB, query = True, value = True)
        print(origin)
        print(centimeter)
        Exporter.export(origin = origin, centimeter = centimeter)

    def BM_LoadMesh(self, other):
        self.BMSelection = cmds.optionMenu(self.meshSelectMenu, query = True, value = True)
        print(self.BMSelection)
        Basemesh.loadMesh(self.BMSelection)

    def refreshBMMenu(self):
        self.BMMenu = Basemesh.populateMenu()

    def BMRefreshImage(self):
        self.BMSelection = cmds.optionMenu(self.meshSelectMenu, query = True, value = True)
        iconFile = iconPath + "BMIcons/{}.jpg".format(self.BMSelection)
        import os.path
        if (os.path.isfile(iconFile)):
            cmds.iconTextButton("BMPreview", style = "iconOnly", image1 = iconFile, e = True, w = 128, h = 128)
        else:
            cmds.iconTextButton("BMPreview", style = "iconOnly", image1 = iconPath + "BMIcons/BMDefault.jpg", e = True, w = 128, h = 128)

    def BMPopulateMenu(self):
        self.meshArray = Basemesh.populateMenu()
        for mesh in self.meshArray:
            cmds.menuItem(label = mesh, p = self.meshSelectMenu)

    def BMAddToLibrary(self, other):
        Exporter.basemeshExport()
        Basemesh.getMeshes()
        self.BMMenuItems = cmds.optionMenu(self.meshSelectMenu, q=True, itemListLong=True)
        cmds.deleteUI(self.BMMenuItems)
        self.BMPopulateMenu()
        self.BMRefreshImage()
        self.refreshUI(None)

    def CLGetName(self, other):
        # get name from selection
        selection = cmds.ls(sl = True)[0]
        cmds.textField(self.CLMeshNameField, e = True, text = selection)

    def CLCreateCollider(self, other, colliderType):
        # get the mesh name from the field
        meshName = cmds.textField(self.CLMeshNameField, q = True, text = True)
        Colliders.createCollider(colliderType = colliderType, meshName = meshName)
    
# instance the UI window
def main():
    SkorgeUI = GUI()