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

    # Tabulka pro uživatele a role
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL DEFAULT 'user',  -- admin, accountant, user
            active INTEGER DEFAULT 1,  -- 1 = aktivní, 0 = neaktivní
            created_date TEXT NOT NULL,
            last_login TEXT
        )
    """)

    # Tabulka pro role
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL,
            description TEXT,
            is_system INTEGER DEFAULT 0,  -- 1 = systémová role (nelze smazat), 0 = uživatelská
            created_date TEXT NOT NULL,
            modified_date TEXT NOT NULL
        )
    """)

    # Tabulka pro oprávnění
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL,
            description TEXT,
            module TEXT NOT NULL,  -- např. 'users', 'invoices', 'accounting'
            created_date TEXT NOT NULL
        )
    """)

    # Tabulka pro propojení rolí a oprávnění
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS role_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER NOT NULL,
            permission_id INTEGER NOT NULL,
            granted_date TEXT NOT NULL,
            granted_by INTEGER,  -- ID uživatele, který oprávnění udělil
            FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE,
            FOREIGN KEY (permission_id) REFERENCES permissions (id) ON DELETE CASCADE,
            FOREIGN KEY (granted_by) REFERENCES users (id),
            UNIQUE(role_id, permission_id)
        )
    """)

    # Tabulka pro dokumenty
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            file_type TEXT NOT NULL,  -- pdf, png, jpg, jpeg
            mime_type TEXT NOT NULL,
            related_table TEXT,  -- 'invoices', 'companies', 'trips', etc.
            related_id INTEGER,  -- ID záznamu v související tabulce
            description TEXT,
            uploaded_by INTEGER NOT NULL,
            upload_date TEXT NOT NULL,
            FOREIGN KEY (uploaded_by) REFERENCES users (id)
        )
    """)

    # Tabulka pro nastavení firmy
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            address TEXT,
            city TEXT,
            postal_code TEXT,
            country TEXT,
            phone TEXT,
            email TEXT,
            website TEXT,
            ico TEXT,
            dic TEXT,
            logo_path TEXT,
            invoice_template TEXT,
            invoice_footer TEXT,
            default_currency TEXT DEFAULT 'CZK',
            tax_rate INTEGER DEFAULT 21,
            created_date TEXT NOT NULL,
            modified_date TEXT NOT NULL
        )
    """)

    # Vytvoření výchozího admin uživatele (heslo: admin123)
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password_hash, full_name, role, created_date)
        VALUES ('admin', 'admin123', 'Administrátor', 'admin', datetime('now'))
    """)
    
    # Vytvoření testovacího neaktivního uživatele pro demonstraci barev
    cursor.execute("""
        DELETE FROM users WHERE username = 'test_inactive'
    """)
    cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, role, active, created_date)
        VALUES ('test_inactive', 'test123', 'Test Neaktivní', 'user', 0, datetime('now'))
    """)

    # Vytvoření základních rolí
    cursor.execute("""
        INSERT OR IGNORE INTO roles (name, display_name, description, is_system, created_date, modified_date)
        VALUES 
        ('admin', 'Administrátor', 'Plný přístup ke všem funkcím systému', 1, datetime('now'), datetime('now')),
        ('accountant', 'Účetní', 'Přístup k účetním funkcím a fakturaci', 1, datetime('now'), datetime('now')),
        ('user', 'Uživatel', 'Základní přístup k systému', 1, datetime('now'), datetime('now'))
    """)

    # Vytvoření základních oprávnění
    cursor.execute("""
        INSERT OR IGNORE INTO permissions (name, display_name, description, module, created_date)
        VALUES 
        -- Správa uživatelů
        ('users.view', 'Zobrazit uživatele', 'Zobrazení seznamu uživatelů', 'users', datetime('now')),
        ('users.create', 'Vytvořit uživatele', 'Vytváření nových uživatelů', 'users', datetime('now')),
        ('users.edit', 'Upravit uživatele', 'Úprava existujících uživatelů', 'users', datetime('now')),
        ('users.delete', 'Smazat uživatele', 'Deaktivace a trvalé mazání uživatelů', 'users', datetime('now')),
        ('users.change_password', 'Změnit heslo', 'Změna hesel uživatelů', 'users', datetime('now')),
        
        -- Správa rolí
        ('roles.view', 'Zobrazit role', 'Zobrazení seznamu rolí a oprávnění', 'roles', datetime('now')),
        ('roles.create', 'Vytvořit role', 'Vytváření nových rolí', 'roles', datetime('now')),
        ('roles.edit', 'Upravit role', 'Úprava rolí a jejich oprávnění', 'roles', datetime('now')),
        ('roles.delete', 'Smazat role', 'Mazání uživatelských rolí', 'roles', datetime('now')),
        
        -- Fakturace
        ('invoices.view', 'Zobrazit faktury', 'Zobrazení seznamu faktur', 'invoices', datetime('now')),
        ('invoices.create', 'Vytvořit faktury', 'Vytváření nových faktur', 'invoices', datetime('now')),
        ('invoices.edit', 'Upravit faktury', 'Úprava existujících faktur', 'invoices', datetime('now')),
        ('invoices.delete', 'Smazat faktury', 'Mazání faktur', 'invoices', datetime('now')),
        
        -- Účetnictví
        ('accounting.view', 'Zobrazit účetnictví', 'Přístup k účetním přehledům', 'accounting', datetime('now')),
        ('accounting.cash_journal', 'Pokladní deník', 'Správa pokladního deníku', 'accounting', datetime('now')),
        
        -- Správa firmy
        ('company.view', 'Zobrazit nastavení', 'Zobrazení nastavení firmy', 'company', datetime('now')),
        ('company.edit', 'Upravit nastavení', 'Úprava nastavení firmy', 'company', datetime('now'))
    """)

    # Přiřazení oprávnění rolím
    cursor.execute("""
        INSERT OR IGNORE INTO role_permissions (role_id, permission_id, granted_date)
        SELECT r.id, p.id, datetime('now')
        FROM roles r, permissions p
        WHERE r.name = 'admin'  -- Admin má všechna oprávnění
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO role_permissions (role_id, permission_id, granted_date)
        SELECT r.id, p.id, datetime('now')
        FROM roles r, permissions p
        WHERE r.name = 'accountant' 
        AND p.name IN (
            'invoices.view', 'invoices.create', 'invoices.edit', 'invoices.delete',
            'accounting.view', 'accounting.cash_journal',
            'company.view'
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO role_permissions (role_id, permission_id, granted_date)
        SELECT r.id, p.id, datetime('now')
        FROM roles r, permissions p
        WHERE r.name = 'user'
        AND p.name IN (
            'invoices.view',
            'accounting.view',
            'company.view'
        )
    """)

    # Vytvoření výchozího nastavení firmy
    cursor.execute("""
        INSERT OR IGNORE INTO company_settings (
            company_name, address, city, postal_code, country, phone, email, website,
            ico, dic, invoice_template, invoice_footer, default_currency, tax_rate,
            created_date, modified_date
        ) VALUES (
            'Projekt & Develop s.r.o.', 
            'Václavské náměstí 1', 
            'Praha 1', 
            '11000', 
            'Česká republika',
            '+420 123 456 789', 
            'info@projektdevelop.cz', 
            'www.projektdevelop.cz',
            '12345678', 
            'CZ12345678',
            'Standardní faktura',
            'Děkujeme za využití našich služeb.\nPlatba na účet: 123456789/0100',
            'CZK',
            21,
            datetime('now'), 
            datetime('now')
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
