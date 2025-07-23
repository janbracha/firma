#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDate
import random
from database import connect

def test_trip_generation():
    """Test generování jízd bez GUI"""
    print("=== Test generování jízd ===")
    
    # Simulace parametrů jako v GUI
    month_name = "Červenec"
    year = 2025
    selected_vehicle = "7AF3233"
    
    # Převod měsíce na číslo
    months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
              "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
    month = months.index(month_name) + 1
    
    print(f"Testujeme pro: {month_name} {year}, vozidlo: {selected_vehicle}")
    
    # Načítání dat jako v původním kódu
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(fuel_amount) FROM fuel_tankings
        WHERE vehicle=? AND substr(date, 4, 2)=? AND substr(date, 7, 4)=?
    """, (selected_vehicle, f"{month:02}", str(year)))

    fuel_quantity = cursor.fetchone()[0] or 0
    print(f"Palivo pro {month_name}: {fuel_quantity} litrů")

    # Získání spotřeby vozidla
    cursor.execute("SELECT consumption FROM cars WHERE registration=?", (selected_vehicle,))
    consumption_result = cursor.fetchone()
    consumption = consumption_result[0] if consumption_result else 0
    print(f"Spotřeba vozidla: {consumption} l/100km")
    
    # Načtení destinací a řidičů z databáze
    cursor.execute("SELECT start, destination, company, distance FROM destinations")
    destinations = cursor.fetchall()

    cursor.execute("SELECT first_name, last_name FROM drivers")
    drivers = cursor.fetchall()
    
    conn.close()

    print(f"Načteno {len(drivers)} řidičů: {drivers}")
    print(f"Načteno {len(destinations)} destinací")
    for i, dest in enumerate(destinations, 1):
        print(f"  {i}. {dest[0]} → {dest[1]} ({dest[3]} km)")

    # Výpočet celkového počtu km z paliva
    total_km = (fuel_quantity / consumption) * 100 if consumption > 0 else 0
    print(f"Celkové km z paliva: {total_km}")

    if total_km <= 0:
        print("❌ Není dostatek paliva pro generování jízd!")
        return

    trips = []
    remaining_km = total_km
    days_used = set()
    days_in_month = QDate(year, month, 1).daysInMonth()
    
    print(f"Dní v měsíci: {days_in_month}")

    # Generování jízd - každá destinace tam a zpět
    for i, destination in enumerate(destinations):
        if remaining_km <= 0 or len(days_used) >= days_in_month:
            print(f"Ukončuji generování - zbývá km: {remaining_km}, použité dny: {len(days_used)}")
            break
            
        print(f"\n--- Generuji pro destinaci {i+1}: {destination[0]} → {destination[1]} ---")
        
        driver = random.choice(drivers)
        trip_distance = destination[3]  # Vzdálenost jedné cesty
        round_trip_distance = trip_distance * 2  # Celková vzdálenost tam i zpět

        if remaining_km < round_trip_distance:
            # Pokud nezbylo dost km, použijeme zbývající km
            trip_distance = remaining_km / 2
            print(f"Upravuji vzdálenost na {trip_distance} km (zbývá {remaining_km} km)")

        # Výběr volného dne
        available_days = set(range(1, days_in_month + 1)) - days_used
        if not available_days:
            available_days = set(range(1, days_in_month + 1))  # Znovu použijeme dny
            print("Znovu používám dny (všechny dny už byly použité)")
            
        trip_day = random.choice(list(available_days))
        days_used.add(trip_day)
        trip_date = QDate(year, month, trip_day).toString("dd.MM.yyyy")
        
        print(f"Datum: {trip_date}, Řidič: {driver[0]} {driver[1]}")

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
        print(f"Přidána jízda tam: {trip_tam}")

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
        print(f"Přidána jízda zpět: {trip_zpet}")

        remaining_km -= round_trip_distance
        print(f"Zbývá km: {remaining_km}")

    print(f"\n=== VÝSLEDEK ===")
    print(f"Vygenerováno celkem {len(trips)} jízd")
    
    # Kontrola prázdných polí
    empty_count = 0
    for i, trip in enumerate(trips, 1):
        print(f"\nJízda {i}:")
        print(f"  Datum: '{trip['datum']}'")
        print(f"  Řidič: '{trip['řidič']}'") 
        print(f"  Start: '{trip['start']}'")
        print(f"  Cíl: '{trip['cíl']}'")
        print(f"  Firma: '{trip['firma']}'")
        print(f"  Vzdálenost: {trip['vzdálenost']}")
        
        # Kontrola prázdných hodnot
        if not trip.get("datum") or not trip.get("řidič") or not trip.get("start") or not trip.get("cíl"):
            empty_count += 1
            print(f"  ❌ PRÁZDNÁ POLE!")
    
    print(f"\nCelkem prázdných záznamů: {empty_count}")
    print("=== Konec testu ===")

if __name__ == "__main__":
    test_trip_generation()
