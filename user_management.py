#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox, QFormLayout)
from PyQt6.QtCore import Qt
from database import connect

class UserManager:
    """Správa uživatelů a rolí"""
    
    @staticmethod
    def hash_password(password):
        """Zahashuje heslo"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hash_password):
        """Ověří heslo"""
        return UserManager.hash_password(password) == hash_password
    
    @staticmethod
    def authenticate_user(username, password):
        """Ověří přihlašovací údaje"""
        conn = connect()
        cursor = conn.cursor()
        
        # Pro účely ukázky používáme jednoduché heslo - v produkci by bylo hashované
        cursor.execute("""
            SELECT id, username, full_name, role, active 
            FROM users 
            WHERE username = ? AND password_hash = ? AND active = 1
        """, (username, password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Aktualizace posledního přihlášení
            UserManager.update_last_login(user[0])
            return {
                'id': user[0],
                'username': user[1], 
                'full_name': user[2],
                'role': user[3],
                'active': user[4]
            }
        return None
    
    @staticmethod
    def update_last_login(user_id):
        """Aktualizuje čas posledního přihlášení"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET last_login = datetime('now') WHERE id = ?
        """, (user_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all_users():
        """Načte všechny uživatele"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, full_name, email, role, active, created_date, last_login
            FROM users ORDER BY username
        """)
        users = cursor.fetchall()
        conn.close()
        return users
    
    @staticmethod
    def add_user(username, password, full_name, email, role):
        """Přidá nového uživatele"""
        conn = connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, email, role, created_date)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """, (username, password, full_name, email, role))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    @staticmethod
    def update_user(user_id, username, full_name, email, role):
        """Aktualizuje údaje uživatele"""
        conn = connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users SET username = ?, full_name = ?, email = ?, role = ?
                WHERE id = ?
            """, (username, full_name, email, role, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    @staticmethod
    def change_password(user_id, new_password):
        """Změní heslo uživatele"""
        conn = connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users SET password_hash = ? WHERE id = ?
            """, (new_password, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    @staticmethod
    def delete_user(user_id):
        """Smaže uživatele (pouze neaktivní účty nebo deaktivuje)"""
        conn = connect()
        cursor = conn.cursor()
        
        try:
            # Nejprve zkontrolujeme, jestli to není admin
            cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            
            if result and result[0] == 'admin':
                conn.close()
                return False  # Admin účet nelze smazat
            
            # Deaktivujeme uživatele místo smazání
            cursor.execute("""
                UPDATE users SET active = 0 WHERE id = ?
            """, (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    @staticmethod
    def activate_user(user_id):
        """Znovu aktivuje deaktivovaného uživatele"""
        conn = connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users SET active = 1 WHERE id = ?
            """, (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    @staticmethod
    def permanently_delete_user(user_id):
        """Trvale odstraní uživatele z databáze"""
        conn = connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                DELETE FROM users WHERE id = ?
            """, (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    @staticmethod
    def get_user_by_id(user_id):
        """Načte uživatele podle ID"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, full_name, email, role, active
            FROM users WHERE id = ?
        """, (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def has_permission(user_role, required_permission):
        """Kontrola oprávnění podle role"""
        permissions = {
            'admin': ['all'],  # Admin má přístup ke všemu
            'accountant': ['invoices', 'companies', 'cash_journal', 'reports'],  # Účetní
            'user': ['view_invoices', 'trip_book']  # Běžný uživatel
        }
        
        user_permissions = permissions.get(user_role, [])
        return 'all' in user_permissions or required_permission in user_permissions


class LoginDialog(QDialog):
    """Dialog pro přihlášení uživatele"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Přihlášení do systému")
        self.setFixedSize(500, 400)  # Zvětšené okno
        self.setModal(True)
        
        # Stylování dialogu s větším fontem
        self.setStyleSheet("""
            QDialog {
                background: #F2F2F2;
                font-family: 'Arial', 'Helvetica', sans-serif;
                color: #000000;
                font-size: 16px;
            }
            
            QLabel {
                color: #2C3E50;
                font-size: 16px;
                font-weight: bold;
            }
            
            QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px;
                color: #000000;
                font-size: 14px;
                font-family: 'Arial', sans-serif;
                selection-background-color: #6C85A3;
                selection-color: white;
            }
            
            QLineEdit:focus {
                border-color: #6C85A3;
                background-color: #FAFAFA;
            }
            
            QLineEdit::placeholder {
                color: #999999;
                font-style: italic;
            }
            
            QPushButton {
                background-color: #6C85A3;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 18px;
                border: none;
            }
            
            QPushButton:hover {
                background-color: #5A7393;
            }
            
            QPushButton:pressed {
                background-color: #4A6383;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Logo/Název aplikace
        title_label = QLabel("Správa firmy")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #6C85A3; margin: 20px;")
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Projekt & Develop s.r.o.")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 16px; color: #7F8C8D; margin-bottom: 30px;")
        layout.addWidget(subtitle_label)
        
        # Formulář přihlášení
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("admin")
        # Výrazně zlepšené styly pro lepší viditelnost
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF !important;
                color: #000000 !important;
                border: 3px solid #4A90E2;
                border-radius: 10px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Arial', 'Helvetica', sans-serif;
                min-height: 25px;
            }
            QLineEdit:focus {
                border-color: #FF6B35 !important;
                background-color: #F8F9FA !important;
                color: #000000 !important;
            }
            QLineEdit::placeholder {
                color: #666666 !important;
                font-style: normal;
                font-weight: normal;
            }
        """)
        form_layout.addRow(QLabel("Uživatelské jméno:"), self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("admin123")
        # Stejné výrazné styly pro heslo
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF !important;
                color: #000000 !important;
                border: 3px solid #4A90E2;
                border-radius: 10px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Arial', 'Helvetica', sans-serif;
                min-height: 25px;
            }
            QLineEdit:focus {
                border-color: #FF6B35 !important;
                background-color: #F8F9FA !important;
                color: #000000 !important;
            }
            QLineEdit::placeholder {
                color: #666666 !important;
                font-style: normal;
                font-weight: normal;
            }
        """)
        form_layout.addRow(QLabel("Heslo:"), self.password_input)
        
        layout.addLayout(form_layout)
        
        # PRO TESTOVÁNÍ - předvyplněné hodnoty pro kontrolu viditelnosti
        self.username_input.setText("admin")
        self.password_input.setText("admin123")
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Přihlásit se")
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)
        
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
        
        # Nápověda
        help_label = QLabel("Výchozí přístup: admin / admin123")
        help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_label.setStyleSheet("font-size: 12px; color: #7F8C8D; margin-top: 20px;")
        layout.addWidget(help_label)
        
        self.setLayout(layout)
        
        # Enter pro přihlášení
        self.username_input.returnPressed.connect(self.login)
        self.password_input.returnPressed.connect(self.login)
        
        # Nastavení fokusu
        self.username_input.setFocus()
    
    def login(self):
        """Zpracuje přihlášení"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Chyba", "Zadejte uživatelské jméno a heslo!")
            return
        
        # Ověření přihlašovacích údajů
        user = UserManager.authenticate_user(username, password)
        
        if user:
            self.current_user = user
            QMessageBox.information(self, "Úspěch", f"Vítejte, {user['full_name']}!")
            self.accept()
        else:
            QMessageBox.critical(self, "Chyba", "Nesprávné uživatelské jméno nebo heslo!")
            self.password_input.clear()
            self.password_input.setFocus()
    
    def get_current_user(self):
        """Vrátí aktuálně přihlášeného uživatele"""
        return self.current_user
