#!/usr/bin/python3
"""Cachuntu live welcome screen, based on the approved installer design."""

from pathlib import Path
import subprocess
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class Welcome(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Cachuntu")
        self.setMinimumSize(960, 570)
        self.setStyleSheet("""
            QWidget { background: #061326; color: #f0f7ff; font-family: Inter; }
            QLabel#heading { font-size: 40px; font-weight: 700; }
            QLabel#detail { font-size: 18px; color: #a9c2d9; }
            QPushButton { font-size: 20px; font-weight: 600; padding: 18px 28px;
                          border-radius: 8px; border: 2px solid #4de4d1; }
            QPushButton#install { background: #4de4d1; color: #061326; }
            QPushButton#try { background: #061326; color: #4de4d1; }
            QPushButton:focus { border-color: #ffffff; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(64, 28, 64, 48)
        layout.setSpacing(18)
        logo = QLabel()
        logo.setPixmap(QPixmap("/usr/share/pixmaps/cachuntu-logo.png").scaled(
            330, 290, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation))
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(logo)
        heading = QLabel("Welcome to Cachuntu")
        heading.setObjectName("heading")
        layout.addWidget(heading)
        detail = QLabel("Choose how to begin. You can select KDE Plasma or GNOME during installation.")
        detail.setObjectName("detail")
        detail.setWordWrap(True)
        layout.addWidget(detail)
        layout.addStretch()
        buttons = QHBoxLayout()
        install = QPushButton("Install Cachuntu")
        install.setObjectName("install")
        install.setAutoDefault(True)
        install.clicked.connect(self.install)
        trial = QPushButton("Try Cachuntu")
        trial.setObjectName("try")
        trial.setAutoDefault(True)
        trial.clicked.connect(self.close)
        buttons.addWidget(install)
        buttons.addWidget(trial)
        layout.addLayout(buttons)
        install.setFocus()

    def install(self):
        self.hide()
        with Path("/tmp/cachuntu-calamares-launch.log").open("a") as log:
            result = subprocess.run(["/usr/libexec/cachuntu-launch-installer"],
                                    stdout=log, stderr=subprocess.STDOUT, check=False)
        if result.returncode:
            self.show()
            self.setWindowTitle("Installer exited; see /tmp/cachuntu-calamares-launch.log")
        else:
            self.close()


app = QApplication(sys.argv)
window = Welcome()
window.show()
sys.exit(app.exec())
