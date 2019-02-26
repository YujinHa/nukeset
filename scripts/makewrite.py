#coding:utf8
import os
import nuke
from PySide2.QtWidgets import *

class MakeWrite(QWidget):
	def __init__(self):
		super(MakeWrite, self).__init__()
		self.ok = QPushButton("OK")
		self.cancel = QPushButton("Cancel")
		self.ext = QComboBox()
		self.exts = [".exr", ".dpx", ".tga", ".mov"]
		self.ext.addItems(self.exts)
		self.fm = QComboBox()
		self.formats = ["2048x1152", "1920x1080", "2048x872", "2048x968"]
		self.fm.addItems(self.formats)
		self.reformat = QCheckBox("&reformat", self)
		self.reformat.setChecked(True)
		self.slate = QCheckBox("&slate", self)
		self.slate.setChecked(True)
		self.addtimecode = QCheckBox("&AddTimecode", self)
		self.addtimecode.setChecked(False)
		self.startframe = QLineEdit(str(int(nuke.Root()["first_frame"].value())))
		self.starttimecode = QLineEdit("00:00:00:00")

		# event
		self.ok.clicked.connect(self.pushOK)
		self.cancel.clicked.connect(self.close)

		# layout
		layout = QGridLayout()
		layout.addWidget(self.reformat, 0, 0)
		layout.addWidget(self.fm, 0, 1)
		layout.addWidget(self.addtimecode, 1, 0)
		layout.addWidget(self.startframe, 1, 1)
		layout.addWidget(self.starttimecode, 1, 2)
		layout.addWidget(self.slate, 2, 0)
		layout.addWidget(QLabel("Ext"), 3, 0)
		layout.addWidget(self.ext, 3, 1)
		layout.addWidget(self.cancel, 4, 0)
		layout.addWidget(self.ok, 4,1)
		self.setLayout(layout)

		# node list
		self.linkOrder = []


	def genReformat(self):
		reformat = nuke.nodes.Reformat()
		reformat["box_fixed"].setValue(True)
		reformat["type"].setValue("to box")
		width, height = self.fm.currentText().split("x")
		reformat["box_width"].setValue(int(width))
		reformat["box_height"].setValue(int(height))
		self.linkOrder.append(reformat)

	def genAddTimecode(self):
		timecode = nuke.nodes.AddTimeCode()
		timecode["startcode"].setValue(str(self.starttimecode.text()))
		timecode["useFrame"].setValue(True)
		timecode["frame"].setValue(int(self.startframe.text()))
		self.linkOrder.append(timecode)

	def genSlate(self):
		slate = nuke.nodes.slate()
		slate["vendor"].setValue("bae")
		self.linkOrder.append(slate)

	def genWrite(self):
		write = nuke.nodes.Write()
		dirname, basename = os.path.split(nuke.root().name())
		filename, notuse = os.path.splitext(basename)
		ext = str(self.ext.currentText())
		write["file_type"].setValue(ext[1:])
		write["file"].setValue("%s/out/%s/%s.####%s" % (dirname, filename, filename, ext))
		write["create_directories"].setValue(True)
		self.linkOrder.append(write)

	def linkNodes(self):
		"""
		linkOrder 노드 순서대로 노드를 연결, 생성한다.
		"""
		tail = nuke.selectedNode()
		for n in self.linkOrder:
			n.setInput(0, tail)
			tail = n

	def pushOK(self):
		"""
		OK버튼을 누르면 노드를 생성한다.
		"""
		if self.reformat.isChecked():
			self.genReformat()
		if self.addtimecode.isChecked():
			self.genAddTimecode()
		if self.slate.isChecked():
			self.genSlate()
		self.genWrite()
		self.linkNodes()
		self.close()


def checkCondition():
	if nuke.root().name() == "Root":
		nuke.message("파일을 저장해주세요.")
		return

	if len(nuke.selectedNodes()) != 1:
		nuke.message("노드를 하나만 선택하세요")
		return

def main():
	checkCondition()
	global customApp
	try:
		customApp.close()
	except:
		pass
	customApp = MakeWrite()
	try:
		customApp.show()
	except:
		pass
