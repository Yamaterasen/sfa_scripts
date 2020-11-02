import logging

from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
from pymel.core.system import Path
import random

log = logging.getLogger(__name__)


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Scatter UI Class"""

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMinimumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scatter = Scatter()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.button_lay = self._create_button_ui()
        self.features_lay = self._create_features_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.features_lay)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.save_increment_btn = QtWidgets.QPushButton("Save Increment")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        layout.addWidget(self.save_increment_btn)
        return layout

    def _create_features_ui(self):
        layout = self._create_features_headers()
        self.density_le = QtWidgets.QLineEdit()
        self.density_le.setFixedWidth(50)
        self.scale_le = QtWidgets.QLineEdit()
        self.scale_le.setFixedWidth(50)
        self.rotation_le = QtWidgets.QLineEdit()
        self.rotation_le.setFixedWidth(50)
        # self.rotation_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.spacing = QtWidgets.QLabel("")
        layout.addWidget(self.density_le, 0, 1)
        layout.addWidget(self.scale_le, 1, 1)
        layout.addWidget(self.rotation_le, 2, 1)
        layout.addWidget(self.spacing, 0, 2)
        layout.addWidget(self.spacing, 0, 3)
        layout.addWidget(self.spacing, 0, 4)
        layout.addWidget(self.spacing, 0, 5)
        return layout

    def _create_features_headers(self):
        self.density_header_lbl = QtWidgets.QLabel("Density")
        self.density_header_lbl.setStyleSheet("font: bold")
        self.scale_header_lbl = QtWidgets.QLabel("Scale")
        self.scale_header_lbl.setStyleSheet("font: bold")
        self.rotation_header_lbl = QtWidgets.QLabel("Rotation")
        self.rotation_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.density_header_lbl, 0, 0)
        layout.addWidget(self.scale_header_lbl, 1, 0)
        layout.addWidget(self.rotation_header_lbl, 2, 0)
        return layout

    def create_connections(self):
        """Connect Signals and Slots"""
        self.scatter_btn.clicked.connect(self._scatter)
