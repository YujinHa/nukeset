#coding:utf8
import os
import nuke
from PySide2.QtWidgets import *
from PySide2.QtCore import *

class NkLibrary(QWidget):
    currentItem = ""
    def __init__(self):
        super(NkLibrary, self).__init__()
        self.nklist = QListWidget()
        for i in range(100):
            self.nklist.addItem(QListWidgetItem("/test/"+str(i)+".nk")) # 이 부분을 파일리스트로 변경해야함.
        self.ok = QPushButton("OK")
        self.cancel = QPushButton("Cancel")
        self.oc = QDialogButtonBox(QtCore.Qt.Horizontal)
        
        # event
        self.ok.clicked.connect(self.bt_ok)
        self.nklist.itemClicked.connect(self.itemClick)
        self.cancel.clicked.connect(self.close)

        # layout
        self.setWindowTitle(Nuke Library)
        layout = QGridLayout()
        layout.addWidget(self.nklist, 0, 0)
        layout.addWidget(self.ok, 3, 0)
        layout.addWidget(self.cancel, 4, 0)
        layout.addWidget(self.oc, 5, 0)
        self.setLayout(layout)

    def itemClick(self, item):
        self.currentItem = item.text()

    def bt_ok(self):
        print "load %s" % (self.currentItem)
        self.close()

def main():
    # 이미 존재하는 customApp이 있다면 종료
    global customApp
    try:
        customApp.close()
    except:
        pass

    # customApp 변수로 NkLibrary를 실행
    customApp = NkLibrary()
    try:
        customApp.show()
    except:
        pass
