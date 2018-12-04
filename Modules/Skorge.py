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
font.setPointSize(10)
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
		"border-radius: 5px;",
		"border-style: outset;",
		"border-width: 0px;",
        "min-width: 50px;",
        "min-height: 20px;"
	])

windowStyle = makeStyle([
	])

class W:
	def __init__(self, parent, name = ""):
		self.w = QMainWindow(parent)
		self.w.setObjectName(name)
		self.w.setMinimumSize(200, 100)
		self.w.setMaximumWidth(200)
		self.w.setStyleSheet(windowStyle)
		self.w.show()


class B:
	def __init__(self, text, style):
		self.t = text

		self.b = QPushButton(self.t, self)
		self.b.setFont(font)
		self.b.setMinimumSize(240, 60)
		self.b.setStyleSheet(style)
        self.b.clicked.connect(self.button_onClicked)
		#self.b.show()

# create the Skorge UI window
skorgeUI = W(parent = mainMayaWindow, name = "skorge main window")

# create a widget
skorgeWidget = QWidget()
skorgeUI.w.setCentralWidget(skorgeWidget)

# create a box layout
layout = QVBoxLayout(skorgeWidget)

# create the contained buttons and apply the button stylesheet
hello = B(text = "Hello there", style = buttonStyle)
layout.addWidget(hello.b)
kewl = B(text = "This iz kewl", style = buttonStyle)
layout.addWidget(kewl.b)

# add functionality
def hello_onClicked(self):
    print("Hello!")
