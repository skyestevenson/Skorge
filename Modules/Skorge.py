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
import Modules.Colliders as Colliders
reload(Colliders)

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
        self.window = cmds.window(title = "Skorge Alpha", topLeftCorner = [350, 1500], backgroundColor = [0.15, 0.15, 0.15], toolbox = True)
        cmds.columnLayout(adjustableColumn = True)

        # Skorge icon
        cmds.iconTextButton(style = "iconOnly", image1 = iconPath + "SkorgeIcon.png")
        dash()

        # -------- Grid Spacing UI
        frame(label = "Grid Spacing", closed = False)
        self.testSlider = IntSlider(min = 4, max = 16, increment = 4)
        closeFrame()

        # -------- UVing UI
        frame(label = "UV Toolbox", closed = False, note = "")
        b(label = "Cut hard edges", command = "mel.eval('polyUVHardEdgesAutoSeams 1;')", width = None)
        closeFrame()

        # -------- Quick Collision UI
        frame(label = "Quick Collision", closed = False, note = "Create properly named collision primitives.")
        self.CLMeshNameField = cmds.textField()
        b(label = "Get mesh name", command = partial(self.CLGetName), ann = "", width = None)
        cmds.rowColumnLayout(numberOfRows = 2)
        self.QBWidth = 64
        b(label = "Box", command = partial(self.CLCreateCollider, colliderType = "box"), width = self.QBWidth)
        b(label = "Capsule", command = partial(self.CLCreateCollider, colliderType = "capsule"), width = self.QBWidth)
        b(label = "Sphere", command = partial(self.CLCreateCollider, colliderType = "sphere"), width = self.QBWidth)
        b(label = "Convex", command = partial(self.CLCreateCollider, colliderType = "convex"), width = self.QBWidth)
        closeFrame()
        closeFrame()

        # -------- Basemesh UI
        frame(label = "Mesh Library", closed = False, note = "Load meshes from the Skorge library.")
        # show an icon displaying the currently selected mesh
        cmds.iconTextButton("BMPreview", style = "iconOnly", image1 = iconPath + "BMIcons/Human.jpg")
        # create a dropdown menu to select the mesh
        self.meshSelectMenu = cmds.optionMenu(bgc = color2, cc = partial(self.refreshUI))
        self.BMMenu = self.BMPopulateMenu()
        self.BMRefreshImage()
        # add a button for querying the thing
        b(label = "Load selected", command = partial(self.BM_LoadMesh), ann = "Load a copy of the selected mesh into the scene.", width = None)
        b(label = "Add to library", command = partial(self.BMAddToLibrary), ann = "", width = None)
        closeFrame()

        # -------- Exporter UI
        frame(label = "Exporter", closed = False, note = "")
        self.originCB = cmds.checkBox(label = "Export from origin", ann = "Exports the mesh from the world space origin.", value = True)
        self.centimeterCB = cmds.checkBox(label = "Use centimeter scale", ann = "Scales the mesh up 100 times.", value = True)
        b(label = "Export Copy", command = partial(self.EXExport), ann = "Export a copy from the scene origin.", width = None)
        closeFrame()

        # -------- Extras UI
        frame(label = "Extras", closed = True, note = "")
        b(label = "Tell me a joke", command = partial(Joke.tellJoke), ann = "", width = None)
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
            cmds.iconTextButton("BMPreview", style = "iconOnly", image1 = iconFile, e = True)
        else:
            cmds.iconTextButton("BMPreview", style = "iconOnly", image1 = iconPath + "BMIcons/BMDefault.jpg", e = True)

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
SkorgeUI = GUI()