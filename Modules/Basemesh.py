import maya.cmds as cmds
import maya.mel as mel

path = cmds.internalVar(userScriptDir = True) + "Skorge/Meshes/"

# dictionary of meshes to be loaded on-demand
meshes = {
    "human": "Human.obj",
    "stove": "Stove.fbx"
}

def loadMesh(mesh):
    cmds.file(path + meshes[mesh], i = True, mergeNamespacesOnClash = True, namespace = ':')

#loadMesh("stove")
