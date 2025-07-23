#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtCore import QDate
import random
from database import connect

def debug_trip_data_only():
    """Debug pouze dat bez GUI"""
    print("=== DEBUG POUZE DATA ===")
    
    # Parametry
    month_name = "Červenec"
    year = 2025
    selected_vehicle = "7AF3233"
    
    months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
              "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
    month = months.index(month_name) + 1
    
    print(f"Testujeme: {month_name} {year}, vozidlo: {selected_vehicle}")
    
    # Načítání dat z databáze
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(fuel_amount) FROM fuel_tankings
        WHERE vehicle=? AND substr(date, 4, 2)=? AND substr(date, 7, 4)=?
    """, (selected_vehicle, f"{month:02}", str(year)))

    fuel_quantity = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT consumption FROM cars WHERE registration=?", (selected_vehicle,))
    consumption_result = cursor.fetchone()
    consumption = consumption_result[0] if consumption_result else 0
    
    cursor.execute("SELECT start, destination, company, distance FROM destinations")
    destinations = cursor.fetchall()

    cursor.execute("SELECT first_name, last_name FROM drivers")
    drivers = cursor.fetchall()
    
    conn.close()

    print(f"Palivo: {fuel_quantity} l, Spotřeba: {consumption} l/100km")
    print(f"Řidiči: {len(drivers)}, Destinace: {len(destinations)}")

    # Výpočet km
    total_km = (fuel_quantity / consumption) * 100 if consumption > 0 else 0
    print(f"Celkové km: {total_km}")

    trips = []
    remaining_km = total_km
    days_used = set()
    days_in_month = QDate(year, month, 1).daysInMonth()

    # Generování jízd
    for i, destination in enumerate(destinations):
        if remaining_km <= 0 or len(days_used) >= days_in_month:
            print(f"Ukončuji na destinaci {i+1} - zbývá {remaining_km} km")
            break
            
        driver = random.choice(drivers)
        trip_distance = destination[3]
        round_trip_distance = trip_distance * 2

        if remaining_km < round_trip_distance:
            trip_distance = remaining_km / 2

        available_days = set(range(1, days_in_month + 1)) - days_used
        if not available_days:
            available_days = set(range(1, days_in_month + 1))
            
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
        }
        trips.append(trip_tam)
        print(f"TAM {len(trips)}: {trip_date} | {driver[0]} {driver[1]} | {destination[0]} → {destination[1]} | {int(trip_distance)} km")

        # Jízda zpět
        driver_zpet = random.choice(drivers)
        trip_zpet = {
            "datum": trip_date,
            "řidič": f"{driver_zpet[0]} {driver_zpet[1]}",
            "start": destination[1],
            "cíl": destination[0],
            "firma": destination[2],
            "vzdálenost": int(trip_distance),
        }
        trips.append(trip_zpet)
        print(f"ZPĚT {len(trips)}: {trip_date} | {driver_zpet[0]} {driver_zpet[1]} | {destination[1]} → {destination[0]} | {int(trip_distance)} km")

        remaining_km -= round_trip_distance

    print(f"\n=== VÝSLEDEK ===")
    print(f"Vygenerováno celkem {len(trips)} jízd")
    
    # Kontrola prázdných polí
    problem_count = 0
    for i, trip in enumerate(trips, 1):
        issues = []
        if not trip.get("datum"): issues.append("datum")
        if not trip.get("řidič"): issues.append("řidič") 
        if not trip.get("start"): issues.append("start")
        if not trip.get("cíl"): issues.append("cíl")
        
        if issues:
            problem_count += 1
            print(f"❌ PROBLÉM jízda {i}: chybí {', '.join(issues)}")
        else:
            print(f"✅ OK jízda {i}: {trip['datum']} | {trip['řidič']} | {trip['start']} → {trip['cíl']}")
    
    print(f"\nProblematické záznamy: {problem_count}")
    print("================")

if __name__ == "__main__":
    debug_trip_data_only()
