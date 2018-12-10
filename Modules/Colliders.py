import maya.cmds as cmds
import maya.mel as mel
import sys

# alert user function
def alert(message):
    sys.stdout.write("Skorge says: " + message)

def createCollider(colliderType, meshName):
	if (meshName != ""):
		# make the correct collider primitive
		if (colliderType == "box"):
			# create box collider
			cmds.polyCube(name = "UBX_{}_#".format(meshName), w = 0.5, h = 0.5, d = 0.5, sx = 1, sy = 1, sz = 1, ax = [0, 1, 0])
		if (colliderType == "capsule"):
			# create capsule collider
			cmds.polyCylinder(name = "UCP_{}_#".format(meshName), r = 0.25, h = 1, sx = 8, sy = 1, sz = 1, ax = [0, 1, 0])
		if (colliderType == "sphere"):
			# create sphere collider
			cmds.polySphere(name = "USP_{}_#".format(meshName), r = 0.5, sx = 8, sy = 8, ax = [0, 1, 0])
		if (colliderType == "convex"):
			# create convex collider
			cmds.polyCube(name = "UCX_{}_#".format(meshName), w = 0.5, h = 0.5, d = 0.5, sx = 1, sy = 1, sz = 1, ax = [0, 1, 0])

		# if the mesh name correlates to a real object in the scene, move the primitive to the center of its bounding box!
		if cmds.objExists(meshName):
			# queries the bounding box of the object in world space
			bb = cmds.xform(meshName, q = True, bb = True, ws = True)

			# averages x, y and z bounds to find center point in world space
			center = ((bb[0]+bb[3])/2,(bb[1]+bb[4])/2,(bb[2]+bb[5])/2)

			# move the collider we just made to that center
			cmds.xform(ws = True, t = center)
	else:
		alert("No naming convention set. Select a visible mesh and press 'Get mesh name' or type one in.")