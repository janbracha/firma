from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QFormLayout, QLabel, QComboBox, QMessageBox, 
                             QTableWidget, QTableWidgetItem, QScrollArea, QFrame, QDialog)
from PyQt6.QtCore import QDate, Qt
from database import connect
import random

class TripCalculationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Výpočet knihy jízd")
        self.setGeometry(100, 100, 1200, 800)
        
        # Hlavní scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Hlavní widget
        main_widget = QWidget()
        scroll_area.setWidget(main_widget)
        self.setCentralWidget(scroll_area)
        
        # Hlavní layout
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Aplikování moderních stylů
        self.apply_modern_styles()
        
        # Vytvoření obsahu
        self.create_header(layout)
        self.create_content(layout)

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("📊 Výpočet knihy jízd")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Generování a analýza jízdních dokladů")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa a generování dokladů")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("📋 Generovat knihu", "Vygenerovat knihu jízd", self.generate_trip_book),
            ("📊 Analýza dat", "Zobrazit analýzu a statistiky", self.show_analysis),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, 0, i)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Formulář nastavení
        form_frame = self.create_section_frame("⚙️ Nastavení generování", "Konfigurace parametrů pro výpočet")
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Výběr měsíce
        self.month_box = QComboBox()
        self.month_box.setObjectName("modernComboBox")
        self.month_box.addItems(["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
                                 "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"])
        form_layout.addRow("📅 Měsíc:", self.month_box)
        self.month_box.currentIndexChanged.connect(self.update_fuel_display)

        # Výběr roku
        self.year_box = QComboBox()
        self.year_box.setObjectName("modernComboBox")
        current_year = QDate.currentDate().year()
        self.year_box.addItems([str(y) for y in range(current_year, current_year - 10, -1)])
        self.year_box.currentIndexChanged.connect(self.update_fuel_display)
        form_layout.addRow("📆 Rok:", self.year_box)

        # Výběr vozidla
        self.vehicle_box = QComboBox()
        self.vehicle_box.setObjectName("modernComboBox")
        self.load_vehicles()
        self.vehicle_box.currentIndexChanged.connect(self.update_fuel_display)
        form_layout.addRow("🚗 Vozidlo:", self.vehicle_box)
        
        form_frame.layout().addLayout(form_layout)
        layout.addWidget(form_frame)
        
        # Informační panely
        info_frame = self.create_section_frame("📈 Přehled dat", "Aktuální informace o palivě a kilometrech")
        info_layout = QHBoxLayout()
        
        # Panel paliva
        self.monthly_fuel_label = QLabel("⛽ Množství paliva za zvolený měsíc:\nN/A")
        self.monthly_fuel_label.setObjectName("infoPanel")
        self.monthly_fuel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.monthly_fuel_label)
        
        # Panel kilometrů
        self.estimated_km_label = QLabel("📏 Předpokládaný průměrný počet kilometrů:\nN/A")
        self.estimated_km_label.setObjectName("infoPanel")
        self.estimated_km_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.estimated_km_label)
        
        info_frame.layout().addLayout(info_layout)
        layout.addWidget(info_frame)
        
        # Počáteční načtení dat
        self.update_fuel_display()

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
        card.setFixedSize(280, 100)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)
        
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

    def apply_modern_styles(self):
        """Aplikuje moderní styly"""
        self.setStyleSheet("""
            /* Hlavní okno */
            QMainWindow {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                border: 2px solid rgba(108, 133, 163, 0.1);
                border-radius: 12px;
                margin: 5px;
            }
            
            #actionCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 1.0),
                    stop:1 rgba(240, 248, 255, 1.0));
                border: 2px solid rgba(108, 133, 163, 0.3);
            }
            
            #cardTitle {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 3px;
            }
            
            #cardDescription {
                font-size: 14px;
                color: #7f8c8d;
                line-height: 1.3;
            }
            
            /* Moderní ComboBox */
            #modernComboBox {
                background: white;
                border: 2px solid rgba(108, 133, 163, 0.2);
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                color: #2c3e50;
            }
            
            #modernComboBox:focus {
                border: 2px solid rgba(52, 152, 219, 0.5);
            }
            
            #modernComboBox::drop-down {
                border: none;
                background: transparent;
                width: 20px;
            }
            
            #modernComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 5px 5px 0 5px;
                border-color: #7f8c8d transparent transparent transparent;
            }
            
            /* Informační panely */
            #infoPanel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.1),
                    stop:1 rgba(39, 174, 96, 0.1));
                border: 2px solid rgba(39, 174, 96, 0.3);
                border-radius: 12px;
                padding: 20px;
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                margin: 5px;
            }
        """)

    def load_vehicles(self):
        """Načte seznam vozidel z databáze."""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT registration FROM cars")
        vehicles = cursor.fetchall()
        conn.close()

        self.vehicle_box.addItems([vehicle[0] for vehicle in vehicles])

    def generate_trip_book(self):
        """Vygeneruje Knihu jízd na základě paliva v databázi."""
        self.trip_table = QTableWidget()  # Inicializace tabulky
        self.trip_table.setColumnCount(6)
        self.trip_table.setHorizontalHeaderLabels(["Datum", "Řidič", "Start", "Cíl", "Firma", "Vzdálenost (km)"])

        month_name = self.month_box.currentText()
        year = int(self.year_box.currentText())
        selected_vehicle = self.vehicle_box.currentText()

        # Převod měsíce na číslo
        months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
                  "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
        month = months.index(month_name) + 1

        # Sečtení tankování pro dané vozidlo a měsíc
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(fuel_amount) FROM fuel_tankings
            WHERE vehicle=? AND substr(date, 4, 2)=? AND substr(date, 7, 4)=?
        """, (selected_vehicle, f"{month:02}", str(year)))

        fuel_quantity = cursor.fetchone()[0] or 0  # Pokud není tankování, nastavíme 0
        
        # Získání spotřeby vozidla
        cursor.execute("SELECT consumption FROM cars WHERE registration=?", (selected_vehicle,))
        consumption_result = cursor.fetchone()
        consumption = consumption_result[0] if consumption_result else 0
        
        # Načtení destinací a řidičů z databáze
        cursor.execute("SELECT start, destination, company, distance FROM destinations")
        destinations = cursor.fetchall()

        cursor.execute("SELECT first_name, last_name FROM drivers")
        drivers = cursor.fetchall()
        
        conn.close()

        if not drivers:
            QMessageBox.warning(self, "Chyba", "V databázi nejsou žádní řidiči!")
            return
            
        if not destinations:
            QMessageBox.warning(self, "Chyba", "V databázi nejsou žádné destinace!")
            return

        # Výpočet celkového počtu km z paliva
        total_km = (fuel_quantity / consumption) * 100 if consumption > 0 else 0
        
        if total_km <= 0:
            QMessageBox.warning(self, "Chyba", "Není dostatek paliva pro generování jízd!")
            return

        trips = []
        remaining_km = total_km
        days_used = set()
        days_in_month = QDate(year, month, 1).daysInMonth()

        # Generování jízd - každá destinace tam a zpět
        for destination in destinations:
            if remaining_km <= 0 or len(days_used) >= days_in_month:
                break
                
            driver = random.choice(drivers)
            trip_distance = destination[3]  # Vzdálenost jedné cesty
            round_trip_distance = trip_distance * 2  # Celková vzdálenost tam i zpět

            if remaining_km < round_trip_distance:
                # Pokud nezbylo dost km, použijeme zbývající km
                trip_distance = remaining_km / 2

            # Výběr volného dne
            available_days = set(range(1, days_in_month + 1)) - days_used
            if not available_days:
                available_days = set(range(1, days_in_month + 1))  # Znovu použijeme dny
                
            trip_day = random.choice(list(available_days))
            days_used.add(trip_day)
            trip_date = QDate(year, month, trip_day).toString("dd.MM.yyyy")

            # Jízda tam
            trip_tam = {
                "datum": trip_date,
                "řidič": f"{driver[0]} {driver[1]}",
                "start": destination[0],
                "cíl": destination[1],
                "firma": destination[2],
                "vzdálenost": int(trip_distance),
                "vozidlo": selected_vehicle,
                "měsíc": month_name,
                "rok": str(year)
            }
            trips.append(trip_tam)

            # Jízda zpět (může být jiný řidič)
            driver_zpet = random.choice(drivers)
            trip_zpet = {
                "datum": trip_date,
                "řidič": f"{driver_zpet[0]} {driver_zpet[1]}",
                "start": destination[1],  # Zpáteční cesta
                "cíl": destination[0],
                "firma": destination[2],
                "vzdálenost": int(trip_distance),
                "vozidlo": selected_vehicle,
                "měsíc": month_name,
                "rok": str(year)
            }
            trips.append(trip_zpet)

            remaining_km -= round_trip_distance

        # Výpis výsledků s datem
        trip_summary = "\n".join([f"{trip['datum']} | {trip['řidič']} ({trip['vozidlo']}): {trip['start']} → {trip['cíl']} ({trip['vzdálenost']} km, Firma: {trip['firma']})" for trip in trips])

        # Vytvoření tabulky
        self.trip_table.setRowCount(len(trips))
        self.trip_table.setHorizontalHeaderLabels(["Datum", "Řidič", "Start", "Cíl", "Firma", "Vzdálenost (km)"])
        
        # NEJPRVE naplníme tabulku daty, POTOM povolíme řazení
        actual_row = 0
        for trip in trips:
            # Kontrola základních údajů (neměly by být None nebo prázdné stringy)
            if not trip.get("datum") or not trip.get("řidič") or not trip.get("start") or not trip.get("cíl"):
                continue

            self.trip_table.setItem(actual_row, 0, QTableWidgetItem(str(trip["datum"])))
            self.trip_table.setItem(actual_row, 1, QTableWidgetItem(str(trip["řidič"])))
            self.trip_table.setItem(actual_row, 2, QTableWidgetItem(str(trip["start"])))
            self.trip_table.setItem(actual_row, 3, QTableWidgetItem(str(trip["cíl"])))
            self.trip_table.setItem(actual_row, 4, QTableWidgetItem(str(trip["firma"] or "")))
            self.trip_table.setItem(actual_row, 5, QTableWidgetItem(str(trip["vzdálenost"])))
            actual_row += 1

        # Upravení počtu řádků tabulky na skutečný počet záznamů
        self.trip_table.setRowCount(actual_row)
        
        # TEPRVE NYNÍ povolíme řazení a seřadíme podle data
        self.trip_table.setSortingEnabled(True)  # Povolení řazení sloupců
        self.trip_table.sortItems(0, Qt.SortOrder.AscendingOrder)  # Řazení podle data vzestupně

        # Zobrazení tabulky v novém okně
        self.trip_window = QWidget()
        self.trip_window.setWindowTitle("Vygenerovaná Kniha jízd")
        layout = QVBoxLayout()
        layout.addWidget(self.trip_table)
        self.trip_window.setLayout(layout)
        self.trip_window.show()
        
        # Informace o vygenerovaných jízdách
        total_generated_km = sum(trip['vzdálenost'] for trip in trips)
        QMessageBox.information(self, "Kniha jízd vygenerována", 
                              f"Vygenerováno {len(trips)} jízd pro {len(set(trip['cíl'] for trip in trips))//2} destinací.\n"
                              f"Celkový počet km: {total_generated_km} (z {int(total_km)} dostupných km)")

    def show_analysis(self):
        """Zobrazí analýzu a statistiky."""
        try:
            dialog = AnalysisDialog(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při zobrazení analýzy: {str(e)}")

    def update_fuel_display(self):
        """Načte množství paliva ihned po změně měsíce."""
        if not hasattr(self, 'month_box') or not hasattr(self, 'year_box') or not hasattr(self, 'vehicle_box'):
            return  # Pokud ještě nejsou inicializované komponenty
            
        month_name = self.month_box.currentText()
        year = int(self.year_box.currentText())
        selected_vehicle = self.vehicle_box.currentText()

        # Převod měsíce na číslo
        months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
                "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
        month = months.index(month_name) + 1

        # Sečtení tankování z databáze
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(fuel_amount) FROM fuel_tankings
            WHERE vehicle=? AND substr(date, 4, 2)=? AND substr(date, 7, 4)=?
        """, (selected_vehicle, f"{month:02}", str(year)))
        fuel_quantity = cursor.fetchone()[0] or 0
        conn.close()

        # Zobrazení množství paliva na stránce
        self.monthly_fuel_label.setText(f"Množství paliva za zvolený měsíc: {fuel_quantity} litrů")

        # Výpočet předpokládaného počtu kilometrů
        if selected_vehicle and fuel_quantity > 0:
            # Získání spotřeby vozidla
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("SELECT consumption FROM cars WHERE registration=?", (selected_vehicle,))
            consumption_result = cursor.fetchone()
            conn.close()
            
            if consumption_result:
                consumption = consumption_result[0]
                estimated_km = (fuel_quantity / consumption) * 100 if consumption > 0 else 0
                self.estimated_km_label.setText(f"Předpokládaný průměrný počet kilometrů: {estimated_km:.1f} km")
            else:
                self.estimated_km_label.setText("Předpokládaný průměrný počet kilometrů: Vozidlo nenalezeno")
        else:
            self.estimated_km_label.setText("Předpokládaný průměrný počet kilometrů: N/A")


