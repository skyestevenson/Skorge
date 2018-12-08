import maya.cmds as cmds
import maya.mel as mel
import sys

# export as copy
def export(self):
    cmds.duplicate(rr = True)
    cmds.move(0, 0, 0, rpr = True)
    cmds.ExportSelection()
    cmds.delete()
