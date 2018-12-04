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

# allow Maya to see the SkyeTools modules
import sys
sys.path.append( STPath )

# -------- SkyeTools Modules --------
import Modules.Basemesh as Basemesh
reload (Basemesh)
import Modules.QuickShelf as QuickShelf
reload (QuickShelf)
import Modules.Exporter as Exporter
reload (Exporter)

# -------- HELPFUL FUNCTIONS --------
# alert user function
def alert(message):
    sys.stdout.write("ST: " + message)

# -------- UI FUNCTIONS --------
# a thin horizontal line separator
def dash():
    cmds.separator(horizontal = 1, height = 5, style = "single")
# a collapsable frame that contains UI elements
def frame(inLabel, isCollapsed, inAnn):
    cmds.frameLayout(label = inLabel, collapsable = True, cl = isCollapsed, ann = inAnn)
# close a frame
def closeFrame():
    cmds.setParent( '..' )
# button UI
def b(inLabel, inCommand, inAnn):
    cmds.button(label = inLabel, command = inCommand, ann = inAnn)
# checkbox UI
def cb(inLabel, inOnCommand, inOffCommand, inAnn):
    cmds.checkBox(label = inLabel, onCommand = inOnCommand, offCommand = inOffCommand, ann = inAnn)
# shelf layout UI
def shelf():
    cmds.shelfLayout("QuickShelf", width = 100, height = 134)

# -------- MAIN FUNCTION --------
def main():
    # -------- MAIN UI --------
    # set up main UI window
    window = cmds.window(title = "SkyeTools 1.0", topLeftCorner = [300, 360], backgroundColor = [0.15, 0.15, 0.15], toolbox = True)
    cmds.columnLayout(adjustableColumn = True)

    # SkyeTools icon
    cmds.iconTextButton(style = "iconOnly", image1 = iconPath + "SkyeTools.png")
    dash()

    # Project Shelf UI
    frame("QuickShelf", False, "A persistent shelf which stays with your project. Middle mouse drag-and-drop to add items.")
    shelf()
    QuickShelf.importShelf()
    closeFrame()
    b("Save Shelf", "QuickShelf.exportShelf()", "Save to " + projScripts)
    closeFrame()
    dash()

    # QuickSelect UI
    frame("QuickSelect", True, "Quickly create and access selection sets.")
    b("Add New", "", "Create QuickSelect set from selection.")
    closeFrame()
    dash()

    # Mesh Actions UI
    frame("Mesh Actions", True, "Perform various actions on meshes.")
    b("Unite Meshes", "", "Combine and merge meshes.")
    closeFrame()
    dash()

    # Mirroring UI
    frame("Mirroring", True, "Mirror meshes comprehensively.")
    cb("Use Object Pivot", "", "", "")
    cb("Make Instance", "", "", "")
    b("Mirror X", "", "")
    b("Mirror Y", "", "")
    b("Mirror Z", "", "")
    closeFrame()
    dash()

    # Shading UI
    frame("Shading", True, "Assign default shader models.")
    b("Blinn", "", "")
    b("Lambert", "", "")
    closeFrame()
    dash()

    # Basemesh UI
    frame("Basemesh", False, "Create useful basemeshes for reference or to kickstart modeling.")
    b("Create Human", "Basemesh.makeHuman()", "Create a human basemesh. Default height is 180cm.")
    closeFrame()

    # Exporter UI
    frame("Exporter", False, "")
    b("Export Copy", "Exporter.export()", "Export a copy from the scene origin.")
    closeFrame()

    # show main UI window
    cmds.showWindow(window)
