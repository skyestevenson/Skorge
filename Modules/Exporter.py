import sys
import maya.cmds as cmds
import maya.mel as mel

# export as copy
def export():
    cmds.duplicate(rr = True)
    cmds.move(0, 0, 0, rpr = True)
    cmds.ExportSelection()
    cmds.delete()