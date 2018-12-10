import sys
import maya.cmds as cmds
import maya.mel as mel

# export as copy
def export(origin, centimeter):
    cmds.duplicate(rr = True)
    if origin:
    	cmds.move(0, 0, 0, rpr = True)
    if centimeter:
    	cmds.scale(100, 100, 100)
    cmds.ExportSelection()
    cmds.delete()

BMPath = cmds.internalVar(userScriptDir = True) + "Skorge/Meshes/"

# export an OBJ directly to the Basemesh library
def basemeshExport():
	# ask user how many instances to make
	prompt = cmds.promptDialog(title = "Skorge Mesh Library", message = "Mesh name", button = ["OK", "Cancel"], defaultButton = "OK", cancelButton = "Cancel", dismissString = "Eh, never mind.")

	# get the input from that prompt
	if prompt == "OK":
		meshName = cmds.promptDialog(query = True, text = True)

	cmds.file(BMPath + meshName + ".obj", force = True, options = "groups=0;ptgroups=0;materials=0;smoothing=1;normals=1", typ = "OBJexport", pr = True, es = True)