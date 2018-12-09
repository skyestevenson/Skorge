import maya.cmds as cmds
import maya.mel as mel
import os

path = cmds.internalVar(userScriptDir = True) + "Skorge/Meshes/"

# dictionary of meshes to be loaded on-demand
meshes = {}

# load in only OBJ meshes automatically from the folder
def getMeshes():
	for fileName in os.listdir(path):
	    if fileName.endswith(".obj"):
	    	# add that file to the meshes dictionary
	    	simpleName = fileName.replace(".obj", "")
	    	meshes[simpleName] = fileName

def populateMenu():
	for mesh in meshes:
		cmds.menuItem(label = mesh)

def loadMesh(mesh):
    cmds.file(path + meshes[mesh], i = True, mergeNamespacesOnClash = True, namespace = ':')

getMeshes()
