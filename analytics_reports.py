from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, 
    QGridLayout, QLabel, QPushButton, QComboBox, QDateEdit, QTableWidget, 
    QTableWidgetItem, QMessageBox, QGroupBox, QTextEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QPainter
from database import connect
import sqlite3
from datetime import datetime, timedelta

class AnalyticsReportsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analýzy a reporty - Projekt & Develop s.r.o.")
        self.setGeometry(200, 200, 1400, 900)
        
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
        
        # Načtení dat
        self.load_analytics()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("📈 Analýzy a reporty")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Finanční analýzy, statistiky a business intelligence")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Rychlé metriky
        metrics_frame = self.create_section_frame("⚡ Klíčové ukazatele", "Aktuální stav firmy")
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(15)
        
        # Karty metrik
        self.revenue_card = self.create_metric_card("💰 Celkové příjmy", "0 Kč", "green")
        self.expenses_card = self.create_metric_card("💸 Celkové výdaje", "0 Kč", "red")
        self.profit_card = self.create_metric_card("📊 Zisk", "0 Kč", "blue")
        self.invoices_card = self.create_metric_card("📄 Počet faktur", "0", "orange")
        
        metrics_grid.addWidget(self.revenue_card, 0, 0)
        metrics_grid.addWidget(self.expenses_card, 0, 1)
        metrics_grid.addWidget(self.profit_card, 0, 2)
        metrics_grid.addWidget(self.invoices_card, 0, 3)
        
        metrics_frame.layout().addLayout(metrics_grid)
        layout.addWidget(metrics_frame)
        
        # Filtrování a akce
        filter_frame = self.create_section_frame("🔍 Filtrování a exporty", "Nastavení analýz a generování reportů")
        filter_layout = QHBoxLayout()
        
        # Datum od
        filter_layout.addWidget(QLabel("Od:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-12))
        self.date_from.setCalendarPopup(True)
        filter_layout.addWidget(self.date_from)
        
        # Datum do
        filter_layout.addWidget(QLabel("Do:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        filter_layout.addWidget(self.date_to)
        
        # Tlačítka
        refresh_btn = QPushButton("🔄 Aktualizovat")
        refresh_btn.clicked.connect(self.load_analytics)
        filter_layout.addWidget(refresh_btn)
        
        export_excel_btn = QPushButton("📊 Export Excel")
        export_excel_btn.clicked.connect(self.export_to_excel)
        filter_layout.addWidget(export_excel_btn)
        
        export_pdf_btn = QPushButton("📄 Report PDF")
        export_pdf_btn.clicked.connect(self.export_to_pdf)
        filter_layout.addWidget(export_pdf_btn)
        
        filter_layout.addStretch()
        
        filter_frame.layout().addLayout(filter_layout)
        layout.addWidget(filter_frame)
        
        # Detailní analýzy
        details_layout = QHBoxLayout()
        
        # Levá strana - tabulky
        left_group = QGroupBox("📋 Detailní přehledy")
        left_layout = QVBoxLayout(left_group)
        
        # Tabulka příjmů/výdajů
        self.summary_table = QTableWidget(0, 4)
        self.summary_table.setObjectName("dataTable")
        self.summary_table.setHorizontalHeaderLabels(["Kategorie", "Počet", "Částka", "Podíl"])
        self.summary_table.setMaximumHeight(200)
        left_layout.addWidget(QLabel("💼 Přehled podle kategorií:"))
        left_layout.addWidget(self.summary_table)
        
        # Tabulka nejlepších klientů
        self.clients_table = QTableWidget(0, 3)
        self.clients_table.setObjectName("dataTable")
        self.clients_table.setHorizontalHeaderLabels(["Klient", "Počet faktur", "Celková částka"])
        self.clients_table.setMaximumHeight(200)
        left_layout.addWidget(QLabel("🏆 Top klienti:"))
        left_layout.addWidget(self.clients_table)
        
        details_layout.addWidget(left_group)
        
        # Pravá strana - statistiky
        right_group = QGroupBox("📊 Statistiky a trendy")
        right_layout = QVBoxLayout(right_group)
        
        # Měsíční přehled
        self.monthly_table = QTableWidget(0, 4)
        self.monthly_table.setObjectName("dataTable")
        self.monthly_table.setHorizontalHeaderLabels(["Měsíc", "Příjmy", "Výdaje", "Zisk"])
        right_layout.addWidget(QLabel("📅 Měsíční vývoj:"))
        right_layout.addWidget(self.monthly_table)
        
        details_layout.addWidget(right_group)
        
        layout.addLayout(details_layout)

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
    
    def create_metric_card(self, title, value, color):
        """Vytvoří kartu pro metriku"""
        card = QFrame()
        card.setObjectName(f"metricCard_{color}")
        card.setFixedSize(320, 100)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setObjectName("metricTitle")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("metricValue")
        layout.addWidget(value_label)
        
        return card

    def apply_modern_styles(self):
        """Aplikuje moderní styly"""
        self.setStyleSheet("""
            /* Hlavní okno */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(45, 62, 80, 1.0),
                    stop:1 rgba(52, 73, 94, 1.0));
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
            
            /* Metriky karty */
            #metricCard_green {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.9),
                    stop:1 rgba(39, 174, 96, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(39, 174, 96, 0.3);
            }
            
            #metricCard_red {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(231, 76, 60, 0.9),
                    stop:1 rgba(192, 57, 43, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(192, 57, 43, 0.3);
            }
            
            #metricCard_blue {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(52, 152, 219, 0.9),
                    stop:1 rgba(41, 128, 185, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(41, 128, 185, 0.3);
            }
            
            #metricCard_orange {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(230, 126, 34, 0.9),
                    stop:1 rgba(211, 84, 0, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(211, 84, 0, 0.3);
            }
            
            #metricTitle {
                font-size: 12px;
                font-weight: bold;
                color: white;
                margin-bottom: 5px;
            }
            
            #metricValue {
                font-size: 20px;
                font-weight: bold;
                color: white;
            }
            
            /* Tlačítka */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                margin: 2px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
            
            /* Tabulky */
            #dataTable {
                background: white;
                alternate-background-color: #f8f9fa;
                border: 1px solid rgba(108, 133, 163, 0.2);
                border-radius: 8px;
                gridline-color: rgba(108, 133, 163, 0.1);
                font-size: 11px;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(108, 133, 163, 0.8),
                    stop:1 rgba(108, 133, 163, 0.6));
                color: white;
                font-weight: bold;
                font-size: 10px;
                padding: 6px;
                border: none;
            }
            
            /* GroupBox */
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid rgba(108, 133, 163, 0.2);
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                background: white;
            }
            
            /* Datum editory */
            QDateEdit {
                padding: 8px;
                border: 2px solid #e1e8ed;
                border-radius: 6px;
                font-size: 11px;
                background: white;
                margin: 2px;
            }
            
            QDateEdit:focus {
                border-color: #3498db;
            }
        """)

    def load_analytics(self):
        """Načte analytická data"""
        try:
            date_from = self.date_from.date().toString("yyyy-MM-dd")
            date_to = self.date_to.date().toString("yyyy-MM-dd")
            
            cursor = self.db.cursor()
            
            # Celkové příjmy z faktur
            cursor.execute("""
                SELECT COALESCE(SUM(total), 0) FROM invoices 
                WHERE issue_date BETWEEN ? AND ? AND type = 'vydaná'
            """, (date_from, date_to))
            total_revenue = cursor.fetchone()[0]
            
            # Celkové výdaje z pokladny
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM cash_journal 
                WHERE date BETWEEN ? AND ? AND type = 'výdaj'
            """, (date_from, date_to))
            total_expenses = cursor.fetchone()[0]
            
            # Počet faktur
            cursor.execute("""
                SELECT COUNT(*) FROM invoices 
                WHERE issue_date BETWEEN ? AND ?
            """, (date_from, date_to))
            invoice_count = cursor.fetchone()[0]
            
            # Aktualizace karet
            profit = total_revenue - total_expenses
            
            self.update_metric_card(self.revenue_card, f"{total_revenue:,.2f} Kč")
            self.update_metric_card(self.expenses_card, f"{total_expenses:,.2f} Kč")
            self.update_metric_card(self.profit_card, f"{profit:,.2f} Kč")
            self.update_metric_card(self.invoices_card, str(invoice_count))
            
            # Načtení detailních dat
            self.load_summary_data(date_from, date_to)
            self.load_top_clients(date_from, date_to)
            self.load_monthly_data(date_from, date_to)
            
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání analýz: {str(e)}")
    
    def update_metric_card(self, card, value):
        """Aktualizuje hodnotu v metrické kartě"""
        value_label = card.findChild(QLabel, "metricValue")
        if not value_label:
            # Najdeme label podle pozice
            layout = card.layout()
            if layout and layout.count() > 1:
                value_label = layout.itemAt(1).widget()
        
        if value_label:
            value_label.setText(value)
    
    def load_summary_data(self, date_from, date_to):
        """Načte souhrnná data podle kategorií"""
        try:
            # Blokujeme signály pro zabránění varování dataChanged
            self.summary_table.blockSignals(True)
            
            cursor = self.db.cursor()
            
            # Data pro souhrn
            summary_data = [
                ("Vydané faktury", "invoices", "type = 'vydaná'", "total"),
                ("Přijaté faktury", "invoices", "type = 'přijatá'", "total"),
                ("Příjmy pokladna", "cash_journal", "type = 'příjem'", "amount"),
                ("Výdaje pokladna", "cash_journal", "type = 'výdaj'", "amount"),
            ]
            
            # Vyčistíme tabulku a nastavíme počet řádků
            self.summary_table.clearContents()
            self.summary_table.setRowCount(len(summary_data))
            
            for row, (category, table, condition, amount_col) in enumerate(summary_data):
                # Počet záznamů
                cursor.execute(f"""
                    SELECT COUNT(*), COALESCE(SUM({amount_col}), 0) 
                    FROM {table} 
                    WHERE date BETWEEN ? AND ? AND {condition}
                """, (date_from, date_to))
                
                count, total = cursor.fetchone()
                
                self.summary_table.setItem(row, 0, QTableWidgetItem(category))
                self.summary_table.setItem(row, 1, QTableWidgetItem(str(count)))
                self.summary_table.setItem(row, 2, QTableWidgetItem(f"{total:,.2f} Kč"))
                self.summary_table.setItem(row, 3, QTableWidgetItem("100%"))  # TODO: Vypočítat podíl
            
        except Exception as e:
            print(f"Chyba při načítání souhrnu: {e}")
        finally:
            # Obnovíme signály
            self.summary_table.blockSignals(False)
    
    def load_top_clients(self, date_from, date_to):
        """Načte top klienty"""
        try:
            # Blokujeme signály pro zabránění varování dataChanged
            self.clients_table.blockSignals(True)
            
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT recipient, COUNT(*) as count, SUM(total) as total_amount
                FROM invoices 
                WHERE issue_date BETWEEN ? AND ? AND type = 'vydaná'
                GROUP BY recipient 
                ORDER BY total_amount DESC 
                LIMIT 10
            """, (date_from, date_to))
            
            clients = cursor.fetchall()
            
            # Vyčistíme tabulku a nastavíme počet řádků
            self.clients_table.clearContents()
            self.clients_table.setRowCount(len(clients))
            
            for row, (client, count, total) in enumerate(clients):
                self.clients_table.setItem(row, 0, QTableWidgetItem(client or "N/A"))
                self.clients_table.setItem(row, 1, QTableWidgetItem(str(count)))
                self.clients_table.setItem(row, 2, QTableWidgetItem(f"{total:,.2f} Kč"))
                
        except Exception as e:
            print(f"Chyba při načítání klientů: {e}")
        finally:
            # Obnovíme signály
            self.clients_table.blockSignals(False)
    
    def load_monthly_data(self, date_from, date_to):
        """Načte měsíční data"""
        try:
            cursor = self.db.cursor()
            
            # Generování měsíců v rozsahu
            from datetime import datetime
            start_date = datetime.strptime(date_from, "%Y-%m-%d")
            end_date = datetime.strptime(date_to, "%Y-%m-%d")
            
            months = []
            current = start_date.replace(day=1)
            
            while current <= end_date:
                month_start = current.strftime("%Y-%m-01")
                if current.month == 12:
                    month_end = current.replace(year=current.year + 1, month=1, day=1) - timedelta(days=1)
                else:
                    month_end = current.replace(month=current.month + 1) - timedelta(days=1)
                month_end_str = month_end.strftime("%Y-%m-%d")
                
                # Příjmy
                cursor.execute("""
                    SELECT COALESCE(SUM(total), 0) FROM invoices 
                    WHERE issue_date BETWEEN ? AND ? AND type = 'vydaná'
                """, (month_start, month_end_str))
                revenue = cursor.fetchone()[0]
                
                # Výdaje
                cursor.execute("""
                    SELECT COALESCE(SUM(amount), 0) FROM cash_journal 
                    WHERE date BETWEEN ? AND ? AND type = 'výdaj'
                """, (month_start, month_end_str))
                expenses = cursor.fetchone()[0]
                
                months.append((
                    current.strftime("%Y-%m"),
                    revenue,
                    expenses,
                    revenue - expenses
                ))
                
                if current.month == 12:
                    current = current.replace(year=current.year + 1, month=1)
                else:
                    current = current.replace(month=current.month + 1)
            
            # Zobrazení v tabulce
            # Blokujeme signály pro zabránění varování dataChanged
            self.monthly_table.blockSignals(True)
            
            # Vyčistíme tabulku a nastavíme počet řádků
            self.monthly_table.clearContents()
            self.monthly_table.setRowCount(len(months))
            
            for row, (month, revenue, expenses, profit) in enumerate(months):
                self.monthly_table.setItem(row, 0, QTableWidgetItem(month))
                self.monthly_table.setItem(row, 1, QTableWidgetItem(f"{revenue:,.2f} Kč"))
                self.monthly_table.setItem(row, 2, QTableWidgetItem(f"{expenses:,.2f} Kč"))
                self.monthly_table.setItem(row, 3, QTableWidgetItem(f"{profit:,.2f} Kč"))
            
            # Obnovíme signály
            self.monthly_table.blockSignals(False)
                
        except Exception as e:
            print(f"Chyba při načítání měsíčních dat: {e}")
    
    def export_to_excel(self):
        """Export do Excel"""
        try:
            from PyQt6.QtWidgets import QFileDialog
            import csv
            from datetime import datetime
            
            # Výběr souboru
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                "Uložit Excel export",
                f"analyza_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV soubory (*.csv)"
            )
            
            if filename:
                cursor = self.db.cursor()
                
                # Získání dat pro export
                cursor.execute("""
                    SELECT 'Faktury' as typ, COUNT(*) as pocet, SUM(total) as suma
                    FROM invoices
                    UNION ALL
                    SELECT 'Příjmy', COUNT(*), SUM(amount) 
                    FROM cash_journal WHERE type = 'Příjem'
                    UNION ALL  
                    SELECT 'Výdaje', COUNT(*), SUM(amount)
                    FROM cash_journal WHERE type = 'Výdaj'
                    UNION ALL
                    SELECT 'Majetek', COUNT(*), SUM(purchase_price)
                    FROM assets WHERE status = 'Aktivní'
                """)
                data = cursor.fetchall()
                
                # Zápis do CSV
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    writer.writerow(['Typ', 'Počet', 'Celková částka'])
                    writer.writerows(data)
                    
                    # Prázdný řádek a datum exportu
                    writer.writerow([])
                    writer.writerow(['Export vytvořen:', datetime.now().strftime('%d.%m.%Y %H:%M')])
                
                QMessageBox.information(self, "✅ Úspěch", f"Data byla exportována do:\n{filename}")
                
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při exportu: {str(e)}")
    
    def export_to_pdf(self):
        """Export do PDF"""
        try:
            from PyQt6.QtWidgets import QFileDialog
            from PyQt6.QtGui import QPainter, QFont
            from PyQt6.QtPrintSupport import QPrinter
            from datetime import datetime
            
            # Výběr souboru
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                "Uložit PDF report",
                f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                "PDF soubory (*.pdf)"
            )
            
            if filename:
                cursor = self.db.cursor()
                
                # Získání dat
                cursor.execute("""
                    SELECT COUNT(*) as pocet_faktur, SUM(total) as suma_faktur
                    FROM invoices
                """)
                invoice_data = cursor.fetchone()
                
                cursor.execute("""
                    SELECT SUM(amount) as prijem
                    FROM cash_journal WHERE type = 'Příjem'
                """)
                income = cursor.fetchone()[0] or 0
                
                cursor.execute("""
                    SELECT SUM(amount) as vydaj  
                    FROM cash_journal WHERE type = 'Výdaj'
                """)
                expense = cursor.fetchone()[0] or 0
                
                # Vytvoření PDF
                printer = QPrinter()
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(filename)
                
                painter = QPainter()
                painter.begin(printer)
                
                # Fonty
                title_font = QFont("Arial", 16, QFont.Weight.Bold)
                normal_font = QFont("Arial", 12)
                
                y = 100
                
                # Nadpis
                painter.setFont(title_font)
                painter.drawText(100, y, "Finanční report - Projekt & Develop s.r.o.")
                y += 80
                
                # Datum
                painter.setFont(normal_font)
                painter.drawText(100, y, f"Vytvořeno: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
                y += 60
                
                # Data
                painter.drawText(100, y, f"Počet faktur: {invoice_data[0] or 0}")
                y += 40
                painter.drawText(100, y, f"Celkový obrat: {invoice_data[1] or 0:,.2f} Kč")
                y += 40
                painter.drawText(100, y, f"Příjmy pokladny: {income:,.2f} Kč")
                y += 40
                painter.drawText(100, y, f"Výdaje pokladny: {expense:,.2f} Kč")
                y += 40
                painter.drawText(100, y, f"Zisk/ztráta: {income - expense:,.2f} Kč")
                
                painter.end()
                
                QMessageBox.information(self, "✅ Úspěch", f"PDF report byl vytvořen:\n{filename}")
                
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při vytváření PDF: {str(e)}")

    def closeEvent(self, event):
        """Uzavře databázové připojení při zavření okna"""
        if hasattr(self, 'db'):
            self.db.close()
        event.accept()
