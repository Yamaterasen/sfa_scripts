from PySide2 import QtWidgets


class SimpleUI(QtWidgets.QDialog):
    """Simple UI Class"""

    def __init__(self):
        """Constructor"""
        # Passing the object SimpleUI as an argument to super()
        # Makes this line python 2 and 3 compatible.
        super(SimpleUI, self).__init__()
        self.setWindowTitle("A Simple UI")
