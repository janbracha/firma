#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
from user_management import UserManager

class ChangePasswordDialog(QDialog):
    """Dialog pro změnu hesla uživatele"""
    
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"Změna hesla - {self.username}")
        self.setFixedSize(400, 200)
        self.setModal(True)
        
        # Stylování
        self.setStyleSheet("""
            QDialog {
                background: #F2F2F2;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            
            QLabel {
                color: #2C3E50;
                font-size: 14px;
                font-weight: bold;
            }
            
            QLineEdit {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px;
                color: #2C3E50;
                font-size: 14px;
            }
            
            QLineEdit:focus {
                border-color: #6C85A3;
            }
            
            QPushButton {
                background-color: #6C85A3;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 18px;
                border: none;
            }
            
            QPushButton:hover {
                background-color: #5A7393;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Nadpis
        title = QLabel(f"Změna hesla pro uživatele: {self.username}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; margin: 15px;")
        layout.addWidget(title)
        
        # Formulář
        form_layout = QFormLayout()
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setPlaceholderText("Zadejte nové heslo")
        form_layout.addRow(QLabel("Nové heslo:"), self.new_password_input)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Potvrďte nové heslo")
        form_layout.addRow(QLabel("Potvrzení hesla:"), self.confirm_password_input)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Změnit heslo")
        self.save_button.clicked.connect(self.change_password)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #95A5A6;
                color: white;
            }
            QPushButton:hover {
                background-color: #7F8C8D;
            }
        """)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Nastavení fokusu
        self.new_password_input.setFocus()
        
        # Enter pro potvrzení
        self.new_password_input.returnPressed.connect(self.change_password)
        self.confirm_password_input.returnPressed.connect(self.change_password)
    
    def change_password(self):
        """Změní heslo uživatele"""
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        if not new_password:
            QMessageBox.warning(self, "Chyba", "Zadejte nové heslo!")
            return
        
        if len(new_password) < 4:
            QMessageBox.warning(self, "Chyba", "Heslo musí mít alespoň 4 znaky!")
            return
        
        if new_password != confirm_password:
            QMessageBox.warning(self, "Chyba", "Hesla se neshodují!")
            return
        
        # Změna hesla v databázi
        if UserManager.change_password(self.user_id, new_password):
            QMessageBox.information(self, "Úspěch", "Heslo bylo úspěšně změněno!")
            self.accept()
        else:
            QMessageBox.critical(self, "Chyba", "Nepodařilo se změnit heslo!")
