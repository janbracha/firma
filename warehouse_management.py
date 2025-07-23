from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, 
    QGridLayout, QLabel, QPushButton, QComboBox, QDateEdit, QTableWidget, 
    QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QLineEdit, QTextEdit,
    QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from database import connect
from inventory_dialog import InventoryDialog

class WarehouseManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skladové hospodářství - Projekt & Develop s.r.o.")
        self.setGeometry(200, 200, 1300, 850)
        
        # Databázové připojení
        self.db = connect()

        # Hlavní widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Hlavní scroll area pro responsive design
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(scroll_area)
        
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Moderní hlavička
        self.create_header(layout)
        
        # Hlavní obsah
        self.create_content(layout)
        
        # Aplikace stylů
        self.apply_modern_styles()
        
        # Vytvoření tabulky a načtení dat
        self.create_warehouse_tables()
        self.load_inventory()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("📋 Skladové hospodářství")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Evidence materiálu, zboží a skladových operací")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa skladových operací")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Příjem zboží", "Naskladnění materiálu", self.add_stock_in),
            ("➖ Výdej zboží", "Vyskladnění materiálu", self.add_stock_out),
            ("📦 Nová položka", "Přidat nový produkt", self.add_product),
            ("📊 Inventura", "Provést inventuru skladu", self.start_inventory),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, 0, i)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Aktuální stav skladu
        stats_frame = self.create_section_frame("📊 Přehled skladu", "Aktuální stav zásob")
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        # Karty statistik
        self.products_card = self.create_stat_card("📦 Celkem položek", "0", "blue")
        self.low_stock_card = self.create_stat_card("⚠️ Nízké zásoby", "0", "orange")
        self.out_stock_card = self.create_stat_card("❌ Vyprodáno", "0", "red")
        self.value_card = self.create_stat_card("💰 Hodnota skladu", "0 Kč", "green")
        
        stats_grid.addWidget(self.products_card, 0, 0)
        stats_grid.addWidget(self.low_stock_card, 0, 1)
        stats_grid.addWidget(self.out_stock_card, 0, 2)
        stats_grid.addWidget(self.value_card, 0, 3)
        
        stats_frame.layout().addLayout(stats_grid)
        layout.addWidget(stats_frame)
        
        # Tabulka produktů
        table_frame = self.create_section_frame("📋 Aktuální zásoby", "Přehled všech produktů ve skladu")
        
        # Tabulka zásob
        self.table = QTableWidget(0, 8)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "ID", "Název", "Kategorie", "Množství", "Jednotka", 
            "Min. zásoba", "Cena", "Celková hodnota"
        ])
        
        # Nastavení tabulky
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        table_frame.layout().addWidget(self.table)
        layout.addWidget(table_frame)

    def create_section_frame(self, title, subtitle):
        """Vytvoří rám pro sekci"""
        frame = QFrame()
        frame.setObjectName("sectionFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Hlavička sekce
        header_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setObjectName("sectionTitle")
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("sectionSubtitle")
        header_layout.addWidget(subtitle_label)
        
        layout.addLayout(header_layout)
        
        return frame
    
    def create_action_card(self, title, description, callback):
        """Vytvoří kartu pro akci"""
        card = QFrame()
        card.setObjectName("actionCard")
        card.setFixedSize(300, 120)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setObjectName("cardDescription")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # Kliknutí na kartu
        def mousePressEvent(event):
            if event.button() == Qt.MouseButton.LeftButton:
                callback()
        
        card.mousePressEvent = mousePressEvent
        
        return card
    
    def create_stat_card(self, title, value, color):
        """Vytvoří kartu pro statistiku"""
        card = QFrame()
        card.setObjectName(f"statCard_{color}")
        card.setFixedSize(300, 100)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setObjectName("statTitle")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        layout.addWidget(value_label)
        
        return card

    def apply_modern_styles(self):
        """Aplikuje moderní styly"""
        self.setStyleSheet("""
            /* Hlavní okno */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(26, 188, 156, 1.0),
                    stop:1 rgba(22, 160, 133, 1.0));
            }
            
            /* Scroll area */
            QScrollArea {
                border: none;
                background: transparent;
            }
            
            /* Header */
            #headerFrame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                margin-bottom: 20px;
            }
            
            #titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin: 0;
            }
            
            #subtitleLabel {
                font-size: 14px;
                color: #7f8c8d;
                margin: 0;
            }
            
            /* Sekce */
            #sectionFrame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                margin-bottom: 20px;
            }
            
            #sectionTitle {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            
            #sectionSubtitle {
                font-size: 13px;
                color: #7f8c8d;
                margin-bottom: 15px;
            }
            
            /* Karty akcí */
            #actionCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(247, 249, 252, 0.9));
                border: 2px solid rgba(26, 188, 156, 0.1);
                border-radius: 12px;
                margin: 5px;
            }
            
            #actionCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 1.0),
                    stop:1 rgba(240, 248, 255, 1.0));
                border: 2px solid rgba(26, 188, 156, 0.3);
            }
            
            #cardTitle {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 3px;
            }
            
            #cardDescription {
                font-size: 12px;
                color: #7f8c8d;
                line-height: 1.3;
            }
            
            /* Statistické karty */
            #statCard_blue {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(52, 152, 219, 0.9),
                    stop:1 rgba(41, 128, 185, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(41, 128, 185, 0.3);
            }
            
            #statCard_orange {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(230, 126, 34, 0.9),
                    stop:1 rgba(211, 84, 0, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(211, 84, 0, 0.3);
            }
            
            #statCard_red {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(231, 76, 60, 0.9),
                    stop:1 rgba(192, 57, 43, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(192, 57, 43, 0.3);
            }
            
            #statCard_green {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.9),
                    stop:1 rgba(39, 174, 96, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(39, 174, 96, 0.3);
            }
            
            #statTitle {
                font-size: 12px;
                font-weight: bold;
                color: white;
                margin-bottom: 5px;
            }
            
            #statValue {
                font-size: 18px;
                font-weight: bold;
                color: white;
            }
            
            /* Tabulka */
            #dataTable {
                background: white;
                alternate-background-color: #f8f9fa;
                border: 1px solid rgba(26, 188, 156, 0.2);
                border-radius: 8px;
                gridline-color: rgba(26, 188, 156, 0.1);
                font-size: 12px;
                selection-background-color: rgba(26, 188, 156, 0.2);
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(26, 188, 156, 0.8),
                    stop:1 rgba(26, 188, 156, 0.6));
                color: white;
                font-weight: bold;
                font-size: 11px;
                padding: 8px;
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)

    def create_warehouse_tables(self):
        """Vytvoří tabulky pro skladové hospodářství"""
        try:
            cursor = self.db.cursor()
            
            # Tabulka produktů
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS warehouse_products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    description TEXT,
                    unit TEXT,
                    price REAL,
                    min_stock INTEGER DEFAULT 0,
                    current_stock INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabulka skladových pohybů
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS warehouse_movements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    movement_type TEXT,
                    quantity INTEGER,
                    price REAL,
                    date TEXT,
                    description TEXT,
                    user_id TEXT,
                    FOREIGN KEY (product_id) REFERENCES warehouse_products (id)
                )
            """)
            
            self.db.commit()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při vytváření tabulek: {str(e)}")

    def load_inventory(self):
        """Načte aktuální stav skladu"""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT id, name, category, current_stock, unit, min_stock, price,
                       (current_stock * price) as total_value
                FROM warehouse_products 
                ORDER BY name
            """)
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            
            total_products = len(rows)
            low_stock_count = 0
            out_stock_count = 0
            total_value = 0
            
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    if col_idx in [6, 7]:  # Cenové sloupce
                        if value is not None:
                            formatted_value = f"{float(value):,.2f} Kč"
                        else:
                            formatted_value = "0,00 Kč"
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(formatted_value))
                    else:
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))
                
                # Statistiky
                current_stock = row[3] if row[3] else 0
                min_stock = row[5] if row[5] else 0
                value = row[7] if row[7] else 0
                
                if current_stock == 0:
                    out_stock_count += 1
                elif current_stock <= min_stock:
                    low_stock_count += 1
                    
                total_value += value
                
            # Aktualizace karet
            self.update_stat_card(self.products_card, str(total_products))
            self.update_stat_card(self.low_stock_card, str(low_stock_count))
            self.update_stat_card(self.out_stock_card, str(out_stock_count))
            self.update_stat_card(self.value_card, f"{total_value:,.2f} Kč")
            
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání skladu: {str(e)}")
    
    def update_stat_card(self, card, value):
        """Aktualizuje hodnotu ve statistické kartě"""
        layout = card.layout()
        if layout and layout.count() > 1:
            value_label = layout.itemAt(1).widget()
            if value_label:
                value_label.setText(value)

    def add_product(self):
        """Přidá nový produkt do skladu"""
        dialog = ProductDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO warehouse_products (name, category, description, unit, 
                                                  price, min_stock, current_stock) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    dialog.name_edit.text(),
                    dialog.category_edit.text(),
                    dialog.description_edit.toPlainText(),
                    dialog.unit_edit.text(),
                    dialog.price_edit.value(),
                    dialog.min_stock_edit.value(),
                    0  # Počáteční stav
                ))
                self.db.commit()
                self.load_inventory()
                QMessageBox.information(self, "Úspěch", "Produkt byl úspěšně přidán!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při přidávání produktu: {str(e)}")

    def add_stock_in(self):
        """Přidá příjem zboží"""
        dialog = StockMovementDialog("Příjem zboží", self.get_products())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                product_id = dialog.product_combo.currentData()
                quantity = dialog.quantity_edit.value()
                
                cursor = self.db.cursor()
                
                # Záznam pohybu
                cursor.execute("""
                    INSERT INTO warehouse_movements (product_id, movement_type, quantity, 
                                                   date, description) 
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    product_id,
                    "Příjem",
                    quantity,
                    QDate.currentDate().toString("yyyy-MM-dd"),
                    dialog.description_edit.toPlainText()
                ))
                
                # Aktualizace stavu
                cursor.execute("""
                    UPDATE warehouse_products 
                    SET current_stock = current_stock + ? 
                    WHERE id = ?
                """, (quantity, product_id))
                
                self.db.commit()
                self.load_inventory()
                QMessageBox.information(self, "Úspěch", "Příjem zboží byl zaznamenán!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při příjmu zboží: {str(e)}")

    def add_stock_out(self):
        """Přidá výdej zboží"""
        dialog = StockMovementDialog("Výdej zboží", self.get_products())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                product_id = dialog.product_combo.currentData()
                quantity = dialog.quantity_edit.value()
                
                cursor = self.db.cursor()
                
                # Kontrola dostupnosti
                cursor.execute("SELECT current_stock FROM warehouse_products WHERE id = ?", (product_id,))
                current_stock = cursor.fetchone()[0]
                
                if current_stock < quantity:
                    QMessageBox.warning(self, "Upozornění", 
                                      f"Nedostatek zásob! Dostupné množství: {current_stock}")
                    return
                
                # Záznam pohybu
                cursor.execute("""
                    INSERT INTO warehouse_movements (product_id, movement_type, quantity, 
                                                   date, description) 
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    product_id,
                    "Výdej",
                    quantity,
                    QDate.currentDate().toString("yyyy-MM-dd"),
                    dialog.description_edit.toPlainText()
                ))
                
                # Aktualizace stavu
                cursor.execute("""
                    UPDATE warehouse_products 
                    SET current_stock = current_stock - ? 
                    WHERE id = ?
                """, (quantity, product_id))
                
                self.db.commit()
                self.load_inventory()
                QMessageBox.information(self, "Úspěch", "Výdej zboží byl zaznamenán!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při výdeji zboží: {str(e)}")

    def get_products(self):
        """Vrátí seznam produktů pro combo box"""
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT id, name FROM warehouse_products ORDER BY name")
            return cursor.fetchall()
        except:
            return []

    def start_inventory(self):
        """Spustí inventuru"""
        dialog = InventoryDialog(self.get_products())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor = self.db.cursor()
                product_id = dialog.product_combo.currentData()
                real_stock = dialog.real_stock_edit.value()
                
                # Zjištění současného stavu
                cursor.execute("SELECT current_stock, name FROM warehouse_products WHERE id = ?", (product_id,))
                result = cursor.fetchone()
                current_stock = result[0]
                product_name = result[1]
                
                # Výpočet rozdílu
                difference = real_stock - current_stock
                
                if difference != 0:
                    # Aktualizace stavu
                    cursor.execute("""
                        UPDATE warehouse_products 
                        SET current_stock = ? 
                        WHERE id = ?
                    """, (real_stock, product_id))
                    
                    # Záznam pohybu
                    movement_type = "Inventurní přebytek" if difference > 0 else "Inventurní manko"
                    cursor.execute("""
                        INSERT INTO warehouse_movements (product_id, movement_type, quantity, 
                                                       date, description) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        product_id,
                        movement_type,
                        abs(difference),
                        QDate.currentDate().toString("yyyy-MM-dd"),
                        f"Inventura - {dialog.notes_edit.toPlainText()}"
                    ))
                    
                    self.db.commit()
                    self.load_inventory()
                    
                    if difference > 0:
                        QMessageBox.information(self, "✅ Inventura dokončena", 
                                              f"Přebytek u {product_name}: +{difference} ks")
                    else:
                        QMessageBox.warning(self, "⚠️ Inventura dokončena", 
                                          f"Manko u {product_name}: {difference} ks")
                else:
                    QMessageBox.information(self, "✅ Inventura dokončena", 
                                          f"Stav {product_name} souhlasí - žádný rozdíl.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při inventuře: {str(e)}")

    def closeEvent(self, event):
        """Uzavře databázové připojení při zavření okna"""
        if hasattr(self, 'db'):
            self.db.close()
        event.accept()


