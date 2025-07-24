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
        ('accounting.analytics', 'Analýzy a reporty', 'Finanční analýzy a výkazy', 'accounting', datetime('now')),
        
        -- Správa firmy
        ('company.view', 'Zobrazit nastavení', 'Zobrazení nastavení firmy', 'company', datetime('now')),
        ('company.edit', 'Upravit nastavení', 'Úprava nastavení firmy', 'company', datetime('now')),
        ('company.manage', 'Správa firem', 'Správa firemních kontaktů a partnerů', 'company', datetime('now')),
        
        -- Dokumenty
        ('documents.view', 'Zobrazit dokumenty', 'Zobrazení seznamu dokumentů', 'documents', datetime('now')),
        ('documents.create', 'Nahrát dokumenty', 'Nahrávání nových dokumentů', 'documents', datetime('now')),
        ('documents.edit', 'Upravit dokumenty', 'Úprava a přejmenování dokumentů', 'documents', datetime('now')),
        ('documents.delete', 'Smazat dokumenty', 'Mazání dokumentů', 'documents', datetime('now')),
        
        -- Majetek
        ('assets.view', 'Zobrazit majetek', 'Zobrazení hmotného majetku', 'assets', datetime('now')),
        ('assets.create', 'Přidat majetek', 'Přidávání nového majetku', 'assets', datetime('now')),
        ('assets.edit', 'Upravit majetek', 'Úprava údajů o majetku', 'assets', datetime('now')),
        ('assets.delete', 'Smazat majetek', 'Vyřazení majetku', 'assets', datetime('now')),
        
        -- Doprava
        ('transport.view', 'Zobrazit dopravu', 'Zobrazení knihy jízd', 'transport', datetime('now')),
        ('transport.create', 'Zadat jízdu', 'Zadávání nových jízd', 'transport', datetime('now')),
        ('transport.edit', 'Upravit jízdu', 'Úprava záznamů o jízdách', 'transport', datetime('now')),
        ('transport.delete', 'Smazat jízdu', 'Mazání záznamů o jízdách', 'transport', datetime('now')),
        ('transport.manage_drivers', 'Správa řidičů', 'Správa řidičů a vozidel', 'transport', datetime('now')),
        ('transport.manage_vehicles', 'Správa vozidel', 'Správa vozového parku', 'transport', datetime('now')),
        ('transport.manage_destinations', 'Správa destinací', 'Správa tras a destinací', 'transport', datetime('now')),
        ('transport.fuel_management', 'Správa pohonných hmot', 'Evidence tankování', 'transport', datetime('now')),
        
        -- Kalendář
        ('calendar.view', 'Zobrazit kalendář', 'Zobrazení kalendáře a termínů', 'calendar', datetime('now')),
        ('calendar.create', 'Vytvořit událost', 'Vytváření nových událostí', 'calendar', datetime('now')),
        ('calendar.edit', 'Upravit událost', 'Úprava kalendářních událostí', 'calendar', datetime('now')),
        ('calendar.delete', 'Smazat událost', 'Mazání událostí', 'calendar', datetime('now')),
        
        -- Sklad
        ('warehouse.view', 'Zobrazit sklad', 'Zobrazení skladových zásob', 'warehouse', datetime('now')),
        ('warehouse.create', 'Přidat zboží', 'Přidávání nového zboží', 'warehouse', datetime('now')),
        ('warehouse.edit', 'Upravit zboží', 'Úprava skladových položek', 'warehouse', datetime('now')),
        ('warehouse.delete', 'Smazat zboží', 'Mazání skladových položek', 'warehouse', datetime('now')),
        ('warehouse.inventory', 'Inventura', 'Provádění inventur', 'warehouse', datetime('now')),
        
        -- Zaměstnanci
        ('employees.view', 'Zobrazit zaměstnance', 'Zobrazení seznamu zaměstnanců', 'employees', datetime('now')),
        ('employees.create', 'Přidat zaměstnance', 'Přijímání nových zaměstnanců', 'employees', datetime('now')),
        ('employees.edit', 'Upravit zaměstnance', 'Úprava údajů zaměstnanců', 'employees', datetime('now')),
        ('employees.delete', 'Smazat zaměstnance', 'Ukončení pracovního poměru', 'employees', datetime('now')),
        ('employees.contracts', 'Správa smluv', 'Správa pracovních smluv', 'employees', datetime('now')),
        ('employees.training', 'Správa školení', 'Plánování a evidence školení', 'employees', datetime('now')),
        ('employees.payroll', 'Mzdová agenda', 'Správa mezd a odměn', 'employees', datetime('now')),
        
        -- Servis a údržba
        ('maintenance.view', 'Zobrazit servis', 'Zobrazení plánů servisu', 'maintenance', datetime('now')),
        ('maintenance.create', 'Naplánovat servis', 'Plánování nových servisů', 'maintenance', datetime('now')),
        ('maintenance.edit', 'Upravit servis', 'Úprava servisních plánů', 'maintenance', datetime('now')),
        ('maintenance.delete', 'Smazat servis', 'Zrušení servisních plánů', 'maintenance', datetime('now')),
        ('maintenance.costs', 'Náklady servisu', 'Správa nákladů na servis', 'maintenance', datetime('now')),
        ('maintenance.certificates', 'Certifikáty', 'Správa certifikátů a kontrol', 'maintenance', datetime('now'))
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
            'accounting.view', 'accounting.cash_journal', 'accounting.analytics',
            'company.view', 'company.manage',
            'documents.view', 'documents.create', 'documents.edit', 'documents.delete',
            'assets.view', 'assets.create', 'assets.edit', 'assets.delete',
            'transport.view', 'transport.create', 'transport.edit', 'transport.delete',
            'transport.manage_drivers', 'transport.manage_vehicles', 'transport.manage_destinations', 'transport.fuel_management',
            'calendar.view', 'calendar.create', 'calendar.edit', 'calendar.delete',
            'warehouse.view', 'warehouse.create', 'warehouse.edit', 'warehouse.delete', 'warehouse.inventory',
            'employees.view', 'employees.create', 'employees.edit', 'employees.contracts', 'employees.training', 'employees.payroll',
            'maintenance.view', 'maintenance.create', 'maintenance.edit', 'maintenance.costs', 'maintenance.certificates'
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO role_permissions (role_id, permission_id, granted_date)
        SELECT r.id, p.id, datetime('now')
        FROM roles r, permissions p
        WHERE r.name = 'user'
        AND p.name IN (
            'invoices.view',
            'accounting.view', 'accounting.analytics',
            'company.view',
            'documents.view', 'documents.create',
            'assets.view',
            'transport.view',
            'calendar.view', 'calendar.create', 'calendar.edit',
            'warehouse.view',
            'employees.view',
            'maintenance.view'
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

    # Tabulka pro hmotný majetek
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            purchase_price REAL,
            purchase_date TEXT,
            depreciation_method TEXT,
            useful_life INTEGER,
            total_depreciation REAL DEFAULT 0,
            book_value REAL,
            status TEXT DEFAULT 'Aktivní',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabulka pro kalendář a termíny
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            event_type TEXT,
            event_date TEXT,
            event_time TEXT,
            end_date TEXT,
            end_time TEXT,
            status TEXT DEFAULT 'Plánováno',
            reminder_minutes INTEGER DEFAULT 15,
            reminder_sent BOOLEAN DEFAULT 0,
            recurring BOOLEAN DEFAULT 0,
            recurring_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabulka produktů ve skladu
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
    
    # Tabulka zaměstnanců
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            position TEXT,
            department TEXT,
            hire_date TEXT,
            birth_date TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            salary REAL,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabulka mezd
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_salaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            month TEXT,
            base_salary REAL,
            overtime REAL,
            bonus REAL,
            deductions REAL,
            net_salary REAL,
            paid_date TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    """)
    
    # Tabulka docházky
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            date TEXT,
            start_time TEXT,
            end_time TEXT,
            break_time INTEGER DEFAULT 0,
            overtime INTEGER DEFAULT 0,
            absence_type TEXT,
            notes TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    """)
    
    # Tabulka servisních záznamů
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            asset_type TEXT,
            asset_id INTEGER,
            asset_name TEXT,
            service_type TEXT,
            description TEXT,
            technician TEXT,
            cost REAL,
            status TEXT DEFAULT 'Plánováno',
            scheduled_date TEXT,
            completed_date TEXT,
            next_service_date TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabulka servisních plánů
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_type TEXT,
            asset_id INTEGER,
            service_type TEXT,
            interval_days INTEGER,
            last_service_date TEXT,
            next_service_date TEXT,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabulka náhradních dílů
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_record_id INTEGER,
            part_name TEXT,
            part_number TEXT,
            quantity INTEGER,
            unit_price REAL,
            total_price REAL,
            supplier TEXT,
            FOREIGN KEY (service_record_id) REFERENCES service_records (id)
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