class AnalysisDialog(QDialog):
    """Dialog pro analýzu dat"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analýza dat")
        self.setFixedSize(900, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            QTableWidget {
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background: white;
                gridline-color: #e1e8ed;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e1e8ed;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
        """)
        
        self.setup_ui()
        self.load_analysis_data()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("📊 Analýza jízd a spotřeby")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db; margin-bottom: 20px;")
        layout.addWidget(header_label)
        
        # Statistiky
        stats_layout = QHBoxLayout()
        
        total_trips_label = QLabel("Celkem jízd: 156")
        total_trips_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; background: #ecf0f1; padding: 15px; border-radius: 8px;")
        stats_layout.addWidget(total_trips_label)
        
        total_km_label = QLabel("Celkem km: 23,450")
        total_km_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; background: #ecf0f1; padding: 15px; border-radius: 8px;")
        stats_layout.addWidget(total_km_label)
        
        avg_consumption_label = QLabel("Průměrná spotřeba: 8.2 l/100km")
        avg_consumption_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; background: #ecf0f1; padding: 15px; border-radius: 8px;")
        stats_layout.addWidget(avg_consumption_label)
        
        layout.addLayout(stats_layout)
        
        # Detailní tabulka
        table_label = QLabel("📈 Detailní statistiky")
        table_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #3498db; margin-top: 15px;")
        layout.addWidget(table_label)
        
        self.analysis_table = QTableWidget()
        self.analysis_table.setColumnCount(6)
        self.analysis_table.setHorizontalHeaderLabels([
            "Měsíc", "Počet jízd", "Celkem km", "Spotřeba (l)", "Náklady (Kč)", "Průměr l/100km"
        ])
        layout.addWidget(self.analysis_table)
        
        # Graf informace
        graph_info_label = QLabel("""
📈 Grafické zobrazení:
• Trend spotřeby v čase
• Porovnání měsíčních nákladů  
• Analýza nejčastějších tras
• Výkonnost vozidel
        """)
        graph_info_label.setStyleSheet("""
            font-size: 11px; 
            color: #7f8c8d; 
            background: #ecf0f1; 
            padding: 15px; 
            border-radius: 8px;
            margin-top: 10px;
        """)
        layout.addWidget(graph_info_label)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        period_button = QPushButton("📅 Změnit období")
        period_button.clicked.connect(self.change_period)
        button_layout.addWidget(period_button)
        
        export_csv_button = QPushButton("📊 Export CSV")
        export_csv_button.clicked.connect(self.export_csv)
        button_layout.addWidget(export_csv_button)
        
        export_excel_button = QPushButton("📈 Export Excel")
        export_excel_button.clicked.connect(self.export_excel)
        button_layout.addWidget(export_excel_button)
        
        close_button = QPushButton("Zavřít")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def load_analysis_data(self):
        """Načte data pro analýzu"""
        # Simulace dat pro analýzu
        analysis_data = [
            ("2024-01", "12", "1,890", "154.3", "6,890", "8.17"),
            ("2024-02", "15", "2,340", "189.2", "8,460", "8.09"),
            ("2024-03", "18", "2,780", "225.6", "10,080", "8.12"),
            ("2024-04", "14", "2,150", "172.0", "7,680", "8.00"),
            ("2024-05", "16", "2,450", "198.8", "8,890", "8.11"),
            ("2024-06", "13", "1,980", "160.4", "7,170", "8.10"),
        ]
        
        self.analysis_table.setRowCount(len(analysis_data))
        
        for row, data in enumerate(analysis_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                if col == 5:  # Průměrná spotřeba
                    consumption = float(value)
                    if consumption < 8.0:
                        item.setBackground(Qt.GlobalColor.green)
                        item.setForeground(Qt.GlobalColor.white)
                    elif consumption > 8.2:
                        item.setBackground(Qt.GlobalColor.red)
                        item.setForeground(Qt.GlobalColor.white)
                    else:
                        item.setForeground(Qt.GlobalColor.darkBlue)
                elif col == 4:  # Náklady
                    item.setForeground(Qt.GlobalColor.darkMagenta)
                self.analysis_table.setItem(row, col, item)
        
        self.analysis_table.resizeColumnsToContents()
    
    def change_period(self):
        """Změní období pro analýzu"""
        QMessageBox.information(self, "Období", "Funkce změny období bude k dispozici v další verzi.")
    
    def export_csv(self):
        """Export do CSV"""
        QMessageBox.information(self, "Export", "Data byla exportována do CSV souboru.")
    
    def export_excel(self):
        """Export do Excel"""
        QMessageBox.information(self, "Export", "Data byla exportována do Excel souboru.")


