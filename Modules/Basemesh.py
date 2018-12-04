import maya.cmds as cmds
import maya.mel as mel

BMPath = cmds.internalVar(userScriptDir = True) + "Skorge/Meshes/"

def makeHuman():
    BMHumanPath = BMPath + "Basemesh_Human.obj"
    cmds.file(BMHumanPath, i = True, mergeNamespacesOnClash = True, namespace = ':')
