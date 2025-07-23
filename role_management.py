#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox, QFormLayout, QTextEdit,
                            QListWidget, QListWidgetItem, QCheckBox, QGroupBox,
                            QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from database import connect

class RoleManager:
    """Správa rolí a oprávnění"""
    
    @staticmethod
    def get_all_roles():
        """Načte všechny role"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, display_name, description, is_system, created_date, modified_date
            FROM roles ORDER BY display_name
        """)
        roles = cursor.fetchall()
        conn.close()
        return roles
    
    @staticmethod
    def get_all_permissions():
        """Načte všechna oprávnění"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, display_name, description, module, created_date
            FROM permissions ORDER BY module, display_name
        """)
        permissions = cursor.fetchall()
        conn.close()
        return permissions
    
    @staticmethod
    def get_role_permissions(role_id):
        """Načte oprávnění pro konkrétní roli"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.name, p.display_name, p.description, p.module
            FROM permissions p
            INNER JOIN role_permissions rp ON p.id = rp.permission_id
            WHERE rp.role_id = ?
            ORDER BY p.module, p.display_name
        """, (role_id,))
        permissions = cursor.fetchall()
        conn.close()
        return permissions
    
    @staticmethod
    def get_permissions_by_module():
        """Načte oprávnění seskupená podle modulů"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT module, id, name, display_name, description
            FROM permissions 
            ORDER BY module, display_name
        """)
        permissions = cursor.fetchall()
        conn.close()
        
        # Seskupení podle modulů
        modules = {}
        for perm in permissions:
            module = perm[0]
            if module not in modules:
                modules[module] = []
            modules[module].append(perm[1:])  # bez názvu modulu
        
        return modules
    
    @staticmethod
    def create_role(name, display_name, description, permission_ids, created_by=None):
        """Vytvoří novou roli"""
        conn = connect()
        cursor = conn.cursor()
        
        try:
            # Vytvoření role
            cursor.execute("""
                INSERT INTO roles (name, display_name, description, is_system, created_date, modified_date)
                VALUES (?, ?, ?, 0, datetime('now'), datetime('now'))
            """, (name, display_name, description))
            
            role_id = cursor.lastrowid
            
            # Přiřazení oprávnění
            for perm_id in permission_ids:
                cursor.execute("""
                    INSERT INTO role_permissions (role_id, permission_id, granted_date, granted_by)
                    VALUES (?, ?, datetime('now'), ?)
                """, (role_id, perm_id, created_by))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            return False
    
    @staticmethod
    def update_role(role_id, display_name, description, permission_ids, updated_by=None):
        """Aktualizuje existující roli"""
        conn = connect()
        cursor = conn.cursor()
        
        try:
            # Aktualizace role
            cursor.execute("""
                UPDATE roles 
                SET display_name = ?, description = ?, modified_date = datetime('now')
                WHERE id = ?
            """, (display_name, description, role_id))
            
            # Smazání starých oprávnění
            cursor.execute("""
                DELETE FROM role_permissions WHERE role_id = ?
            """, (role_id,))
            
            # Přiřazení nových oprávnění
            for perm_id in permission_ids:
                cursor.execute("""
                    INSERT INTO role_permissions (role_id, permission_id, granted_date, granted_by)
                    VALUES (?, ?, datetime('now'), ?)
                """, (role_id, perm_id, updated_by))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            return False
    
    @staticmethod
    def delete_role(role_id):
        """Smaže roli (pouze uživatelské role)"""
        conn = connect()
        cursor = conn.cursor()
        
        try:
            # Kontrola, zda není systémová
            cursor.execute("SELECT is_system FROM roles WHERE id = ?", (role_id,))
            result = cursor.fetchone()
            
            if result and result[0] == 1:
                conn.close()
                return False  # Systémovou roli nelze smazat
            
            # Smazání oprávnění role
            cursor.execute("DELETE FROM role_permissions WHERE role_id = ?", (role_id,))
            
            # Smazání role
            cursor.execute("DELETE FROM roles WHERE id = ?", (role_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            return False
    
    @staticmethod
    def get_user_permissions(user_role):
        """Získá oprávnění uživatele podle jeho role"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name
            FROM permissions p
            INNER JOIN role_permissions rp ON p.id = rp.permission_id
            INNER JOIN roles r ON rp.role_id = r.id
            WHERE r.name = ?
        """, (user_role,))
        permissions = [row[0] for row in cursor.fetchall()]
        conn.close()
        return permissions


class RoleDialog(QDialog):
    """Dialog pro vytvoření/úpravu role"""
    
    def __init__(self, role_data=None):
        super().__init__()
        self.role_data = role_data
        self.permission_checkboxes = {}
        self.init_ui()
        
        if role_data:
            self.load_role_data()
    
    def init_ui(self):
        self.setWindowTitle("Nová role" if not self.role_data else "Upravit roli")
        self.setGeometry(200, 200, 600, 700)
        
        layout = QVBoxLayout()
        
        # Základní informace o roli
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.display_name_edit = QLineEdit()
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        
        if self.role_data:
            # Při úpravě nelze měnit systémový název
            self.name_edit.setEnabled(False)
        
        form_layout.addRow("Systémový název:", self.name_edit)
        form_layout.addRow("Zobrazovaný název:", self.display_name_edit)
        form_layout.addRow("Popis:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Oprávnění
        permissions_group = QGroupBox("Oprávnění")
        permissions_layout = QVBoxLayout()
        
        # Scroll area pro oprávnění
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Načtení oprávnění podle modulů
        modules = RoleManager.get_permissions_by_module()
        
        for module_name, permissions in modules.items():
            module_group = QGroupBox(self.get_module_display_name(module_name))
            module_layout = QVBoxLayout()
            
            for perm in permissions:
                perm_id, perm_name, perm_display_name, perm_description = perm
                
                checkbox = QCheckBox(f"{perm_display_name}")
                if perm_description:
                    checkbox.setToolTip(perm_description)
                
                self.permission_checkboxes[perm_id] = checkbox
                module_layout.addWidget(checkbox)
            
            module_group.setLayout(module_layout)
            scroll_layout.addWidget(module_group)
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        permissions_layout.addWidget(scroll_area)
        permissions_group.setLayout(permissions_layout)
        
        layout.addWidget(permissions_group)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Uložit")
        self.save_button.clicked.connect(self.save_role)
        
        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_module_display_name(self, module_name):
        """Převede systémový název modulu na zobrazovaný"""
        module_names = {
            'users': 'Správa uživatelů',
            'roles': 'Správa rolí',
            'invoices': 'Fakturace',
            'accounting': 'Účetnictví',
            'company': 'Nastavení firmy'
        }
        return module_names.get(module_name, module_name.capitalize())
    
    def load_role_data(self):
        """Načte data role pro úpravu"""
        role_id, name, display_name, description, is_system, created_date, modified_date = self.role_data
        
        self.name_edit.setText(name)
        self.display_name_edit.setText(display_name)
        self.description_edit.setText(description or "")
        
        # Načtení oprávnění role
        role_permissions = RoleManager.get_role_permissions(role_id)
        role_permission_ids = [perm[0] for perm in role_permissions]
        
        # Zaškrtnutí odpovídajících checkboxů
        for perm_id, checkbox in self.permission_checkboxes.items():
            if perm_id in role_permission_ids:
                checkbox.setChecked(True)
    
    def save_role(self):
        """Uloží roli"""
        name = self.name_edit.text().strip()
        display_name = self.display_name_edit.text().strip()
        description = self.description_edit.toPlainText().strip()
        
        if not name or not display_name:
            QMessageBox.warning(self, "Chyba", "Vyplňte název role!")
            return
        
        # Získání vybraných oprávnění
        selected_permissions = []
        for perm_id, checkbox in self.permission_checkboxes.items():
            if checkbox.isChecked():
                selected_permissions.append(perm_id)
        
        if not selected_permissions:
            QMessageBox.warning(self, "Chyba", "Vyberte alespoň jedno oprávnění!")
            return
        
        try:
            if self.role_data:
                # Úprava existující role
                role_id = self.role_data[0]
                success = RoleManager.update_role(role_id, display_name, description, selected_permissions)
            else:
                # Vytvoření nové role
                success = RoleManager.create_role(name, display_name, description, selected_permissions)
            
            if success:
                QMessageBox.information(self, "Úspěch", "Role byla úspěšně uložena!")
                self.accept()
            else:
                QMessageBox.critical(self, "Chyba", "Nepodařilo se uložit roli!")
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při ukládání role: {str(e)}")
