# 🔧 Technická dokumentace - Firemní aplikace

> **Pro vývojáře a správce systému**

## 📁 Architektura projektu

### **Hlavní komponenty**
```
firma/
├── main.py                 # Entry point aplikace
├── gui.py                  # Hlavní GUI a dashboard  
├── database.py             # Databázové operace a migrace
├── simple_login.py         # Přihlašovací systém
└── invoices.db            # SQLite databáze
```

### **Moduly funkcí**
```
├── user_management.py         # Backend správy uživatelů
├── user_management_window.py  # GUI správy uživatelů  
├── role_management.py         # Backend správy rolí
├── role_management_window.py  # GUI správy rolí
├── invoice_management.py      # Správa faktur
├── cash_journal.py           # Pokladní deník
├── company_managment.py      # Správa firem
├── trip_book.py             # Kniha jízd
├── employee_management.py    # Správa zaměstnanců
├── warehouse_management.py   # Skladové hospodářství
├── asset_management.py      # Správa majetku
├── calendar_schedule.py     # Kalendář
├── service_maintenance.py   # Servis a údržba
├── analytics_reports.py    # Analýzy a reporty
└── document_management_window.py # Správa dokumentů
```

### **Pomocné moduly**
```
├── companies.py              # Backend správy firem
├── invoices.py              # Backend fakturace
├── vehicle_management.py    # Backend vozidel
├── driver_management.py     # Backend řidičů
├── destination_management.py # Backend destinací
├── fuel_management.py       # Backend pohonných hmot
├── trip_calculation.py      # Výpočty cest
└── company_settings.py      # Nastavení firmy
```

## 🗄️ Databázová struktura

### **Hlavní tabulky**
- `users` - Uživatelé systému
- `roles` - Role uživatelů
- `permissions` - Oprávnění systému
- `role_permissions` - Přiřazení oprávnění k rolím
- `invoices` - Faktury
- `companies` - Firemní kontakty
- `cash_journal` - Pokladní deník
- `employees` - Zaměstnanci
- `assets` - Hmotný majetek
- `warehouse_items` - Skladové položky
- `calendar_events` - Kalendářní události
- `maintenance_plans` - Plány údržby

### **Dopravní tabulky**
- `drivers` - Řidiči
- `cars` - Vozidla
- `destinations` - Destinace
- `trips` - Jízdy
- `fuel_tankings` - Tankování

### **Systémové tabulky**
- `company_settings` - Nastavení firmy
- `documents` - Správa dokumentů

## 🔐 Systém oprávnění

### **Hierarchie rolí**
1. **Admin** (`admin`) - 57 oprávnění
2. **Accountant** (`accountant`) - 45 oprávnění  
3. **User** (`user`) - 14 oprávnění

### **Moduly oprávnění** (12 celkem)
- `users` - Správa uživatelů (5 oprávnění)
- `roles` - Správa rolí (4 oprávnění)
- `invoices` - Fakturace (4 oprávnění)
- `accounting` - Účetnictví (3 oprávnění)
- `company` - Správa firmy (3 oprávnění)
- `documents` - Dokumenty (4 oprávnění)
- `assets` - Majetek (4 oprávnění)
- `transport` - Doprava (8 oprávnění)
- `calendar` - Kalendář (4 oprávnění)
- `warehouse` - Sklad (5 oprávnění)
- `employees` - Zaměstnanci (7 oprávnění)
- `maintenance` - Servis (6 oprávnění)

### **Kontrola oprávnění**
```python
from user_management import UserManager

# Kontrola oprávnění
if UserManager.has_permission(user_role, 'invoices.create'):
    # Uživatel může vytvářet faktury
    pass
```

## 🏗️ Přidání nové funkce

### **1. Vytvoření modulu**
```python
# new_feature.py
from PyQt6.QtWidgets import QMainWindow
from database import connect

class NewFeatureWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # GUI implementace
        pass
```

### **2. Přidání oprávnění**
```python
# V database.py - create_tables()
cursor.execute("""
    INSERT OR IGNORE INTO permissions (name, display_name, description, module, created_date)
    VALUES 
    ('new_feature.view', 'Zobrazit novou funkci', 'Popis', 'new_module', datetime('now')),
    ('new_feature.create', 'Vytvořit záznam', 'Popis', 'new_module', datetime('now'))
""")
```

### **3. Integrace do GUI**
```python
# V gui.py - create_dashboard()
if UserManager.has_permission(self.current_user['role'], 'new_feature.view'):
    card = self.create_function_card("🆕 Nová funkce", 
                                    "Popis funkce", 
                                    self.show_new_feature)
    basic_grid.addWidget(card, row, col)
```

### **4. Aktualizace role_management_window.py**
```python
# Přidat do get_module_display_name()
module_names = {
    # ... existující
    'new_module': 'Název nového modulu'
}
```

## 🔄 Databázové migrace

### **Automatické vytvoření**
- Databáze se vytvoří při prvním spuštění
- Tabulky se vytvoří pomocí `database.py` → `create_tables()`
- Výchozí data se naplní automaticky

