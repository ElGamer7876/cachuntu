#!/usr/bin/env python3
"""Check Return activation for both live welcome actions with real Qt events."""
import runpy
import sys
from types import SimpleNamespace
from unittest.mock import patch
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QPushButton

with patch.object(QApplication, 'exec', return_value=0), patch('sys.exit'), patch('subprocess.run', return_value=SimpleNamespace(returncode=1)) as launch:
    namespace = runpy.run_path(sys.argv[1])
    app = QApplication.instance()
    window = namespace['window']
    install = window.findChild(QPushButton, 'install')
    install.setFocus()
    app.processEvents()
    QTest.keyClick(install, Qt.Key.Key_Return)
    app.processEvents()
    assert launch.call_count == 1, 'Return did not activate Install'
    trial = window.findChild(QPushButton, 'try')
    trial.setFocus()
    app.processEvents()
    QTest.keyClick(trial, Qt.Key.Key_Return)
    app.processEvents()
    assert not window.isVisible(), 'Return did not activate Try'
print('Welcome keyboard activation: OK')
