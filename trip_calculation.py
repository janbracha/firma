from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QFormLayout, QLabel, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QDate, Qt
from database import connect
import random
from fuel_management import FuelManagementWindow  # Import správy tankování



class TripCalculationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Výpočet Knihy jízd")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Použití stejného stylu jako v hlavní aplikaci
        self.setStyleSheet("""
            * {
                font-family: 'Inter', 'Roboto', sans-serif;
                color: #2C3E50;
            }

            QWidget {
                background: #F2F2F2;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }

            QPushButton {
                background-color: #6C85A3;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 18px;
                border: none;
            }

            QPushButton:hover {
                background-color: #5A7393;
            }

            QLabel {
                background: transparent;
                border: none;
                color: #2C3E50;
                font-size: 14px;
            }

            QComboBox {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px;
                color: #2C3E50;
            }

            QComboBox:focus {
                border-color: #6C85A3;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #E0E0E0;
            }

            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }

            QTableWidget::item:selected {
                background-color: #6C85A3;
                color: white;
            }

            QHeaderView::section {
                background-color: #6C85A3;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)

        # Formulář pro zadání vstupních údajů
        form_layout = QFormLayout()


        # Výběr měsíce
        self.month_box = QComboBox()
        self.month_box.addItems(["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
                                 "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"])
        form_layout.addRow(QLabel("Měsíc:"), self.month_box)
        self.month_box.currentIndexChanged.connect(self.update_fuel_display)

        # Výběr roku
        self.year_box = QComboBox()
        current_year = QDate.currentDate().year()
        self.year_box.addItems([str(y) for y in range(current_year, current_year - 10, -1)])
        self.year_box.currentIndexChanged.connect(self.update_fuel_display)
        form_layout.addRow(QLabel("Rok:"), self.year_box)

        # Množství paliva za měsíc - s výrazným stylem ale v souladu s hlavním tématem
        self.monthly_fuel_label = QLabel("Množství paliva za zvolený měsíc: N/A")
        self.monthly_fuel_label.setStyleSheet("""
            QLabel {
                background-color: #E3F2FD;
                padding: 12px;
                border: 2px solid #6C85A3;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                color: #2C3E50;
            }
        """)
        form_layout.addRow(QLabel(""), self.monthly_fuel_label)

        # Předpokládaný počet kilometrů - v souladu s hlavním tématem
        self.estimated_km_label = QLabel("Předpokládaný průměrný počet kilometrů: N/A")
        self.estimated_km_label.setStyleSheet("""
            QLabel {
                background-color: #F3E5F5;
                padding: 12px;
                border: 2px solid #6C85A3;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                color: #2C3E50;
            }
        """)
        form_layout.addRow(QLabel(""), self.estimated_km_label)

        # Výběr vozidla
        self.vehicle_box = QComboBox()
        self.load_vehicles()
        self.vehicle_box.currentIndexChanged.connect(self.update_fuel_display)
        form_layout.addRow(QLabel("Vozidlo:"), self.vehicle_box)

        layout.addLayout(form_layout)

        # Tlačítka
        self.generate_button = QPushButton("Generovat Knihu jízd")
        self.generate_button.clicked.connect(self.generate_trip_book)
        layout.addWidget(self.generate_button)

        self.manage_fuel_button = QPushButton("Správa tankování")
        self.manage_fuel_button.clicked.connect(self.show_fuel_management)
        layout.addWidget(self.manage_fuel_button)

        central_widget.setLayout(layout)

        # Počáteční načtení dat
        self.update_fuel_display()

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

    def show_fuel_management(self):
        """Otevře okno pro správu tankování."""
        self.fuel_management_window = FuelManagementWindow()
        self.fuel_management_window.show()

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


