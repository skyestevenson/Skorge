from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

# get Skorge folder location
skorgePath = cmds.internalVar(userScriptDir = True) + "Skorge/"
iconPath = skorgePath + "Icons/"

# get current workspace path
projPath = cmds.workspace(q = True, rd = True)
projScripts = projPath + "scripts/"
print projPath
print projScripts

# allow Maya to see the Skorge modules
import sys
sys.path.append( skorgePath )

# -------- Skorge Modules --------
import Modules.Basemesh as Basemesh
reload (Basemesh)
import Modules.Exporter as Exporter
reload (Exporter)

# -------- HELPFUL FUNCTIONS --------
# alert user function
def alert(message):
    sys.stdout.write("Skorge: " + message)

# -------- PYSIDE UI SETUP BEGINS HERE --------

def getMayaWindow():
	ptr = omui.MQtUtil.mainWindow()
	if ptr is not None:
		return wrapInstance(long(ptr), QWidget)

mainMayaWindow = getMayaWindow()

font = QFont("Calibri")
font.setPointSize(14)
font.setBold(True)

def makeStyle(propList):
	inlineStyle = ""

	for item in propList:
		inlineStyle += item

	return inlineStyle

buttonStyle = makeStyle([
		"color: rgb(255, 255, 255);",
		"background-color: rgb(30, 30, 30);",
		"selection-color: rgb(255, 255, 255);",
		"selection-background-color: rgb(0, 187, 255);",
		"border-radius: 10px;",
		"border-style: outset;",
		"border-width: 0px;"
	])

windowStyle = makeStyle([
		"margin: 5px;"
	])

class W:
	def __init__(self, parent, name = ""):
		self.w = QMainWindow(parent)
		self.w.setObjectName(name)
		self.w.setMinimumSize(240, 100)
		self.w.setMaximumWidth(240)
		self.w.setStyleSheet(windowStyle)
		self.w.show()


class B:
	def __init__(self, text, style):
		self.t = text

		self.b = QPushButton(self.t)
		self.b.setFont(font)
		self.b.setMinimumSize(240, 60)
		self.b.setStyleSheet(style)
		self.b.show()

#layout = UI()

wind = W(parent = mainMayaWindow, name = "skorge main window")

# create a widget
widget = QWidget()
wind.w.setCentralWidget(widget)

# create a layout
layout = QVBoxLayout(widget)

foo = B(text = "Hello there", style = buttonStyle)
noob = B(text = "This iz kewl", style = buttonStyle)

layout.addWidget(foo.b)
layout.addWidget(noob.b)

wind.w.show()
