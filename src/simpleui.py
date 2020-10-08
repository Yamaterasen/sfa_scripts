import maya.OpenMayaUI as omui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance


def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SimpleUI(QtWidgets.QDialog):
    """Simple UI Class"""

    def __init__(self):
        """Constructor"""
        # Passing the object SimpleUI as an argument to super()
        # Makes this line python 2 and 3 compatible.
        super(SimpleUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("A Simple UI")
