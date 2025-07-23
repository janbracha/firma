#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import QDate, Qt
import random
from database import connect

def test_real_trip_generation():
    """Test reálného generování jízd s GUI - přesná kopie logiky z aplikace"""
    
    app = QApplication(sys.argv)
    
    # Vytvoření okna
    window = QMainWindow()
    window.setWindowTitle("Test reálného generování knihy jízd")
    window.setGeometry(200, 200, 1200, 700)
    
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout()
    central_widget.setLayout(layout)
    
    # === PŘESNÁ KOPIE LOGIKY Z trip_calculation.py ===
    
    # Simulace parametrů
    month_name = "Červenec"
    year = 2025
    selected_vehicle = "7AF3233"
    
    # Převod měsíce na číslo
    months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
              "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
    month = months.index(month_name) + 1
    
    print(f"=== GENEROVÁNÍ KNIHY JÍZD ===")
    print(f"Měsíc: {month_name} {year}, Vozidlo: {selected_vehicle}")
    
    # Načítání dat z databáze
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(fuel_amount) FROM fuel_tankings
        WHERE vehicle=? AND substr(date, 4, 2)=? AND substr(date, 7, 4)=?
    """, (selected_vehicle, f"{month:02}", str(year)))

    fuel_quantity = cursor.fetchone()[0] or 0
    print(f"Palivo: {fuel_quantity} litrů")

    # Získání spotřeby vozidla
    cursor.execute("SELECT consumption FROM cars WHERE registration=?", (selected_vehicle,))
    consumption_result = cursor.fetchone()
    consumption = consumption_result[0] if consumption_result else 0
    print(f"Spotřeba: {consumption} l/100km")
    
    # Načtení destinací a řidičů z databáze
    cursor.execute("SELECT start, destination, company, distance FROM destinations")
    destinations = cursor.fetchall()

    cursor.execute("SELECT first_name, last_name FROM drivers")
    drivers = cursor.fetchall()
    
    conn.close()

    print(f"Řidiči: {len(drivers)}, Destinace: {len(destinations)}")

    if not drivers or not destinations:
        print("Chybí data v databázi!")
        return

    # Výpočet celkového počtu km z paliva
    total_km = (fuel_quantity / consumption) * 100 if consumption > 0 else 0
    print(f"Celkové km: {total_km}")

    if total_km <= 0:
        print("Není dostatek paliva!")
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

    print(f"Vygenerováno {len(trips)} jízd")
    
    # === VYTVOŘENÍ TABULKY STEJNĚ JAKO V APLIKACI ===
    
    trip_table = QTableWidget()
    trip_table.setColumnCount(6)
    trip_table.setHorizontalHeaderLabels(["Datum", "Řidič", "Start", "Cíl", "Firma", "Vzdálenost (km)"])
    
    # Vytvoření tabulky
    trip_table.setRowCount(len(trips))
    print(f"Nastaveno {len(trips)} řádků")
    
    # NEJPRVE naplníme tabulku daty, POTOM povolíme řazení
    actual_row = 0
    for i, trip in enumerate(trips):
        print(f"Zpracovávám záznam {i+1}: {trip['datum']} - {trip['řidič']}")
        
        # Kontrola základních údajů (neměly by být None nebo prázdné stringy)
        if not trip.get("datum") or not trip.get("řidič") or not trip.get("start") or not trip.get("cíl"):
            print(f"  -> Přeskakuji prázdný záznam")
            continue

        print(f"  -> Vkládám do řádku {actual_row}")
        trip_table.setItem(actual_row, 0, QTableWidgetItem(str(trip["datum"])))
        trip_table.setItem(actual_row, 1, QTableWidgetItem(str(trip["řidič"])))
        trip_table.setItem(actual_row, 2, QTableWidgetItem(str(trip["start"])))
        trip_table.setItem(actual_row, 3, QTableWidgetItem(str(trip["cíl"])))
        trip_table.setItem(actual_row, 4, QTableWidgetItem(str(trip["firma"] or "")))
        trip_table.setItem(actual_row, 5, QTableWidgetItem(str(trip["vzdálenost"])))
        actual_row += 1

    # Upravení počtu řádků tabulky na skutečný počet záznamů
    trip_table.setRowCount(actual_row)
    print(f"Upraveno na {actual_row} řádků")
    
    # TEPRVE NYNÍ povolíme řazení a seřadíme podle data
    trip_table.setSortingEnabled(True)  # Povolení řazení sloupců
    trip_table.sortItems(0, Qt.SortOrder.AscendingOrder)  # Řazení podle data vzestupně
    print("Tabulka seřazena")
    
    layout.addWidget(trip_table)
    
    # Tlačítko pro kontrolu obsahu tabulky
    def check_table_content():
        print("\n=== FINÁLNÍ KONTROLA TABULKY ===")
        print(f"Počet řádků: {trip_table.rowCount()}")
        
        empty_rows = 0
        filled_rows = 0
        for row in range(trip_table.rowCount()):
            item_0 = trip_table.item(row, 0)  # Datum
            item_1 = trip_table.item(row, 1)  # Řidič
            item_2 = trip_table.item(row, 2)  # Start
            item_3 = trip_table.item(row, 3)  # Cíl
            
            if item_0 and item_0.text() and item_1 and item_1.text() and item_2 and item_2.text() and item_3 and item_3.text():
                filled_rows += 1
                print(f"Řádek {row}: {item_0.text()} | {item_1.text()} | {item_2.text()} → {item_3.text()}")
            else:
                empty_rows += 1
                print(f"Řádek {row}: PRÁZDNÝ!")
        
        print(f"\nVyplněné řádky: {filled_rows}")
        print(f"Prázdné řádky: {empty_rows}")
        print("===============================\n")
    
    check_button = QPushButton("Zkontroluj konečný stav tabulky")
    check_button.clicked.connect(check_table_content)
    layout.addWidget(check_button)
    
    # Okamžitá kontrola
    check_table_content()
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    test_real_trip_generation()
