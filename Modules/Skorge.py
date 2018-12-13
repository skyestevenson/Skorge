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

# -------- GLOBAL VARIABLES --------
UIOrigin = (200, 100)
accentColor = (0, .4, 1)
buttonColor = (.2, .2, .2)
UIWidth = 146
UIHeight = 765

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
        self.window = cmds.window(title = "Skorge Alpha", topLeftCorner = UIOrigin, backgroundColor = [0.15, 0.15, 0.15], toolbox = True, s = False, w = UIWidth, h = UIHeight, rtf = False)
        cmds.scrollLayout(hst = 0)

        # Skorge icon
        cmds.iconTextButton(style = "iconOnly", image1 = iconPath + "SkorgeIcon.png")
        dash()

        # Project notes UI
        frame(label = "Notepad", closed = False)
        b(label = "Open project notes", command = partial(self.PNOpen), width = None)
        dash()
        closeFrame()

        # -------- UVing UI
        frame(label = "Quick UVs", closed = False, note = "")
        self.UVBWidth = 127
        cmds.columnLayout(nch = 6)
        b(label = "Harden + cut edge", command = "mel.eval('polySoftEdge -a 0; polyMapCut -ch 1;')", width = self.UVBWidth)
        dash()
        # texel density menu
        self.UVTexelDensityMenu = cmds.optionMenu(bgc = buttonColor, width = self.UVBWidth)
        cmds.menuItem(label = "Texel Density: 512", p = self.UVTexelDensityMenu)
        cmds.menuItem(label = "Texel Density: 1024", p = self.UVTexelDensityMenu)
        cmds.menuItem(label = "Texel Density: 2048", p = self.UVTexelDensityMenu)
        # Map Size menu
        self.UVMapSizeMenu = cmds.optionMenu(bgc = buttonColor, width = self.UVBWidth)
        cmds.menuItem(label = "Map Size: 512", p = self.UVMapSizeMenu)
        cmds.menuItem(label = "Map Size: 1024", p = self.UVMapSizeMenu)
        cmds.menuItem(label = "Map Size: 2048", p = self.UVMapSizeMenu)
        cmds.menuItem(label = "Map Size: 4096", p = self.UVMapSizeMenu)
        dash()
        self.UVAlsoLayoutCB = cmds.checkBox(label = "Also layout UVs", value = False)
        dash()
        b(label = "Set texel density", command = partial(self.UVSetDensity), width = self.UVBWidth)
        closeFrame()
        dash()
        closeFrame()

        # -------- Quick Collision UI
        frame(label = "Quick Colliders", closed = False, note = "Create properly named collision primitives.")
        cmds.columnLayout(nch = 4)
        self.CLMeshNameField = cmds.textField(width = 127)
        b(label = "Get mesh name", command = partial(self.CLGetName), ann = "", width = 127)
        dash()
        cmds.rowColumnLayout(numberOfRows = 2)
        self.QBWidth = 63
        b(label = "Box", command = partial(self.CLCreateCollider, colliderType = "box"), width = self.QBWidth)
        b(label = "Capsule", command = partial(self.CLCreateCollider, colliderType = "capsule"), width = self.QBWidth)
        b(label = "Sphere", command = partial(self.CLCreateCollider, colliderType = "sphere"), width = self.QBWidth)
        b(label = "Convex", command = partial(self.CLCreateCollider, colliderType = "convex"), width = self.QBWidth)
        closeFrame()
        closeFrame()
        dash()
        closeFrame()

        # -------- Basemesh UI
        frame(label = "Mesh Library", closed = False, note = "Load meshes from the Skorge library.")
        # show an icon displaying the currently selected mesh
        cmds.columnLayout(nch = 4)
        cmds.iconTextButton("BMPreview", style = "iconOnly", image1 = iconPath + "BMIcons/BMDefault.jpg", height = UIWidth)
        # create a dropdown menu to select the mesh
        self.meshSelectMenu = cmds.optionMenu(bgc = buttonColor, cc = partial(self.refreshUI), width = 127)
        dash()
        self.BMMenu = self.BMPopulateMenu()
        self.BMRefreshImage()
        # add a button for querying the thing
        b(label = "Load selected", command = partial(self.BM_LoadMesh), ann = "Load a copy of the selected mesh into the scene.", width = 127)
        b(label = "Add to library", command = partial(self.BMAddToLibrary), ann = "", width = 127)
        closeFrame()
        dash()
        closeFrame()

        # -------- Exporter UI
        frame(label = "Exporter", closed = False, note = "")
        cmds.columnLayout(nch = 4)
        self.originCB = cmds.checkBox(label = "Export from origin", ann = "Exports the mesh from the world space origin.", value = True)
        self.centimeterCB = cmds.checkBox(label = "Use centimeter scale", ann = "Scales the mesh up 100 times.", value = True)
        dash()
        b(label = "Export Copy", command = partial(self.EXExport), ann = "Export a copy from the scene origin.", width = 127)
        closeFrame()
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

    def UVSetDensity(self, other):
        # get the selected texel density and Map Size
        texelDensity = cmds.optionMenu(self.UVTexelDensityMenu, query = True, value = True)
        mapSize = cmds.optionMenu(self.UVMapSizeMenu, query = True, value = True)

        # make it actual integers
        if (texelDensity == "Texel Density: 512"):
            texelDensity = 512
        elif (texelDensity == "Texel Density: 1024"):
            texelDensity = 1024
        elif (texelDensity == "Texel Density: 2048"):
            texelDensity = 2048

        if (mapSize == "Map Size: 512"):
            mapSize = 512
        elif (mapSize == "Map Size: 1024"):
            mapSize = 1024
        elif (mapSize == "Map Size: 2048"):
            mapSize = 2048
        elif (mapSize == "Map Size: 4096"):
            mapSize = 4096

        # set the texel density using those values
        texSetCommand = "texSetTexelDensity {} {};".format(texelDensity, mapSize)
        mel.eval(texSetCommand)

        # check if the user wants to layout the UVs
        if (cmds.checkBox(self.UVAlsoLayoutCB, query = True, value = True)):
            # progress alert
            alert(None, "Setting texel density and laying out UVs...")

            # layout the UVs
            spacing = 0.01
            margin = 0.02
            layoutCommand = "u3dLayout -res {} -rmn 0 -rmx 360 -rst 30 -spc {} -mar {} -box 0 1 0 1 -ls 1;".format(mapSize, spacing, margin)
            mel.eval(layoutCommand)

            # progress alert
            alert(None, "Texel density and layout completed!")

    def PNOpen(self, other):
        self.PNNoteWidth = 250
        self.PNNoteHeight = 300
        self.PNNoteWindow = cmds.window(title = "Project notes", topLeftCorner = (UIOrigin[0], UIOrigin[1] + 175), backgroundColor = [0.15, 0.15, 0.15], toolbox = True, s = False, w = self.PNNoteWidth, h = self.PNNoteHeight, sizeable = False)
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