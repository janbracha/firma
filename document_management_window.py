#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import platform
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QMessageBox, QGroupBox, QSplitter, QHeaderView,
                            QAbstractItemView, QMenu, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction, QPixmap
from document_management import DocumentManager, DocumentViewer, DocumentUploadDialog

class DocumentManagementWindow(QMainWindow):
    """Okno pro správu dokumentů"""
    
    def __init__(self, related_table=None, related_id=None, title_suffix=""):
        super().__init__()
        self.related_table = related_table
        self.related_id = related_id
        self.title_suffix = title_suffix
        self.init_ui()
        self.load_documents()
    
    def init_ui(self):
        title = "Správa dokumentů"
        if self.title_suffix:
            title += f" - {self.title_suffix}"
        
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 1200, 800)
        
        # Stylování
        self.setStyleSheet("""
            QMainWindow {
                background: #F2F2F2;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            
            QLabel {
                color: #2B2B2B;
                font-weight: 500;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                background: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            QPushButton {
                background: #0078D4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background: #106EBE;
            }
            
            QPushButton:pressed {
                background: #005A9E;
            }
            
            QPushButton:disabled {
                background: #C8C8C8;
                color: #666666;
            }
            
            QTableWidget {
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                background: white;
                gridline-color: #F0F0F0;
                selection-background-color: #E3F2FD;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
            }
            
            QHeaderView::section {
                background: #F8F9FA;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                padding: 10px;
                font-weight: bold;
                color: #2B2B2B;
            }
        """)
        
        # Hlavní widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter pro rozdělení na seznam a náhled
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Levá strana - seznam dokumentů
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Header s tlačítky
        header_layout = QHBoxLayout()
        
        title_label = QLabel("📄 Dokumenty")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Tlačítka
        self.upload_btn = QPushButton("➕ Nahrát")
        self.upload_btn.clicked.connect(self.upload_document)
        header_layout.addWidget(self.upload_btn)
        
        self.refresh_btn = QPushButton("🔄 Obnovit")
        self.refresh_btn.clicked.connect(self.load_documents)
        header_layout.addWidget(self.refresh_btn)
        
        left_layout.addLayout(header_layout)
        
        # Tabulka dokumentů
        self.documents_table = QTableWidget()
        self.documents_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.documents_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.documents_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.documents_table.customContextMenuRequested.connect(self.show_context_menu)
        self.documents_table.itemSelectionChanged.connect(self.on_document_selected)
        self.documents_table.itemDoubleClicked.connect(self.open_document)
        
        # Nastavení sloupců
        columns = ["Název", "Typ", "Velikost", "Nahráno", "Uživatel"]
        self.documents_table.setColumnCount(len(columns))
        self.documents_table.setHorizontalHeaderLabels(columns)
        
        # Nastavení šířky sloupců
        header = self.documents_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Název
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Typ
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Velikost
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Nahráno
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Uživatel
        
        left_layout.addWidget(self.documents_table)
        
        # Pravá strana - náhled dokumentu
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        preview_label = QLabel("👁 Náhled dokumentu")
        preview_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        right_layout.addWidget(preview_label)
        
        # Viewer
        self.document_viewer = DocumentViewer()
        right_layout.addWidget(self.document_viewer)
        
        # Tlačítka pro práci s dokumentem
        preview_buttons = QHBoxLayout()
        
        self.open_btn = QPushButton("🔍 Otevřít")
        self.open_btn.clicked.connect(self.open_document)
        self.open_btn.setEnabled(False)
        
        self.delete_btn = QPushButton("🗑 Smazat")
        self.delete_btn.clicked.connect(self.delete_document)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet("QPushButton { background: #D83B01; } QPushButton:hover { background: #A4262C; }")
        
        preview_buttons.addWidget(self.open_btn)
        preview_buttons.addWidget(self.delete_btn)
        preview_buttons.addStretch()
        
        right_layout.addLayout(preview_buttons)
        
        # Přidání do splitteru
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 600])  # Poměr 1:1
    
    def load_documents(self):
        """Načte dokumenty do tabulky"""
        documents = DocumentManager.get_documents(self.related_table, self.related_id)
        
        self.documents_table.setRowCount(len(documents))
        
        for row, doc in enumerate(documents):
            # Název souboru
            name_item = QTableWidgetItem(doc[2])  # original_filename
            name_item.setData(Qt.ItemDataRole.UserRole, doc)  # Uložení celého záznamu
            self.documents_table.setItem(row, 0, name_item)
            
            # Typ souboru
            type_item = QTableWidgetItem(doc[5].upper())  # file_type
            self.documents_table.setItem(row, 1, type_item)
            
            # Velikost
            size_kb = doc[4] / 1024  # file_size v KB
            if size_kb > 1024:
                size_text = f"{size_kb/1024:.1f} MB"
            else:
                size_text = f"{size_kb:.0f} KB"
            size_item = QTableWidgetItem(size_text)
            self.documents_table.setItem(row, 2, size_item)
            
            # Datum nahrání
            upload_date = doc[11][:10] if doc[11] else ""  # upload_date (jen datum)
            date_item = QTableWidgetItem(upload_date)
            self.documents_table.setItem(row, 3, date_item)
            
            # Uživatel
            username = doc[12] if doc[12] else "Neznámý"  # username
            user_item = QTableWidgetItem(username)
            self.documents_table.setItem(row, 4, user_item)
    
    def on_document_selected(self):
        """Při výběru dokumentu v tabulce"""
        current_row = self.documents_table.currentRow()
        
        if current_row >= 0:
            # Aktivace tlačítek
            self.open_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            
            # Načtení dokumentu pro náhled
            item = self.documents_table.item(current_row, 0)
            
            if item:
                doc = item.data(Qt.ItemDataRole.UserRole)
                
                if doc:
                    file_path = doc[3]  # file_path
                    file_type = doc[5]  # file_type
                    
                    if os.path.exists(file_path):
                        self.document_viewer.display_document(file_path, file_type)
                        
                        # FORCE REFRESH celého window
                        self.document_viewer.update()
                        self.document_viewer.repaint()
                        self.update()
                        self.repaint()
                        
                    else:
                        self.document_viewer.content_label.setText("❌ Soubor nenalezen")
                        # Odstraněno problematické setPixmap
                        self.document_viewer.content_label.update()
        else:
            # Deaktivace tlačítek
            self.open_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
    
    def upload_document(self):
        """Otevře dialog pro nahrání dokumentu"""
        dialog = DocumentUploadDialog(self.related_table, self.related_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_documents()
    
    def open_document(self):
        """Otevře vybraný dokument v externím programu"""
        current_row = self.documents_table.currentRow()
        if current_row >= 0:
            item = self.documents_table.item(current_row, 0)
            if item:
                doc = item.data(Qt.ItemDataRole.UserRole)
                if doc:
                    file_path = doc[3]  # file_path
                    
                    if os.path.exists(file_path):
                        try:
                            if platform.system() == 'Windows':
                                os.startfile(file_path)
                            elif platform.system() == 'Darwin':  # macOS
                                subprocess.call(['open', file_path])
                            else:  # Linux
                                subprocess.call(['xdg-open', file_path])
                        except Exception as e:
                            QMessageBox.warning(self, "Chyba", f"Nelze otevřít soubor: {str(e)}")
                    else:
                        QMessageBox.warning(self, "Chyba", "Soubor nenalezen")
    
    def delete_document(self):
        """Smaže vybraný dokument"""
        current_row = self.documents_table.currentRow()
        if current_row >= 0:
            item = self.documents_table.item(current_row, 0)
            if item:
                doc = item.data(Qt.ItemDataRole.UserRole)
                if doc:
                    filename = doc[2]  # original_filename
                    
                    reply = QMessageBox.question(
                        self, 
                        "Potvrzení smazání",
                        f"Opravdu chcete smazat dokument '{filename}'?\n\nTato akce je nevratná.",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        success, message = DocumentManager.delete_document(doc[0])  # id
                        
                        if success:
                            QMessageBox.information(self, "Úspěch", message)
                            self.load_documents()
                            # Vymazání náhledu
                            self.document_viewer.content_label.setText("Vyberte dokument pro zobrazení")
                            # Odstraněno problematické setPixmap
                        else:
                            QMessageBox.warning(self, "Chyba", message)
    
    def show_context_menu(self, position):
        """Zobrazí kontextové menu"""
        item = self.documents_table.itemAt(position)
        if item:
            menu = QMenu(self)
            
            open_action = QAction("🔍 Otevřít", self)
            open_action.triggered.connect(self.open_document)
            menu.addAction(open_action)
            
            menu.addSeparator()
            
            delete_action = QAction("🗑 Smazat", self)
            delete_action.triggered.connect(self.delete_document)
            menu.addAction(delete_action)
            
            menu.exec(self.documents_table.mapToGlobal(position))
