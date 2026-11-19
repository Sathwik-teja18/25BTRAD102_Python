"""
GENESIS Desktop UI
------------------
A separate PySide6 desktop interface for the existing GENESIS v4 kernel.

This module does not modify genesis.py, cortex.py, skills, or memory.
Run from the project directory:
    python genesis_ui.py

Install:
    python -m pip install PySide6
"""

from __future__ import annotations

import contextlib
import io
import sys
import threading
import traceback
from pathlib import Path

try:
    from PySide6.QtCore import QObject, QThread, Signal, Slot, Qt
    from PySide6.QtGui import QAction, QFont
    from PySide6.QtWidgets import (
        QApplication, QDialog, QFrame, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QMessageBox, QPushButton, QScrollArea, QSizePolicy,
        QStackedWidget, QTextBrowser, QTextEdit, QVBoxLayout, QWidget,
    )
except ImportError as exc:
    raise SystemExit(
        "GENESIS Desktop UI requires PySide6.\n"
        "Install it with: python -m pip install PySide6"
    ) from exc

import genesis


APP_STYLE = """
QMainWindow, QWidget#Root { background: #0b1020; color: #e5eaf5; }
QWidget { color: #e5eaf5; font-family: 'Segoe UI'; font-size: 10pt; }
QFrame#Sidebar { background: #10182a; border-right: 1px solid #26334b; }
QFrame#Topbar { background: #10182a; border-bottom: 1px solid #26334b; }
QFrame#Panel, QFrame#StatCard {
    background: #131e33; border: 1px solid #263653; border-radius: 12px;
}
QPushButton {
    background: #1a2942; color: #dce7f8; border: 1px solid #304563;
    border-radius: 8px; padding: 10px 13px; text-align: left;
}
QPushButton:hover { background: #243958; border-color: #5b8bc7; }
QPushButton:checked { background: #24466b; border-color: #75aef0; }
QPushButton#Primary {
    background: #3478c8; color: white; border: 0; font-weight: 600;
}
QPushButton#Primary:hover { background: #438bdc; }
QLineEdit, QTextEdit, QTextBrowser {
    background: #0e1728; color: #e5eaf5; border: 1px solid #30415e;
    border-radius: 9px; padding: 10px; selection-background-color: #3478c8;
}
QLabel#Muted { color: #91a3bf; }
QLabel#PageTitle { font-size: 20pt; font-weight: 700; }
QLabel#Brand { font-size: 17pt; font-weight: 800; letter-spacing: 1px; }
QScrollArea { border: 0; background: transparent; }
QTextBrowser { padding: 14px; }
"""

class PromptBroker(QObject):
    """Bridges kernel confirmation prompts to GUI dialogs."""
    prompt_requested = Signal(str)
    answered = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._event = threading.Event()
        self._answer = False
        self.prompt_requested.connect(self._show_prompt)

    def ask(self, prompt: str) -> bool:
        self._answer = False
        self._event.clear()
        self.prompt_requested.emit(prompt)
        self._event.wait()
        return self._answer

    @Slot(str)
    def _show_prompt(self, prompt: str):
        answer = QMessageBox.question(
            self.parent(),
            "GENESIS needs your approval",
            prompt,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        self._answer = answer == QMessageBox.Yes