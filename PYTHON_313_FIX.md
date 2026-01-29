# PYTHON 3.13 COMPATIBILITY FIX

## Problem
The original Pandas version (2.1.4) doesn't have pre-built packages for Python 3.13,
which causes the compiler error you saw.

## Solution 1: Updated Requirements (EASIEST - Try this first)
1. Replace your requirements.txt with this:

flask>=3.0.0
werkzeug>=3.0.0
pandas>=2.2.0
openpyxl>=3.1.2
xlsxwriter>=3.1.0

2. Run install.bat again

## Solution 2: Downgrade to Python 3.11 (If Solution 1 fails)
1. Uninstall Python 3.13
2. Download Python 3.11 from https://python.org/downloads/release/python-3119/
3. Install it (CHECK "Add to PATH")
4. Delete the gst_pro_v2 folder
5. Re-extract the ZIP
6. Run install.bat

## Solution 3: No Pandas/Excel Export (If nothing else works)
Use requirements_minimal.txt instead:
- Reports will show in browser only
- Export button will save CSV instead of Excel
- All other features work normally!

To use this:
1. Copy requirements_minimal.txt to requirements.txt
2. Edit app.py - find the export_excel function and replace with the CSV version below:

@app.route('/export/csv')  # Changed from /export/excel
def export_csv():
    view_type = request.args.get('view', 'monthly')
    month = int(request.args.get('month', 1))
    year = int(request.args.get('year', 2024))

    conn = get_db()
    clients = conn.execute("SELECT * FROM clients WHERE status = 'active'").fetchall()

    import csv
    import io
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['Client Name', 'GSTIN', 'Period', 'GSTR-1 Status', 'GSTR-1 ARN', 'GSTR-3B Status', 'GSTR-3B ARN'])

    for client in clients:
        g1 = conn.execute("SELECT status, arn_number FROM gstr1_records WHERE client_id=? AND month=? AND year=?", 
                         (client['id'], month, year)).fetchone()
        g3 = conn.execute("SELECT status, arn_number FROM gstr3b_records WHERE client_id=? AND month=? AND year=?", 
                         (client['id'], month, year)).fetchone()

        writer.writerow([
            client['client_name'],
            client['gstin'] or '',
            f"{month}-{year}",
            g1['status'] if g1 else 'Not Started',
            g1['arn_number'] if g1 else '',
            g3['status'] if g3 else 'Pending',
            g3['arn_number'] if g3 else ''
        ])

    conn.close()

    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=GST_Report_{month}_{year}.csv"}
    )

## RECOMMENDED: Quick Fix Steps
1. Open requirements.txt in Notepad
2. Replace ALL text with:

flask>=3.0.0
werkzeug>=3.0.0
pandas>=2.2.0
openpyxl>=3.1.2

3. Save
4. Run: python -m pip install --upgrade pip
5. Run install.bat again

This should work with your Python 3.13 installation.
