import sqlite3
import os

# Nastavení absolutní cesty k databázi ve stejné složce jako `database.py`
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "invoices.db")

def connect():
    """Připojení k databázi ve správném adresáři."""
    return sqlite3.connect(DB_PATH)

def create_tables():
    """Vytvoření tabulek v databázi."""

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE,
            type TEXT,
            recipient TEXT,
            issuer TEXT,
            issue_date TEXT,
            tax_date TEXT,
            due_date TEXT,
            amount_no_tax REAL,
            tax REAL,
            total REAL,
            status TEXT,
            note TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            ico TEXT NOT NULL,
            dic TEXT NOT NULL,
            bank TEXT NOT NULL,
            contact TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cash_journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,  -- Příjem / Výdaj
            date TEXT NOT NULL,  -- Datum transakce
            person TEXT NOT NULL,  -- Jméno osoby
            amount REAL NOT NULL,  -- Částka
            note TEXT,  -- Poznámka k transakci
            balance REAL NOT NULL  -- Aktuální zůstatek po transakci
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            role TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration TEXT NOT NULL,
            type TEXT UNIQUE NOT NULL,
            owner TEXT NOT NULL,
            consumption REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start TEXT NOT NULL,
            destination TEXT NOT NULL,
            company TEXT NOT NULL,
            distance REAL NOT NULL,
            note TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuel_tankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            vehicle TEXT NOT NULL,
            fuel_amount REAL NOT NULL
        )
    """)



    conn.commit()
    conn.close()
 
def fetch_all_invoices():
    """Načte všechny faktury z databáze."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, invoice_number, type, recipient, issuer, issue_date, tax_date, due_date, 
               amount_no_tax, tax, total, status, note 
        FROM invoices
    """)
    data = cursor.fetchall()
    conn.close()
    return data
