import sys
import maya.cmds as cmds
import maya.mel as mel

# export as copy
def export(self):
    cmds.duplicate(rr = True)
    cmds.move(0, 0, 0, rpr = True)
    cmds.ExportSelection()
    cmds.delete()

BMPath = cmds.internalVar(userScriptDir = True) + "Skorge/Meshes/"

# export an OBJ directly to the Basemesh library
def basemeshExport(self):
	cmds.file(BMPath + meshName + ".obj", force = True, options = "groups=1;ptgroups=1;materials=0;smoothing=1;normals=1", typ = "OBJexport", pr = True, es = True)