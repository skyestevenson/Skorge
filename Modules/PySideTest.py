from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

def doOK():
	print "OK"

def doCancel():
	print "Cancel"

def getMayaWindow():
	ptr = omui.MQtUtil.mainWindow()
	if ptr is not None:
		return wrapInstance(long(ptr), QWidget)

mayaMainWindow = getMayaWindow()
print(mayaMainWindow)

loader = QUiLoader()
file = QFile("C:/myUI.ui")
file.open(QFile.ReadOnly)
ui = loader.load(file, parentWidget=mayaMainWindow)
file.close()

ui.typeComboBox.addItem( 'mesh' )
ui.typeComboBox.addItem( 'joint' )
ui.typeComboBox.addItem( 'camera' )

ui.okButton.clicked.connect( doOK )
ui.cancelButton.clicked.connect( doCancel )

ui.setWindowFlags( Qt.Window )
ui.show()
