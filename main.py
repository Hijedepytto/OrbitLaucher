import minecraft_launcher_lib
import subprocess
from uuid import uuid1
from random_username.generate import generate_username
from PyQt5 import QtCore, QtGui, QtWidgets

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', 'OrbitLaincher')
class LauncherThread(QtCore.QThread):
    launch_setup_signal = QtCore.pyqtSignal(str, str)
    progress_update_signal = QtCore.pyqtSignal(int, int, str)
    state_update_signal = QtCore.pyqtSignal(bool)

    version_id = ''
    username = ''

    progress = 0
    progress_max = 0
    progress_label = ''

    def __init__(self):
        super().__init__()

        self.launch_setup_signal.connect(self.launch_setup)

    def launch_setup(self, version_id, username):
        self.version_id = version_id
        self.username = username

    def update_progress_label(self, value):
        self.progress_label = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)
    def update_progress(self, value):
        self.progress = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)
    def update_progress_max(self, value):
        self.progress_max = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def run(self):
        self.state_update_signal.emit(True)
        minecraft_launcher_lib.install.install_minecraft_version(versionid=self.version_id, minecraft_directory=minecraft_directory, callback={'setStatus': self.update_progress_label, 'setProgress': self.update_progress, 'setMax': self.update_progress_max})
        
        if self.username == '':
            self.username = generate_username()[0]

        options = {
            'username': self.username,
            'uuid': str(uuid1()),
            'token': ''
        }

        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=self.version_id, minecraft_directory=minecraft_directory, options=options))

        self.state_update_signal.emit(False)

class Ui_OrbitLauncher(object):
    def setupUi(self, OrbitLauncher):
        OrbitLauncher.setObjectName("OrbitLauncher")
        OrbitLauncher.setWindowModality(QtCore.Qt.NonModal)
        OrbitLauncher.setEnabled(True)
        OrbitLauncher.resize(675, 425)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OrbitLauncher.sizePolicy().hasHeightForWidth())
        OrbitLauncher.setSizePolicy(sizePolicy)
        OrbitLauncher.setMinimumSize(QtCore.QSize(675, 425))
        OrbitLauncher.setMaximumSize(QtCore.QSize(675, 425))
        OrbitLauncher.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        OrbitLauncher.setFocusPolicy(QtCore.Qt.NoFocus)
        OrbitLauncher.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        OrbitLauncher.setWindowTitle("OrbitLauncher")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        OrbitLauncher.setWindowIcon(icon)
        OrbitLauncher.setStatusTip("")
        OrbitLauncher.setAccessibleName("")
        OrbitLauncher.setAccessibleDescription("")
        OrbitLauncher.setLayoutDirection(QtCore.Qt.LeftToRight)
        OrbitLauncher.setAutoFillBackground(False)
        OrbitLauncher.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 8pt \"MS Shell Dlg 2\";\n"
"background-color: rgba(255, 255, 255, 0);\n"
"border-color: rgb(255, 108, 110);\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        OrbitLauncher.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(OrbitLauncher)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(0, 0, 675, 425))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label.setAcceptDrops(False)
        self.label.setToolTip("")
        self.label.setAutoFillBackground(False)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("assets/LaucherBG.png"))
        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.start_progress = QtWidgets.QProgressBar(self.centralwidget)
        self.start_progress.setEnabled(False)
        self.start_progress.setGeometry(QtCore.QRect(0, 400, 683, 23))
        self.start_progress.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.start_progress.setProperty("value", 24)
        self.start_progress.setVisible(False)
        self.start_progress.setObjectName("progressBar")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 110, 121, 91))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.version_select = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.version_select.setStyleSheet("")
        self.version_select.setCurrentText("")
        self.version_select.setFrame(True)
        self.version_select.setObjectName("comboBox")

        for version in minecraft_launcher_lib.utils.get_version_list():
            self.version_select.addItem(version['id'])

        self.gridLayout.addWidget(self.version_select, 3, 0, 1, 1)
        self.password = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.password.setInputMask("")
        self.password.setText("")
        self.password.setFrame(True)
        self.password.setObjectName("lineEdit")
        self.password.setPlaceholderText("Password")
        self.gridLayout.addWidget(self.password, 1, 0, 2, 1)
        self.username = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.username.setFrame(True)
        self.username.setObjectName("lineEdit_2")
        self.username.setPlaceholderText("Username")
        self.gridLayout.addWidget(self.username, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 340, 181, 51))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("assets/play-button-idle.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(10, 340, 181, 51))
        self.start_button.clicked.connect(self.launch_game)
        self.start_button.setObjectName("push_button")
        OrbitLauncher.setCentralWidget(self.centralwidget)

        self.launch_thread = LauncherThread()
        self.launch_thread.state_update_signal.connect(self.state_update)
        self.launch_thread.progress_update_signal.connect(self.update_progress)

        QtCore.QMetaObject.connectSlotsByName(OrbitLauncher)

    def state_update(self, value):
        self.start_button.setDisabled(value)
        self.start_progress.setVisible(value)
    def update_progress(self, progress, max_progress, label):
        self.start_progress.setValue(progress)
        self.start_progress.setMaximum(max_progress)

    def launch_game(self):
        self.launch_thread.launch_setup_signal.emit(self.version_select.currentText(), self.username.text())
        self.launch_thread.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OrbitLauncher = QtWidgets.QMainWindow()
    ui = Ui_OrbitLauncher()
    ui.setupUi(OrbitLauncher)
    OrbitLauncher.show()
    sys.exit(app.exec_())
