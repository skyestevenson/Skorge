import maya.cmds as cmds
import maya.mel as mel
import sys

# -------- Unreal's collision standards --------
# Box: UBX_[meshname]_#
# Capsule: UCP_[meshname]_# (Epic recommends 8 segments)
# Sphere: USP_[meshname]_# (Epic recommends 8 segments)
# Convex: UCX_[meshname]_#