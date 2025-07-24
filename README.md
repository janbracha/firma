# 🚀 Firemní aplikace - Kompletní systém pro správu firmy

## 🎯 JAK SPUSTIT APLIKACI:

### ✅ Nejjednodušší způsob:
**Poklikejte na soubor `start_app.bat`**

### � Alternativní způsob:
1. Otevřete PowerShell nebo Command Prompt
2. Přejděte do složky projektu: `cd C:\git\firma`
3. Aktivujte virtuální prostředí: `.venv\Scripts\activate`
4. Spusťte aplikaci: `python main.py`

## 📊 Statistiky projektu:
- **11,000+ řádků** Python kódu
- **15+ modulů** s kompletní funkcionalitou
- **Žádné placeholder funkce** - vše je plně implementováno

## 🏢 Funkce aplikace:
- `main.py` - Spouštěcí soubor aplikace
- `gui.py` - Hlavní GUI interface
- `database.py` - Správa databáze a vytváření tabulek

### 👥 Uživatelská správa:
- `user_management.py` - Backend pro správu uživatelů
- `user_management_window.py` - GUI pro správu uživatelů
- `role_management.py` - Backend pro správu rolí a oprávnění
- `role_management_window.py` - GUI pro správu rolí
- `change_password_dialog.py` - Dialog pro změnu hesla

### 📄 Správa dokumentů:
- `document_management.py` - Backend pro správu dokumentů
- `document_management_window.py` - GUI pro správu dokumentů

### 💼 Firemní moduly:
- `companies.py` - Správa firemních údajů
- `company_managment.py` - Správa nastavení společnosti
- `company_settings.py` - Nastavení společnosti

### 🧾 Fakturace a účetnictví:
- `invoices.py` - Správa faktur
- `invoice_management.py` - GUI pro správu faktur
- `cash_journal.py` - Pokladní kniha

### 🚛 Doprava a logistika:
- `vehicle_management.py` - Správa vozidel
- `driver_management.py` - Správa řidičů
- `destination_management.py` - Správa destinací
- `fuel_management.py` - Správa paliv
- `trip_book.py` - Kniha jízd
- `trip_calculation.py` - Výpočty cest

### 🗃️ Databáze:
- `invoices.db` - SQLite databáze

### 📁 Složky:
- `documents/` - Nahrané dokumenty
- `.venv/` - Python virtuální prostředí
- `.git/` - Git repozitář

## ✨ Implementované funkce:

### ✅ Kompletní uživatelská správa
- CRUD operace pro uživatele
- Aktivace/deaktivace uživatelů
- Trvalé mazání neaktivních uživatelů
- Změna hesel

### ✅ Flexibilní systém rolí a oprávnění
- Vytváření vlastních rolí
- Přiřazování oprávnění
- Správa uživatelských práv

### ✅ Pokročilá správa dokumentů
- Upload dokumentů (PDF, PNG, JPG, TXT, DOC, DOCX)
- Náhledy všech typů souborů
- Škálování obrázků na 800x600px
- Zobrazení obsahu textových souborů
- Náhled první stránky PDF
- Drag & drop upload
- Integrace s fakturami

### ✅ Vyčištěný kód
- Odstraněno 45+ testovacích souborů
- Vyčištěny debug výstupy
- Pouze produkční kód

## 🎯 Přístup k funkcím:
- **Systém → Správa uživatelů** (uživatelé a role)
- **Systém → Správa dokumentů** (všechny dokumenty)
- **Faktury → tlačítko Dokumenty** (dokumenty konkrétní faktury)
