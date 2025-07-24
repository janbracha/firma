#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFileDialog, QMessageBox, QListWidget,
                            QListWidgetItem, QTextEdit, QLineEdit, QFormLayout,
                            QWidget, QSplitter, QGroupBox, QScrollArea)
from PyQt6.QtCore import Qt, QMimeData, QUrl, pyqtSignal
from PyQt6.QtGui import QPixmap, QPalette, QDragEnterEvent, QDropEvent, QImage
from database import connect

# Import pro náhled PDF a dokumentů
try:
    import fitz  # PyMuPDF
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from docx import Document
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

class DocumentManager:
    """Správa dokumentů"""
    
    # Povolené typy souborů
    ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.txt', '.doc', '.docx'}
    MIME_TYPES = {
        '.pdf': 'application/pdf',
        '.png': 'image/png', 
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.txt': 'text/plain',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }
    
    # Maximální velikost souboru (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @staticmethod
    def get_documents_folder():
        """Vrátí cestu ke složce s dokumenty"""
        app_folder = os.path.dirname(os.path.abspath(__file__))
        documents_folder = os.path.join(app_folder, 'documents')
        os.makedirs(documents_folder, exist_ok=True)
        return documents_folder
    
    @staticmethod
    def validate_file(file_path):
        """Validuje soubor před nahráním"""
        if not os.path.exists(file_path):
            return False, "Soubor neexistuje"
        
        # Kontrola přípony
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in DocumentManager.ALLOWED_EXTENSIONS:
            return False, f"Nepodporovaný typ souboru. Povolené: {', '.join(DocumentManager.ALLOWED_EXTENSIONS)}"
        
        # Kontrola velikosti
        file_size = os.path.getsize(file_path)
        if file_size > DocumentManager.MAX_FILE_SIZE:
            return False, f"Soubor je příliš velký. Maximální velikost: {DocumentManager.MAX_FILE_SIZE // (1024*1024)}MB"
        
        return True, ""
    
    @staticmethod
    def upload_document(file_path, related_table=None, related_id=None, description="", uploaded_by=1, target_directory=None):
        """Nahraje dokument do systému"""
        
        # Validace souboru
        is_valid, error_msg = DocumentManager.validate_file(file_path)
        if not is_valid:
            return False, error_msg
        
        try:
            # Generování unikátního názvu souboru
            original_filename = os.path.basename(file_path)
            file_ext = Path(file_path).suffix.lower()
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            
            # Cílová cesta - pokud není zadán target_directory, použije se výchozí
            if target_directory and os.path.exists(target_directory):
                documents_folder = target_directory
            else:
                documents_folder = DocumentManager.get_documents_folder()
                
            target_path = os.path.join(documents_folder, unique_filename)
            
            # Kopírování souboru
            shutil.copy2(file_path, target_path)
            
            # Uložení metadat do databáze
            conn = connect()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO documents 
                (filename, original_filename, file_path, file_size, file_type, mime_type,
                 related_table, related_id, description, uploaded_by, upload_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                unique_filename,
                original_filename,
                target_path,
                os.path.getsize(target_path),
                file_ext.lstrip('.'),
                DocumentManager.MIME_TYPES.get(file_ext, 'application/octet-stream'),
                related_table,
                related_id,
                description,
                uploaded_by,
                datetime.now().isoformat()
            ))
            
            document_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, f"Dokument úspěšně nahrán (ID: {document_id})"
            
        except Exception as e:
            return False, f"Chyba při nahrávání: {str(e)}"
    
    @staticmethod
    def get_documents(related_table=None, related_id=None):
        """Načte dokumenty pro konkrétní záznam nebo všechny"""
        conn = connect()
        cursor = conn.cursor()
        
        if related_table and related_id:
            cursor.execute("""
                SELECT d.*, u.username 
                FROM documents d
                LEFT JOIN users u ON d.uploaded_by = u.id
                WHERE d.related_table = ? AND d.related_id = ?
                ORDER BY d.upload_date DESC
            """, (related_table, related_id))
        else:
            cursor.execute("""
                SELECT d.*, u.username 
                FROM documents d
                LEFT JOIN users u ON d.uploaded_by = u.id
                ORDER BY d.upload_date DESC
            """)
        
        documents = cursor.fetchall()
        conn.close()
        return documents
    
    @staticmethod
    def delete_document(document_id):
        """Smaže dokument"""
        try:
            conn = connect()
            cursor = conn.cursor()
            
            # Načtení cesty k souboru
            cursor.execute("SELECT file_path FROM documents WHERE id = ?", (document_id,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, "Dokument nenalezen"
            
            file_path = result[0]
            
            # Smazání záznamu z databáze
            cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
            conn.commit()
            conn.close()
            
            # Smazání fyzického souboru
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return True, "Dokument byl smazán"
            
        except Exception as e:
            return False, f"Chyba při mazání: {str(e)}"
    
    @staticmethod
    def get_document_path(document_id):
        """Vrátí cestu k dokumentu"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT file_path FROM documents WHERE id = ?", (document_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result and os.path.exists(result[0]):
            return result[0]
        return None


class DocumentViewer(QWidget):
    """Widget pro prohlížení dokumentů"""
    
    def __init__(self):
        super().__init__()
        self.current_document = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.content_label = QLabel("Vyberte dokument pro zobrazení")
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_label.setStyleSheet("""
            QLabel {
                padding: 20px; 
                border: 2px solid #0078d4; 
                background: white;
                color: #000000;
                font-size: 14px;
                font-family: 'Consolas', 'Courier New', monospace;
                border-radius: 5px;
            }
        """)
        self.content_label.setWordWrap(True)  # Povolit zalamování textu
        self.content_label.setMinimumHeight(200)  # Minimální výška
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  # Zarovnání nahoru a doleva pro text
        
        # Zajistíme, že žádný obrázek není nastaven
        self.content_label.setPixmap(QPixmap())
        
        # Přidám label přímo do layoutu místo do scroll area
        layout.addWidget(self.content_label)
        
        self.setLayout(layout)
    
    def display_document(self, document_path, file_type):
        """Zobrazí dokument"""
        self.current_document = document_path
        
        try:
            # Kontrola existence souboru
            if not os.path.exists(document_path):
                self.content_label.setPixmap(QPixmap())
                self.content_label.setText(f"❌ Soubor nenalezen:\n{document_path}")
                return
            
            if file_type in ['png', 'jpg', 'jpeg']:
                self.display_image(document_path)
            elif file_type == 'pdf':
                self.display_pdf_preview(document_path)
            elif file_type in ['txt']:
                self.display_text_preview(document_path)
            elif file_type in ['doc', 'docx']:
                self.display_word_preview(document_path, file_type)
            else:
                self.display_unknown_file(document_path, file_type)
                
        except Exception as e:
            self.content_label.setPixmap(QPixmap())
            self.content_label.setText(f"❌ Chyba při zobrazení:\n{str(e)}")
    
    def scale_pixmap(self, pixmap, max_width=800, max_height=600):
        """Škáluje pixmap na rozumnou velikost"""
        if pixmap.width() > max_width or pixmap.height() > max_height:
            return pixmap.scaled(max_width, max_height, 
                               Qt.AspectRatioMode.KeepAspectRatio, 
                               Qt.TransformationMode.SmoothTransformation)
        return pixmap
    
    def display_image(self, image_path):
        """Zobrazí obrázek"""
        try:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Škálování na rozumnou velikost
                scaled_pixmap = self.scale_pixmap(pixmap)
                
                # Nejprve vymažeme text, pak nastavíme obrázek
                self.content_label.setText("")
                self.content_label.setPixmap(scaled_pixmap)
                self.content_label.update()
                self.content_label.repaint()
            else:
                # Pro chybový stav vymažeme obrázek a nastavíme text
                self.content_label.setPixmap(QPixmap())
                self.content_label.setText("❌ Nelze načíst obrázek")
                self.content_label.update()
                self.content_label.repaint()
        except Exception as e:
            # Pro výjimku vymažeme obrázek a nastavíme text
            self.content_label.setPixmap(QPixmap())
            self.content_label.setText(f"❌ Chyba při načítání obrázku:\n{str(e)}")
            self.content_label.update()
            self.content_label.repaint()
    
    def display_pdf_preview(self, pdf_path):
        """Zobrazí náhled PDF - první stránku jako obrázek"""
        if not PDF_SUPPORT:
            self.display_pdf_info_fallback(pdf_path)
            return
            
        try:
            # Otevření PDF dokumentu
            doc = fitz.open(pdf_path)
            
            if len(doc) == 0:
                self.content_label.setPixmap(QPixmap())
                self.content_label.setText("❌ PDF dokument je prázdný")
                doc.close()
                return
            
            # Načtení první stránky
            page = doc[0]
            
            # Konverze na obrázek (matrix pro zvětšení kvality)
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom pro lepší kvalitu
            pix = page.get_pixmap(matrix=mat)
            
            # Konverze na QImage
            img_data = pix.tobytes("ppm")
            qimg = QImage.fromData(img_data)
            
            if not qimg.isNull():
                # Konverze na QPixmap a škálování
                pixmap = QPixmap.fromImage(qimg)
                scaled_pixmap = self.scale_pixmap(pixmap)
                
                # Zobrazení náhledu
                self.content_label.setText("")
                self.content_label.setPixmap(scaled_pixmap)
                self.content_label.update()
                self.content_label.repaint()
            else:
                self.display_pdf_info_fallback(pdf_path)
            
            doc.close()
            
        except Exception as e:
            self.display_pdf_info_fallback(pdf_path)
    
    def display_pdf_info_fallback(self, pdf_path):
        """Zobrazí informace o PDF (fallback když náhled nejde)"""
        file_size = os.path.getsize(pdf_path) / 1024  # KB
        
        text = (
            f"📄 PDF Dokument\n\n"
            f"📁 {os.path.basename(pdf_path)}\n"
            f"📊 Velikost: {file_size:.1f} KB\n\n"
            f"Dvojklik pro otevření v externím programu"
        )
        
        self.content_label.setPixmap(QPixmap())
        self.content_label.setText(text)
        self.content_label.adjustSize()
        self.content_label.update()
        self.content_label.repaint()
    
    def display_text_preview(self, text_path):
        """Zobrazí náhled textového souboru"""
        try:
            # Načtení prvních řádků souboru
            with open(text_path, 'r', encoding='utf-8') as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= 15:  # Prvních 15 řádků
                        break
                    lines.append(line.rstrip())
                
                content = '\n'.join(lines)
                if len(lines) == 15:
                    content += '\n\n... (dvojklik pro celý soubor)'
            
            file_size = os.path.getsize(text_path) / 1024  # KB
            
            preview_text = (
                f"📝 Textový soubor\n"
                f"📁 {os.path.basename(text_path)} ({file_size:.1f} KB)\n"
                f"{'='*50}\n"
                f"{content}"
            )
            
            self.content_label.setPixmap(QPixmap())
            self.content_label.setText(preview_text)
            self.content_label.update()
            self.content_label.repaint()
            
        except UnicodeDecodeError:
            # Zkusíme jiné kódování
            try:
                with open(text_path, 'r', encoding='cp1250') as f:
                    content = f.read(500)  # Prvních 500 znaků
                    if len(content) == 500:
                        content += '\n\n... (dvojklik pro celý soubor)'
                
                preview_text = (
                    f"📝 Textový soubor\n"
                    f"📁 {os.path.basename(text_path)}\n"
                    f"{'='*50}\n"
                    f"{content}"
                )
                
                self.content_label.setPixmap(QPixmap())
                self.content_label.setText(preview_text)
                self.content_label.update()
                self.content_label.repaint()
                
            except Exception as e:
                self.display_text_info_fallback(text_path, 'txt')
        except Exception as e:
            self.display_text_info_fallback(text_path, 'txt')
    
    def display_word_preview(self, doc_path, file_type):
        """Zobrazí náhled Word dokumentu"""
        if file_type == 'docx' and DOCX_SUPPORT:
            try:
                doc = Document(doc_path)
                
                # Načtení prvních odstavců
                paragraphs = []
                char_count = 0
                max_chars = 500
                
                for para in doc.paragraphs:
                    if char_count >= max_chars:
                        break
                    text = para.text.strip()
                    if text:
                        paragraphs.append(text)
                        char_count += len(text)
                
                content = '\n\n'.join(paragraphs)
                if char_count >= max_chars:
                    content += '\n\n... (dvojklik pro celý dokument)'
                
                file_size = os.path.getsize(doc_path) / 1024  # KB
                
                preview_text = (
                    f"📄 Word dokument\n"
                    f"📁 {os.path.basename(doc_path)} ({file_size:.1f} KB)\n"
                    f"{'='*50}\n"
                    f"{content}"
                )
                
                self.content_label.setPixmap(QPixmap())
                self.content_label.setText(preview_text)
                self.content_label.update()
                self.content_label.repaint()
                
            except Exception as e:
                self.display_text_info_fallback(doc_path, file_type)
        else:
            self.display_text_info_fallback(doc_path, file_type)
    
    def display_text_info_fallback(self, text_path, file_type):
        """Zobrazí informace o textovém dokumentu (fallback)"""
        file_size = os.path.getsize(text_path) / 1024  # KB
        
        icon = "📝" if file_type == 'txt' else "📄"
        type_name = {
            'txt': 'Textový soubor',
            'doc': 'Word dokument', 
            'docx': 'Word dokument'
        }.get(file_type, 'Dokument')
        
        text = (
            f"{icon} {type_name}\n\n"
            f"📁 {os.path.basename(text_path)}\n"
            f"📊 Velikost: {file_size:.1f} KB\n\n"
            f"Dvojklik pro otevření v externím programu"
        )
        
        self.content_label.setPixmap(QPixmap())
        self.content_label.setText(text)
        self.content_label.adjustSize()
        self.content_label.update()
        self.content_label.repaint()
    
    def display_unknown_file(self, file_path, file_type):
        """Zobrazí informace o neznámém typu souboru"""
        file_size = os.path.getsize(file_path) / 1024  # KB
        
        text = (
            f"📎 Neznámý typ souboru\n\n"
            f"📁 {os.path.basename(file_path)}\n"
            f"🏷 Typ: {file_type.upper()}\n"
            f"📊 Velikost: {file_size:.1f} KB\n\n"
            f"Dvojklik pro otevření v externím programu"
        )
        
        # Nejprve vymažeme obrázek, pak nastavíme text
        self.content_label.setPixmap(QPixmap())
        self.content_label.setText(text)
        self.content_label.update()
        self.content_label.repaint()


class DocumentUploadDialog(QDialog):
    """Dialog pro nahrávání dokumentů"""
    
    def __init__(self, related_table=None, related_id=None):
        super().__init__()
        self.related_table = related_table
        self.related_id = related_id
        self.selected_files = []
        self.target_directory = None  # Nová vlastnost pro cílový adresář
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Nahrát dokumenty")
        self.setGeometry(200, 200, 500, 500)
        
        layout = QVBoxLayout()
        
        # Informace
        info_label = QLabel("Přetáhněte soubory nebo použijte tlačítko pro výběr")
        info_label.setStyleSheet("padding: 10px; background: #f0f0f0; border-radius: 5px;")
        layout.addWidget(info_label)
        
        # Výběr cílového adresáře
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Cílový adresář:")
        self.folder_edit = QLineEdit()
        self.folder_edit.setText(DocumentManager.get_documents_folder())  # Výchozí
        self.folder_edit.setReadOnly(True)
        folder_browse_btn = QPushButton("Procházet...")
        folder_browse_btn.clicked.connect(self.select_target_directory)
        
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(folder_browse_btn)
        layout.addLayout(folder_layout)
        
        # Drag & Drop area
        self.drop_area = DropArea()
        self.drop_area.files_dropped.connect(self.files_selected)
        layout.addWidget(self.drop_area)
        
        # Tlačítko pro výběr souborů
        select_btn = QPushButton("Vybrat soubory")
        select_btn.clicked.connect(self.select_files)
        layout.addWidget(select_btn)
        
        # Seznam vybraných souborů
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)
        
        # Popis
        form_layout = QFormLayout()
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        form_layout.addRow("Popis:", self.description_edit)
        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        upload_btn = QPushButton("Nahrát")
        upload_btn.clicked.connect(self.upload_files)
        
        cancel_btn = QPushButton("Zrušit")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(upload_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def select_files(self):
        """Otevře dialog pro výběr souborů"""
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            "Vyberte dokumenty",
            "",
            "Dokumenty (*.pdf *.png *.jpg *.jpeg *.txt *.doc *.docx);;Všechny soubory (*)"
        )
        
        if files:
            self.files_selected(files)
    
    def select_target_directory(self):
        """Otevře dialog pro výběr cílového adresáře"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Vyberte cílový adresář",
            self.folder_edit.text()
        )
        
        if directory:
            self.folder_edit.setText(directory)
            self.target_directory = directory
    
    def files_selected(self, files):
        """Zpracuje vybrané soubory"""
        self.selected_files.extend(files)
        
        # Aktualizace seznamu
        self.file_list.clear()
        for file_path in self.selected_files:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            self.file_list.addItem(item)
    
    def upload_files(self):
        """Nahraje vybrané soubory"""
        if not self.selected_files:
            QMessageBox.warning(self, "Upozornění", "Nebyl vybrán žádný soubor")
            return
        
        description = self.description_edit.toPlainText()
        success_count = 0
        errors = []
        
        # Použije vybraný cílový adresář nebo None pro výchozí
        target_dir = self.target_directory if self.target_directory != DocumentManager.get_documents_folder() else None
        
        for file_path in self.selected_files:
            success, message = DocumentManager.upload_document(
                file_path, 
                self.related_table, 
                self.related_id, 
                description,
                1,  # uploaded_by
                target_dir
            )
            
            if success:
                success_count += 1
            else:
                errors.append(f"{os.path.basename(file_path)}: {message}")
        
        # Výsledek
        if success_count > 0:
            QMessageBox.information(
                self, 
                "Úspěch", 
                f"Úspěšně nahráno {success_count} dokumentů"
            )
        
        if errors:
            QMessageBox.warning(
                self, 
                "Chyby", 
                f"Chyby při nahrávání:\n" + "\n".join(errors)
            )
        
        if success_count > 0:
            self.accept()


class DropArea(QLabel):
    """Oblast pro drag & drop souborů"""
    
    # Definování signálu
    files_dropped = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setText("📎 Přetáhněte soubory sem\n(PDF, PNG, JPG, TXT, DOC, DOCX)")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                padding: 40px;
                background: #fafafa;
                color: #666;
                font-size: 14px;
            }
            QLabel:hover {
                border-color: #0078d4;
                background: #f0f8ff;
            }
        """)
        self.setMinimumHeight(120)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                files.append(file_path)
        
        if files:
            self.files_dropped.emit(files)
