import maya.cmds as cmds
import maya.mel as mel

path = cmds.internalVar(userScriptDir = True) + "Skorge/Meshes/"

def human():
    cmds.file(path + "Basemesh_Human.obj", i = True, mergeNamespacesOnClash = True, namespace = ':')
