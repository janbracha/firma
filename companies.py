from database import connect


def fetch_companies():
    """Načte všechny firmy z databáze správně jako seznam tuple."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name, ico, dic, bank, contact, address FROM companies")
    data = cursor.fetchall()  # Vrací seznam tuple [(název, ico, dic, bank, contact, adresa), ...]
    conn.close()
    return data

def fetch_company_names():
    """Načte názvy firem z databáze pro výběr v rozbalovacím seznamu."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM companies")
    data = [row[0] for row in cursor.fetchall()]  # Vrací seznam názvů firem
    conn.close()
    return data

def update_company(old_name, updated_data):
    """Aktualizuje data firmy v databázi."""
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE companies 
            SET name=?, ico=?, dic=?, bank=?, contact=?, address=? 
            WHERE name=?
        """, (*updated_data, old_name))
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        conn.close()

def add_company(name, ico, dic, bank, contact, address):
    """Přidá firmu do databáze, pokud ještě neexistuje."""
    conn = connect()
    cursor = conn.cursor()

    # Kontrola duplicit
    cursor.execute("SELECT COUNT(*) FROM companies WHERE name=?", (name,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False

    # Vložení firmy se všemi novými atributy
    cursor.execute("""
        INSERT INTO companies (name, ico, dic, bank, contact, address) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, ico, dic, bank, contact, address))

    conn.commit()
    conn.close()
    return True