### **Ruční migrace**
```python
conn = connect()
cursor = conn.cursor()

# Přidání nové tabulky
cursor.execute("""
    CREATE TABLE IF NOT EXISTS new_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_date TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()
```

## 🎨 UI/UX Guidelines

### **Moderní design**
- **PyQt6** s custom CSS
- **Karty funkcí** pro hlavní menu
- **Responzivní layout** s QScrollArea
- **Konzistentní barvy** a fonty

### **Standardní tlačítka**
```python
# Přidání tlačítka
add_button = QPushButton("Přidat záznam")
add_button.setObjectName("primaryButton")
add_button.clicked.connect(self.add_record)

# CSS styling
add_button.setStyleSheet("""
    QPushButton {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 20px;
    }
""")
```

### **Tabulky s daty**
```python
# Standardní nastavení tabulky
table = QTableWidget()
table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
table.setAlternatingRowColors(True)
table.horizontalHeader().setStretchLastSection(True)

# Blokování signálů při naplňování
table.blockSignals(True)
table.clearContents()
table.setRowCount(len(data))
# ... naplnění dat
table.blockSignals(False)
```

## 🐛 Debugging a Logging

### **Debug výstupy**
```python
# Pro development
print(f"Debug: {variable_value}")

# Pro production - odstraňte debug výstupy
if DEBUG:
    print(f"Debug: {variable_value}")
```

### **Error handling**
```python
try:
    # Databázové operace
    cursor.execute("SELECT * FROM table")
    data = cursor.fetchall()
except Exception as e:
    QMessageBox.critical(self, "Chyba", f"Databázová chyba: {str(e)}")
    print(f"Error: {e}")
finally:
    conn.close()
```

## 🧪 Testování

### **Manuální testování**
1. **Funkční testy** - každá funkce zvlášť
2. **Integračně testy** - kombinace funkcí
3. **UI testy** - responzivita a použitelnost
4. **Bezpečnostní testy** - oprávnění a přístupy

### **Automatické testy**
```python
# test_user_management.py
import unittest
from user_management import UserManager

class TestUserManagement(unittest.TestCase):
    def test_user_creation(self):
        # Test vytvoření uživatele
        pass
    
    def test_permissions(self):
        # Test oprávnění
        pass
```

## 📦 Deployment

### **Příprava produkční verze**
1. **Odstranění debug výstupů**
2. **Optimalizace databázových dotazů**
3. **Kompilace Python souborů**
4. **Vytvoření distribučního balíku**

### **Instalační skript**
```bash
# install.bat
@echo off
echo Instalace firemni aplikace...
python -m pip install PyQt6
python -c "from database import create_tables; create_tables()"
echo Instalace dokoncena!
pause
```

### **Zálohovací strategie**
```bash
# backup.bat
@echo off
set backup_dir=backup_%date:~6,4%_%date:~3,2%_%date:~0,2%
mkdir %backup_dir%
copy invoices.db %backup_dir%\
xcopy documents %backup_dir%\documents\ /E /I
echo Zaloha vytvorena v %backup_dir%
```

## 🔧 Konfigurace

### **Konstany a nastavení**
```python
# config.py
DATABASE_PATH = "invoices.db"
DOCUMENTS_PATH = "documents"
DEBUG = False
VERSION = "1.0"

# Výchozí oprávnění
DEFAULT_ADMIN_PERMISSIONS = "all"
DEFAULT_USER_PERMISSIONS = ["invoices.view", "documents.view"]
```

### **Systémové požadavky**
- Python 3.9+
- PyQt6
- SQLite3 (součást Pythonu)
- Windows 10/11 (testováno)

## 📈 Performance

### **Optimalizace databáze**
```sql
-- Indexy pro rychlejší vyhledávání
CREATE INDEX IF NOT EXISTS idx_invoices_date ON invoices(issue_date);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_role_permissions ON role_permissions(role_id, permission_id);
```

### **Memory management**
```python
# Uzavírání databázových spojení
def closeEvent(self, event):
    if hasattr(self, 'db'):
        self.db.close()
    event.accept()
```

## 🔒 Bezpečnost

### **Hashování hesel**
```python
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed
```

### **SQL Injection prevence**
```python
# SPRÁVNĚ - parametrizované dotazy
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

# ŠPATNĚ - string concatenation
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

### **Auditní trail**
```python
def log_user_action(user_id, action, details):
    cursor.execute("""
        INSERT INTO audit_log (user_id, action, details, timestamp)
        VALUES (?, ?, ?, datetime('now'))
    """, (user_id, action, details))
```

---

## 📞 Kontakt pro vývojáře

**Technické dotazy:**
- 📧 dev@projektdevelop.cz
- 📱 Github: github.com/projektdevelop
- 💬 Discord: ProjektDevelop#1234

**Code review a pull requesty:**
- Používejte feature branches
- Popisné commit messages
- Testování před merge

**Konvence kódu:**
- PEP 8 pro Python
- Anglické názvy proměnných
- České UI texty
- Dokumentace v češtině
