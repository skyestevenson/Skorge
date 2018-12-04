import maya.cmds as cmds
import maya.mel as mel

BMPath = cmds.internalVar(userScriptDir = True) + "SkyeTools/Meshes/"

def makeHuman():
    BMHumanPath = BMPath + "ST_Basemesh_Human.obj"
    cmds.file(BMHumanPath, i = True, mergeNamespacesOnClash = True, namespace = ':')