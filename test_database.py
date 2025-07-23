#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from database import connect

def test_database_data():
    """Test načítání dat z databáze"""
    print("=== Test dat v databázi ===")
    
    conn = connect()
    if not conn:
        print("❌ Nepodařilo se připojit k databázi!")
        return
    
    cursor = conn.cursor()
    
    # Test řidičů
    cursor.execute("SELECT first_name, last_name FROM drivers")
    drivers = cursor.fetchall()
    print(f"Řidiči v databázi ({len(drivers)}):")
    for i, driver in enumerate(drivers, 1):
        print(f"  {i}. {driver[0]} {driver[1]}")
    
    # Test destinací 
    cursor.execute("SELECT start, destination, company, distance FROM destinations")
    destinations = cursor.fetchall()
    print(f"\nDestinace v databázi ({len(destinations)}):")
    for i, dest in enumerate(destinations, 1):
        print(f"  {i}. {dest[0]} → {dest[1]} ({dest[3]} km, Firma: {dest[2]})")
    
    # Test vozidel
    cursor.execute("SELECT registration, consumption FROM cars")
    cars = cursor.fetchall()
    print(f"\nVozidla v databázi ({len(cars)}):")
    for i, car in enumerate(cars, 1):
        print(f"  {i}. {car[0]} (spotřeba: {car[1]} l/100km)")
    
    # Test tankování
    cursor.execute("SELECT vehicle, date, fuel_amount FROM fuel_tankings LIMIT 5")
    tankings = cursor.fetchall()
    print(f"\nPoslední tankování ({len(tankings)}):")
    for i, tank in enumerate(tankings, 1):
        print(f"  {i}. {tank[0]} - {tank[1]} - {tank[2]} l")
    
    conn.close()
    
    if not drivers:
        print("\n❌ PROBLÉM: V databázi nejsou žádní řidiči!")
    if not destinations:
        print("\n❌ PROBLÉM: V databázi nejsou žádné destinace!")
    if not cars:
        print("\n❌ PROBLÉM: V databázi nejsou žádná vozidla!")
        
    print("\n=== Konec testu ===")

if __name__ == "__main__":
    test_database_data()
