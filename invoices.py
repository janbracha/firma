from database import connect

def add_invoice(data):
    """Přidání nové faktury."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO invoices (invoice_number, type, recipient, issuer, issue_date, tax_date, due_date,
        amount_no_tax, tax, total, status, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def delete_invoice(invoice_id):
    """Smazání faktury podle ID."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM invoices WHERE id=?", (invoice_id,))
    conn.commit()
    conn.close()

def update_invoice(invoice_id, updated_data):
    """Aktualizace faktury v databázi."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE invoices 
        SET invoice_number=?, type=?, recipient=?, issuer=?, issue_date=?, tax_date=?, due_date=?, 
            amount_no_tax=?, tax=?, total=?, status=?, note=? 
        WHERE id=?
    """, (*updated_data, invoice_id))
    conn.commit()
    conn.close()


