#!/usr/bin/env python3
"""
Demo Data Generator for GST Pro v2.0
Run this to create sample data for testing and training
"""

import sqlite3
import sys
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_demo_data():
    conn = sqlite3.connect('gst_database.db')
    cursor = conn.cursor()

    print("🚀 GST Pro Demo Data Generator")
    print("="*50)

    # Create sample users
    print("\n👥 Creating sample users...")
    users = [
        ('ca_senior1', 'password123', 'reviewer'),
        ('ca_senior2', 'password123', 'reviewer'),
        ('prep_junior1', 'password123', 'preparer'),
        ('prep_junior2', 'password123', 'preparer'),
        ('prep_junior3', 'password123', 'preparer'),
        ('manager', 'password123', 'admin'),
    ]

    created_users = []
    for username, pwd, role in users:
        try:
            pwd_hash = generate_password_hash(pwd)
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                          (username, pwd_hash, role))
            created_users.append(username)
            print(f"   ✓ {username} ({role})")
        except sqlite3.IntegrityError:
            print(f"   ! {username} already exists, skipping")

    # Create sample clients
    print("\n🏢 Creating sample clients...")
    clients = [
        ('ABC Manufacturing Pvt Ltd', '27AABCU9603R1ZX'),
        ('XYZ Trading Company', '29AAGCM1234P1ZT'),
        ('Smith Services LLP', '07AAACS1234A1Z5'),
        ('Global Exports Inc', '33AAACG4567L1ZP'),
        ('Local Retail Shop', '09AAACI7890Q1ZR'),
        ('Tech Solutions India', '36AAACJ2345K1ZU'),
        ('Green Energy Co', '29AAACK3456L1ZQ'),
        ('Healthcare Plus', '07AAACL4567M1ZR'),
    ]

    client_ids = []
    for name, gstin in clients:
        try:
            cursor.execute("INSERT INTO clients (client_name, gstin) VALUES (?, ?)", (name, gstin))
            client_ids.append(cursor.lastrowid)
            print(f"   ✓ {name[:40]}")
        except sqlite3.IntegrityError:
            cursor.execute("SELECT id FROM clients WHERE client_name = ?", (name,))
            result = cursor.fetchone()
            if result:
                client_ids.append(result[0])
                print(f"   ! {name[:40]} (exists)")

    if not client_ids:
        print("   No clients created!")
        conn.close()
        return

    # Get preparer IDs
    cursor.execute("SELECT id FROM users WHERE role = 'preparer'")
    preparers = [r[0] for r in cursor.fetchall()]

    if not preparers:
        print("\n❌ No preparers found! Create preparer users first.")
        conn.close()
        return

    # Create assignments for current month
    now = datetime.now()
    month = now.month - 1 if now.month > 1 else 12
    year = now.year if now.month > 1 else now.year - 1

    print(f"\n🔗 Creating assignments for {month}/{year}...")

    assignments_created = 0
    for i, client_id in enumerate(client_ids):
        prep1 = preparers[i % len(preparers)]
        prep2 = preparers[(i + 1) % len(preparers)] if len(preparers) > 1 else prep1

        try:
            cursor.execute("""
                INSERT INTO client_assignments 
                (client_id, month, year, gstr1_preparer_id, gstr3b_preparer_id, created_by)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (client_id, month, year, prep1, prep2))
            assignments_created += 1
        except sqlite3.IntegrityError:
            pass

    print(f"   ✓ {assignments_created} assignments created")

    # Create sample GSTR-1 records for some clients
    print("\n📝 Creating sample GSTR-1 records...")

    import random
    sample_clients = client_ids[:4]  # First 4 clients

    for client_id in sample_clients:
        b2b = round(random.uniform(50000, 500000), 2)
        b2c = round(random.uniform(20000, 200000), 2)
        tally = b2b + b2c  # Perfect match for demo

        try:
            cursor.execute("""
                INSERT INTO gstr1_records 
                (client_id, month, year, status, b2b_sales, b2c_sales, total_sales, 
                sales_as_per_tally, variance, total_cgst, total_sgst, total_igst,
                chk_sales, chk_purchase, chk_notes, preparer_id, prepared_at)
                VALUES (?, ?, ?, 'draft', ?, ?, ?, ?, 0, ?, ?, ?, 1, 1, 1, ?, ?)
            """, (client_id, month, year, b2b, b2c, b2b+b2c, tally, 
                  b2b*0.09, b2b*0.09, b2c*0.18, preparers[0], datetime.now()))
            print(f"   ✓ Client {client_id}: ₹{b2b+b2c:,.2f}")
        except Exception as e:
            print(f"   ! Client {client_id}: {e}")

    conn.commit()
    conn.close()

    print("\n" + "="*50)
    print("✅ Demo data created successfully!")
    print("="*50)
    print("\n🔑 Login Credentials:")
    print("   Admin:    admin / admin123")
    if created_users:
        print("   Others:   [username] / password123")
        print("   Examples: ca_senior1, prep_junior1, manager")
    print("\n📊 Next Steps:")
    print("   1. Start server (run.bat)")
    print("   2. Login with any account")
    print("   3. Check dashboards are populated")
    print("   4. Test workflow with sample data")
    print("="*50)

if __name__ == '__main__':
    create_demo_data()
