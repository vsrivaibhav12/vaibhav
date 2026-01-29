# Paste this function into app.py to replace Pandas Excel export with CSV\n
# Alternative export function without Pandas (CSV instead of Excel)
@app.route('/export')
@login_required
@role_required('admin')
def export_report():
    """Export to CSV (no Pandas required)"""
    view_type = request.args.get('view', 'monthly')
    month = int(request.args.get('month', get_current_month_year()[0]))
    year = int(request.args.get('year', get_current_month_year()[1]))

    conn = get_db()
    clients = conn.execute("SELECT * FROM clients WHERE status = 'active' ORDER BY client_name").fetchall()

    import csv
    import io
    from flask import Response

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        'Client Name', 'GSTIN', 'Period', 
        'GSTR-1 Status', 'GSTR-1 ARN', 'GSTR-1 Filed Date',
        'GSTR-3B Status', 'GSTR-3B ARN', 'GSTR-3B Filed Date'
    ])

    for client in clients:
        g1 = conn.execute("""
            SELECT status, arn_number, filed_at 
            FROM gstr1_records 
            WHERE client_id=? AND month=? AND year=?
        """, (client['id'], month, year)).fetchone()

        g3 = conn.execute("""
            SELECT status, arn_number, filed_at 
            FROM gstr3b_records 
            WHERE client_id=? AND month=? AND year=?
        """, (client['id'], month, year)).fetchone()

        writer.writerow([
            client['client_name'],
            client['gstin'] or '',
            f"{month}-{year}",
            g1['status'] if g1 else 'Not Started',
            g1['arn_number'] if g1 else '',
            g1['filed_at'] if g1 else '',
            g3['status'] if g3 else 'Pending',
            g3['arn_number'] if g3 else '',
            g3['filed_at'] if g3 else ''
        ])

    conn.close()

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=GST_Report_{month}_{year}.csv"}
    )