class ProductDialog(QDialog):
    """Dialog pro přidání produktu"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nový produkt")
        self.setFixedSize(500, 500)
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
            QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox {
                padding: 10px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 12px;
                background: white;
                margin-bottom: 10px;
            }
            QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus {
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
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Název produktu")
        form_layout.addRow("Název:", self.name_edit)
        
        self.category_edit = QLineEdit()
        self.category_edit.setPlaceholderText("Např. Materiál, Náhradní díly...")
        form_layout.addRow("Kategorie:", self.category_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Popis produktu")
        self.description_edit.setMaximumHeight(80)
        form_layout.addRow("Popis:", self.description_edit)
        
        self.unit_edit = QLineEdit()
        self.unit_edit.setPlaceholderText("ks, m, kg, l...")
        form_layout.addRow("Jednotka:", self.unit_edit)
        
        self.price_edit = QDoubleSpinBox()
        self.price_edit.setMaximum(999999.99)
        self.price_edit.setSuffix(" Kč")
        form_layout.addRow("Cena za jednotku:", self.price_edit)
        
        self.min_stock_edit = QSpinBox()
        self.min_stock_edit.setMaximum(999999)
        form_layout.addRow("Minimální zásoba:", self.min_stock_edit)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Uložit")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)


class StockMovementDialog(QDialog):
    """Dialog pro skladové pohyby"""
    
    def __init__(self, title, products, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(500, 400)
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
            QComboBox, QSpinBox, QTextEdit {
                padding: 10px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 12px;
                background: white;
                margin-bottom: 10px;
            }
            QComboBox:focus, QSpinBox:focus, QTextEdit:focus {
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
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Formulář
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.product_combo = QComboBox()
        for product_id, product_name in self.products:
            self.product_combo.addItem(product_name, product_id)
        form_layout.addRow("Produkt:", self.product_combo)
        
        self.quantity_edit = QSpinBox()
        self.quantity_edit.setMaximum(999999)
        self.quantity_edit.setValue(1)
        form_layout.addRow("Množství:", self.quantity_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Poznámka k pohybu")
        self.description_edit.setMaximumHeight(100)
        form_layout.addRow("Popis:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Uložit")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
