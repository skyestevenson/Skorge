import maya.cmds as cmds
import maya.mel as mel

path = cmds.internalVar(userScriptDir = True) + "Skorge/Meshes/"

# dictionary of meshes to be loaded on-demand
meshes = {
    "Human": "Human.obj",
    "Stove": "Stove.obj"
}

def loadMesh(mesh):
    cmds.file(path + meshes[mesh], i = True, mergeNamespacesOnClash = True, namespace = ':')

#loadMesh("stove")
