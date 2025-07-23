from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QPushButton, QComboBox, QSpinBox, QTextEdit, QLineEdit
)
from PyQt6.QtCore import QDate

class InventoryDialog(QDialog):
    """Dialog pro inventuru"""
    
    def __init__(self, products, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inventura")
        self.setFixedSize(500, 450)
        self.products = products
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            QComboBox, QSpinBox, QTextEdit, QLineEdit {
                padding: 10px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 12px;
                background: white;
                margin-bottom: 10px;
            }
            QComboBox:focus, QSpinBox:focus, QTextEdit:focus, QLineEdit:focus {
                border-color: #1abc9c;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1abc9c, stop:1 #16a085);
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #48c9b0, stop:1 #1abc9c);
            }
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Formulář
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Výběr produktu
        product_label = QLabel("📦 Inventura produktu")
        product_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1abc9c; margin-top: 10px;")
        form_layout.addRow(product_label)
        
        self.product_combo = QComboBox()
        for product_id, product_name in self.products:
            self.product_combo.addItem(product_name, product_id)
        self.product_combo.currentTextChanged.connect(self.load_current_stock)
        form_layout.addRow("Produkt:", self.product_combo)
        
        # Aktuální stav
        self.current_stock_edit = QLineEdit()
        self.current_stock_edit.setReadOnly(True)
        self.current_stock_edit.setPlaceholderText("Načítá se...")
        form_layout.addRow("Aktuální stav:", self.current_stock_edit)
        
        # Inventární údaje
        inventory_label = QLabel("🔍 Inventární údaje")
        inventory_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1abc9c; margin-top: 15px;")
        form_layout.addRow(inventory_label)
        
        self.real_stock_edit = QSpinBox()
        self.real_stock_edit.setMaximum(999999)
        self.real_stock_edit.valueChanged.connect(self.calculate_difference)
        form_layout.addRow("Skutečný stav:", self.real_stock_edit)
        
        self.difference_edit = QLineEdit()
        self.difference_edit.setReadOnly(True)
        self.difference_edit.setPlaceholderText("Rozdíl se zobrazí zde")
        form_layout.addRow("Rozdíl:", self.difference_edit)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Poznámky k inventuře")
        self.notes_edit.setMaximumHeight(80)
        form_layout.addRow("Poznámky:", self.notes_edit)
        
        # Informační text
        info_label = QLabel("""
💡 Pokyny pro inventuru:
• Spočítejte skutečný počet kusů na skladě
• Zapište přesný počet do pole "Skutečný stav"
• Rozdíl bude automaticky vypočítán
• V poznámkách uveďte důvod případného rozdílu
        """)
        info_label.setStyleSheet("""
            font-size: 11px; 
            color: #7f8c8d; 
            background: #ecf0f1; 
            padding: 15px; 
            border-radius: 8px;
            margin-top: 10px;
        """)
        form_layout.addRow(info_label)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Zrušit")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Dokončit inventuru")
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
        
        # Načtení při startu
        if self.products:
            self.load_current_stock()
    
    def load_current_stock(self):
        """Načte aktuální stav vybraného produktu"""
        try:
            from database import connect
            product_id = self.product_combo.currentData()
            if product_id:
                db = connect()
                cursor = db.cursor()
                cursor.execute("SELECT current_stock FROM warehouse_products WHERE id = ?", (product_id,))
                result = cursor.fetchone()
                db.close()
                
                if result:
                    current_stock = result[0] or 0
                    self.current_stock_edit.setText(f"{current_stock} ks")
                    self.real_stock_edit.setValue(current_stock)  # Předvyplnění
                    self.calculate_difference()
        except Exception as e:
            self.current_stock_edit.setText(f"Chyba: {str(e)}")
    
    def calculate_difference(self):
        """Vypočítá rozdíl mezi skutečným a evidovaným stavem"""
        try:
            current_stock_text = self.current_stock_edit.text()
            if "ks" in current_stock_text:
                current_stock = int(current_stock_text.replace(" ks", ""))
                real_stock = self.real_stock_edit.value()
                difference = real_stock - current_stock
                
                if difference > 0:
                    self.difference_edit.setText(f"+{difference} ks (přebytek)")
                    self.difference_edit.setStyleSheet("color: green; font-weight: bold;")
                elif difference < 0:
                    self.difference_edit.setText(f"{difference} ks (manko)")
                    self.difference_edit.setStyleSheet("color: red; font-weight: bold;")
                else:
                    self.difference_edit.setText("0 ks (souhlasí)")
                    self.difference_edit.setStyleSheet("color: blue; font-weight: bold;")
        except:
            self.difference_edit.setText("Chyba výpočtu")
