import sys
import maya.cmds as cmds
import maya.mel as mel

# get Skorge folder location
skorgePath = cmds.internalVar(userScriptDir = True) + "Skorge/"
sys.path.append(skorgePath)

# import main script with UI functions
from Modules.Skorge import *

# -------- MAIN UI --------
def mainWindow():
  # set up main UI window
  window = cmds.window(title = "Skorge 1.0", topLeftCorner = [300, 360], backgroundColor = [0.15, 0.15, 0.15], toolbox = True)
  cmds.columnLayout(adjustableColumn = True)

  # Skorge icon
  cmds.iconTextButton(style = "iconOnly", image1 = iconPath + "SkyeTools.png")
  dash()

  # Basemesh UI
  frame(label = "Basemesh", closed = False, note = "Create useful basemeshes for reference or to kickstart modeling.")
  b("Create Human", "Basemesh.human()", "Create a human basemesh. Default height is 180cm.")
  closeFrame()

  # Exporter UI
  frame(label = "Exporter", closed = False, note = "")
  b("Export Copy", "Exporter.export()", "Export a copy from the scene origin.")
  closeFrame()

  # show main UI window
  cmds.showWindow(window)
