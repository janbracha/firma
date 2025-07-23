#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QMessageBox, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from user_management import UserManager

class SimpleLoginDialog(QDialog):
    """Jednoduchý přihlašovací dialog"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializuje uživatelské rozhraní"""
        self.setWindowTitle("Přihlášení - Správa firmy")
        self.setGeometry(400, 300, 350, 200)
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Hlavička
        header_label = QLabel("Správa firmy")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        subtitle_label = QLabel("Projekt & Develop s.r.o.")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(20)
        
        # Formulář
        form_layout = QFormLayout()
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Uživatelské jméno")
        form_layout.addRow("Uživatel:", self.username_edit)
        
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Heslo")
        form_layout.addRow("Heslo:", self.password_edit)
        
        layout.addLayout(form_layout)
        
        layout.addSpacing(20)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Přihlásit")
        self.login_button.clicked.connect(self.login)
        self.login_button.setDefault(True)
        button_layout.addWidget(self.login_button)
        
        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Styl
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #2c3e50;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        
        # Focus na username
        self.username_edit.setFocus()
        
        # Enter key handling
        self.username_edit.returnPressed.connect(self.password_edit.setFocus)
        self.password_edit.returnPressed.connect(self.login)
    
    def login(self):
        """Zpracuje přihlášení"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Chyba", "Vyplňte prosím všechna pole")
            return
        
        # Ověření přihlašovacích údajů
        user = UserManager.authenticate_user(username, password)
        
        if user:
            self.current_user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Chyba přihlášení", 
                              "Nesprávné uživatelské jméno nebo heslo")
            self.password_edit.clear()
            self.username_edit.setFocus()
    
    def get_current_user(self):
        """Vrátí aktuálně přihlášeného uživatele"""
        return self.current_user
