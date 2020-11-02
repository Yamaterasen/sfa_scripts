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
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout

    def _create_features_ui(self):
        layout = self._create_features_headers()
        self.density_sbx = QtWidgets.QDoubleSpinBox()
        self.density_sbx.setFixedWidth(50)
        self.scale_min_sbx = QtWidgets.QDoubleSpinBox()
        self.scale_min_sbx.setFixedWidth(50)
        self.scale_max_sbx = QtWidgets.QDoubleSpinBox()
        self.scale_max_sbx.setFixedWidth(50)
        self.rotation_sbx = QtWidgets.QDoubleSpinBox()
        self.rotation_sbx.setFixedWidth(50)
        # self.rotation_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.spacing = QtWidgets.QLabel("")
        layout.addWidget(self.density_sbx, 0, 1)
        layout.addWidget(self.scale_min_sbx, 2, 1)
        layout.addWidget(self.scale_max_sbx, 2, 2)
        layout.addWidget(self.rotation_sbx, 3, 1)
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
        self.scale_min_header_lbl = QtWidgets.QLabel("Min")
        self.scale_min_header_lbl.setStyleSheet("font: bold")
        self.scale_max_header_lbl = QtWidgets.QLabel("Max")
        self.scale_max_header_lbl.setStyleSheet("font: bold")
        self.rotation_header_lbl = QtWidgets.QLabel("Rotation")
        self.rotation_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.density_header_lbl, 0, 0)
        layout.addWidget(self.scale_min_header_lbl, 1, 1)
        layout.addWidget(self.scale_max_header_lbl, 1, 2)
        layout.addWidget(self.scale_header_lbl, 2, 0)
        layout.addWidget(self.rotation_header_lbl, 3, 0)
        return layout

    def create_connections(self):
        """Connect Signals and Slots"""
        self.scatter_btn.clicked.connect(self._scatter)

    @QtCore.Slot()
    def _scatter(self):
        """Scatter objects using player input"""
        self.rotation_max = self.rotation_sbx.value()
        self.scale_min = self.scale_min_sbx.value()
        self.scale_max = self.scale_max_sbx.value()
        self.scatter.scatter_objects((0, self.rotation_max),
                                     (self.scale_min, self.scale_max))


class Scatter(object):
    """Scatter objects using random transform, rotation, and scale"""

    def scatter_objects(self, rand_rotation, rand_scale):
        selection = cmds.ls(orderedSelection=True, flatten=True)
        vertex_names = cmds.filterExpand(selection, selectionMask=31,
                                         expand=True)

        # Create a group to contain scatter objects
        scatter_group = cmds.group(em=True, n='scatter_group')
        object_to_instance = selection[0]
        if cmds.objectType(object_to_instance) == 'transform':
            for vertex in vertex_names:
                new_instance = cmds.instance(object_to_instance)
                position = cmds.pointPosition(vertex, world=True)

                # Position and add random rotation and scale
                new_position = [x for x in position]
                new_rotation = [random.uniform(rand_rotation[0],
                                               rand_rotation[1])
                                for _ in range(3)]
                new_scale = [random.uniform(rand_scale[0], rand_scale[1])
                             for _ in range(3)]

                # Move objects to position
                cmds.move(new_position[0],
                          new_position[1],
                          new_position[2],
                          new_instance,
                          absolute=True,
                          worldSpace=True)

                # Set object rotation
                cmds.rotate(new_rotation[0],
                            new_rotation[1],
                            new_rotation[2],
                            new_instance,
                            relative=True,
                            objectSpace=True)

                # Set object scale
                cmds.scale(new_scale[0],
                           new_scale[1],
                           new_scale[2],
                           new_instance,
                           relative=True)

                # Parent new instances to the scatter group from earlier
                cmds.parent(new_instance, scatter_group)

        else:
            print("Please ensure the first object you select is a transform.")
