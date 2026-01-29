#!/usr/bin/env python3
"""
GST Pro v2.0 - Complete Working Version
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file, Response
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
import os
import json
import shutil
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
from io import BytesIO
import csv
import io

app = Flask(__name__)
app.secret_key = 'gst-pro-v2-secret-key-2026-change-in-production'

# Setup Logging
if not os.path.exists('logs'):
    os.makedirs('logs')
file_handler = RotatingFileHandler('logs/gstpro.log', maxBytes=10240000, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Constants
BACKUP_DIR = 'backups'
ARCHIVE_DIR = 'archive'
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# ==================== HELPERS ====================

def get_current_month_year():
    today = datetime.now()
    first_day = today.replace(day=1)
    last_month = first_day - timedelta(days=1)
    return last_month.month, last_month.year

def get_financial_year(month, year):
    if month >= 4:
        return f"{year}-{str(year+1)[-2:]}"
    else:
        return f"{year-1}-{str(year)[-2:]}"

def get_due_date(month, year, return_type='gstr1'):
    day = 11 if return_type == 'gstr1' else 20
    if month == 12:
        return datetime(year + 1, 1, day)
    else:
        return datetime(year, month + 1, day)

def get_due_status_color(month, year, status, return_type):
    if status == 'locked':
        return 'green'
    elif status in ['approved', 'file_pending']:
        return 'blue'
    elif datetime.now() > get_due_date(month, year, return_type):
        return 'red'
    else:
        return 'yellow'

def get_db():
    conn = sqlite3.connect('gst_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    # Users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'reviewer', 'preparer')),
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Clients
    c.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            gstin TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active'
        )
    """)

    # Assignments
    c.execute("""
        CREATE TABLE IF NOT EXISTS client_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            gstr1_preparer_id INTEGER,
            gstr3b_preparer_id INTEGER,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id),
            UNIQUE(client_id, month, year)
        )
    """)

    # Notifications
    c.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT,
            type TEXT DEFAULT 'info',
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # GSTR-1 Records
    c.execute("""
        CREATE TABLE IF NOT EXISTS gstr1_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            status TEXT DEFAULT 'draft',
            b2b_sales REAL DEFAULT 0,
            b2c_sales REAL DEFAULT 0,
            credit_note REAL DEFAULT 0,
            debit_note REAL DEFAULT 0,
            sez_exempted REAL DEFAULT 0,
            total_sales REAL DEFAULT 0,
            sales_as_per_tally REAL DEFAULT 0,
            variance REAL DEFAULT 0,
            total_cgst REAL DEFAULT 0,
            total_sgst REAL DEFAULT 0,
            total_igst REAL DEFAULT 0,
            chk_sales INTEGER DEFAULT 0,
            chk_sales_time TIMESTAMP,
            chk_purchase INTEGER DEFAULT 0,
            chk_purchase_time TIMESTAMP,
            chk_notes INTEGER DEFAULT 0,
            chk_notes_time TIMESTAMP,
            chk_continuity INTEGER DEFAULT 0,
            chk_continuity_time TIMESTAMP,
            chk_hsn INTEGER DEFAULT 0,
            chk_hsn_time TIMESTAMP,
            chk_nil INTEGER DEFAULT 0,
            chk_nil_time TIMESTAMP,
            preparer_id INTEGER,
            reviewer_id INTEGER,
            prepared_at TIMESTAMP,
            reviewed_at TIMESTAMP,
            arn_number TEXT,
            filed_at TIMESTAMP,
            locked_at TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id),
            UNIQUE(client_id, month, year)
        )
    """)

    # GSTR-3B Records
    c.execute("""
        CREATE TABLE IF NOT EXISTS gstr3b_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            gstr1_tv REAL DEFAULT 0,
            gstr1_cgst REAL DEFAULT 0,
            gstr1_sgst REAL DEFAULT 0,
            gstr1_igst REAL DEFAULT 0,
            liability_tv REAL DEFAULT 0,
            liability_cgst REAL DEFAULT 0,
            liability_sgst REAL DEFAULT 0,
            liability_igst REAL DEFAULT 0,
            tv_2b REAL DEFAULT 0,
            cgst_2b REAL DEFAULT 0,
            sgst_2b REAL DEFAULT 0,
            igst_2b REAL DEFAULT 0,
            tv_tally REAL DEFAULT 0,
            cgst_tally REAL DEFAULT 0,
            sgst_tally REAL DEFAULT 0,
            igst_tally REAL DEFAULT 0,
            ineligible_cgst REAL DEFAULT 0,
            ineligible_sgst REAL DEFAULT 0,
            ineligible_igst REAL DEFAULT 0,
            rcm_cgst REAL DEFAULT 0,
            rcm_sgst REAL DEFAULT 0,
            rcm_igst REAL DEFAULT 0,
            eligible_cgst REAL DEFAULT 0,
            eligible_sgst REAL DEFAULT 0,
            eligible_igst REAL DEFAULT 0,
            eligible_total REAL DEFAULT 0,
            net_cgst REAL DEFAULT 0,
            net_sgst REAL DEFAULT 0,
            net_igst REAL DEFAULT 0,
            net_total REAL DEFAULT 0,
            interest_cgst REAL DEFAULT 0,
            interest_sgst REAL DEFAULT 0,
            interest_igst REAL DEFAULT 0,
            late_fee REAL DEFAULT 0,
            tv_variance REAL DEFAULT 0,
            preparer_id INTEGER,
            reviewer_id INTEGER,
            prepared_at TIMESTAMP,
            reviewed_at TIMESTAMP,
            arn_number TEXT,
            filed_at TIMESTAMP,
            locked_at TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id),
            UNIQUE(client_id, month, year)
        )
    """)

    # Activity Logs
    c.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            client_id INTEGER,
            month INTEGER,
            year INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Default admin
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        admin_hash = generate_password_hash('admin123')
        c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                 ('admin', admin_hash, 'admin'))

    conn.commit()
    conn.close()

def add_notification(user_id, title, message, type='info'):
    try:
        conn = get_db()
        conn.execute("INSERT INTO notifications (user_id, title, message, type) VALUES (?, ?, ?, ?)",
                    (user_id, title, message, type))
        conn.commit()
        conn.close()
    except:
        pass

def get_notifications(user_id):
    conn = get_db()
    notifs = conn.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 10",
                         (user_id,)).fetchall()
    unread = conn.execute("SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0",
                         (user_id,)).fetchone()[0]
    conn.close()
    return notifs, unread

def log_activity(user_id, action, details='', client_id=None, month=None, year=None):
    conn = get_db()
    conn.execute("INSERT INTO activity_logs (user_id, action, details, client_id, month, year) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, action, details, client_id, month, year))
    conn.commit()
    conn.close()

# ==================== DECORATORS ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('role') not in roles:
                flash('You do not have permission to access this page', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ==================== ROUTES ====================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND active = 1", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            log_activity(user['id'], 'LOGIN')
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    curr_month, curr_year = get_current_month_year()
    fy = get_financial_year(curr_month, curr_year)
    month_name = datetime(2000, curr_month, 1).strftime('%B')

    conn = get_db()
    user_id = session['user_id']
    role = session['role']

    notifications, unread = get_notifications(user_id)

    # Basic data structure
    data = {
        'current_month': curr_month,
        'current_year': curr_year,
        'fy': fy,
        'month_name': month_name,
        'notifications': notifications,
        'unread_count': unread
    }

    try:
        if role == 'admin':
            # Admin stats
            total_clients = conn.execute("SELECT COUNT(*) FROM clients WHERE status = 'active'").fetchone()[0]
            gstr1_stats = conn.execute("""
                SELECT status, COUNT(*) as count FROM gstr1_records 
                WHERE month = ? AND year = ? GROUP BY status
            """, (curr_month, curr_year)).fetchall()
            gstr1_stats = {row['status']: row['count'] for row in gstr1_stats}

            g1_filed = gstr1_stats.get('locked', 0)
            g1_pending = total_clients - g1_filed

            g3_filed = conn.execute("""
                SELECT COUNT(*) FROM gstr3b_records 
                WHERE month = ? AND year = ? AND status = 'locked'
            """, (curr_month, curr_year)).fetchone()[0]
            g3_pending = total_clients - g3_filed

            data.update({
                'total_clients': total_clients,
                'gstr1_stats': gstr1_stats,
                'g1_filed': g1_filed,
                'g1_pending': g1_pending,
                'g3_filed': g3_filed,
                'g3_pending': g3_pending,
                'view': 'admin'
            })

        elif role == 'reviewer':
            data.update({'view': 'reviewer', 'pending_count': 0})
        else:
            data.update({'view': 'preparer', 'assigned_clients': []})

    except Exception as e:
        app.logger.error(f'Dashboard error: {e}')
        data.update({'view': role, 'error': str(e)})

    conn.close()
    return render_template('dashboard.html', **data, user_role=role)

@app.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    conn = get_db()
    users = conn.execute("SELECT * FROM users ORDER BY role, username").fetchall()
    clients = conn.execute("SELECT * FROM clients WHERE status = 'active' ORDER BY client_name").fetchall()
    preparers = [u for u in users if u['role'] == 'preparer']
    reviewers = [u for u in users if u['role'] == 'reviewer']
    conn.close()
    return render_template('admin_panel.html', users=users, clients=clients, preparers=preparers, reviewers=reviewers)

@app.route('/reports')
@login_required
@role_required('admin')
def reports():
    view_type = request.args.get('view', 'monthly')
    month = int(request.args.get('month', get_current_month_year()[0]))
    year = int(request.args.get('year', get_current_month_year()[1]))
    fy_label = get_financial_year(month, year)

    conn = get_db()
    clients = conn.execute("SELECT * FROM clients WHERE status = 'active' ORDER BY client_name").fetchall()
    total = len(clients)

    g1_filed = conn.execute("SELECT COUNT(*) FROM gstr1_records WHERE month=? AND year=? AND status='locked'",
                           (month, year)).fetchone()[0]
    g3_filed = conn.execute("SELECT COUNT(*) FROM gstr3b_records WHERE month=? AND year=? AND status='locked'",
                           (month, year)).fetchone()[0]

    conn.close()

    return render_template('reports.html', view_type=view_type, fy_label=fy_label, 
                         month=month, year=year, total=total,
                         g1_filed=g1_filed, g1_pending=total-g1_filed,
                         g3_filed=g3_filed, g3_pending=total-g3_filed,
                         report_data=[])

@app.route('/export/excel')
@login_required
def export_excel():
    month = int(request.args.get('month', get_current_month_year()[0]))
    year = int(request.args.get('year', get_current_month_year()[1]))

    conn = get_db()
    clients = conn.execute("SELECT * FROM clients WHERE status='active'").fetchall()

    data = []
    for client in clients:
        g1 = conn.execute("SELECT status, arn_number FROM gstr1_records WHERE client_id=? AND month=? AND year=?",
                         (client['id'], month, year)).fetchone()
        g3 = conn.execute("SELECT status, arn_number FROM gstr3b_records WHERE client_id=? AND month=? AND year=?",
                         (client['id'], month, year)).fetchone()

        data.append({
            'Client': client['client_name'],
            'GSTIN': client['gstin'] or '',
            'Period': f"{month}-{year}",
            'GSTR-1 Status': g1['status'] if g1 else 'Not Started',
            'GSTR-1 ARN': g1['arn_number'] if g1 else '',
            'GSTR-3B Status': g3['status'] if g3 else 'Pending',
            'GSTR-3B ARN': g3['arn_number'] if g3 else ''
        })

    conn.close()

    try:
        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False, sheet_name='GST Report')
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         as_attachment=True, download_name=f'GST_Report_{month}_{year}.xlsx')
    except:
        # Fallback to CSV if pandas fails
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys() if data else [])
        writer.writeheader()
        writer.writerows(data)
        output.seek(0)
        return Response(output.getvalue(), mimetype='text/csv',
                       headers={'Content-Disposition': f'attachment;filename=GST_Report_{month}_{year}.csv'})

# Admin routes
@app.route('/admin/user', methods=['POST'])
@login_required
def manage_user():
    action = request.form.get('action')
    conn = get_db()

    if action == 'create':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        pwd_hash = generate_password_hash(password)
        try:
            conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, pwd_hash, role))
            conn.commit()
            flash('User created', 'success')
        except:
            flash('Username exists', 'error')
    elif action == 'toggle':
        user_id = request.form['user_id']
        user = conn.execute("SELECT active FROM users WHERE id=?", (user_id,)).fetchone()
        if user:
            new_status = 0 if user['active'] else 1
            conn.execute("UPDATE users SET active=? WHERE id=?", (new_status, user_id))
            conn.commit()
            flash('User updated', 'success')

    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/admin/client', methods=['POST'])
@login_required
def manage_client():
    name = request.form['client_name']
    gstin = request.form.get('gstin', '')
    conn = get_db()
    conn.execute("INSERT INTO clients (client_name, gstin) VALUES (?, ?)", (name, gstin))
    conn.commit()
    conn.close()
    flash('Client added', 'success')
    return redirect(url_for('dashboard'))

@app.route('/api/assign', methods=['POST'])
@login_required
def assign_client():
    data = request.json
    conn = get_db()

    existing = conn.execute("""
        SELECT * FROM client_assignments WHERE client_id=? AND month=? AND year=?
    """, (data['client_id'], data['month'], data['year'])).fetchone()

    if existing:
        conn.execute("""
            UPDATE client_assignments 
            SET gstr1_preparer_id=?, gstr3b_preparer_id=?, created_by=?
            WHERE id=?
        """, (data.get('gstr1_preparer_id'), data.get('gstr3b_preparer_id'), session['user_id'], existing['id']))
    else:
        conn.execute("""
            INSERT INTO client_assignments (client_id, month, year, gstr1_preparer_id, gstr3b_preparer_id, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (data['client_id'], data['month'], data['year'], 
               data.get('gstr1_preparer_id'), data.get('gstr3b_preparer_id'), session['user_id']))

    conn.commit()
    conn.close()
    return jsonify({'success': True})

# GSTR-1 Routes
@app.route('/gstr1/<int:client_id>/<int:month>/<int:year>')
@login_required
def gstr1_form(client_id, month, year):
    conn = get_db()
    client = conn.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
    reviewers = conn.execute("SELECT * FROM users WHERE role='reviewer' AND active=1").fetchall()

    if not client:
        conn.close()
        flash('Client not found', 'error')
        return redirect(url_for('dashboard'))

    record = conn.execute("""
        SELECT * FROM gstr1_records WHERE client_id=? AND month=? AND year=?
    """, (client_id, month, year)).fetchone()

    if not record:
        conn.execute("""
            INSERT INTO gstr1_records (client_id, month, year, preparer_id, prepared_at)
            VALUES (?, ?, ?, ?, ?)
        """, (client_id, month, year, session['user_id'], datetime.now()))
        conn.commit()
        record = conn.execute("""
            SELECT * FROM gstr1_records WHERE client_id=? AND month=? AND year=?
        """, (client_id, month, year)).fetchone()

    is_locked = record['status'] == 'locked'
    can_edit = record['status'] in ['draft', 'under_review'] and session['role'] in ['admin', 'preparer', 'reviewer']

    conn.close()

    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']

    return render_template('gstr1_form.html', 
                         client=client, record=record, month=month, year=year,
                         month_name=months[month-1], reviewers=reviewers,
                         can_edit=can_edit, is_locked=is_locked, user_role=session['role'])

@app.route('/api/gstr1/autosave', methods=['POST'])
@login_required
def api_gstr1_autosave():
    data = request.json
    record_id = data.get('record_id')

    conn = get_db()
    b2b = float(data.get('b2b_sales', 0))
    b2c = float(data.get('b2c_sales', 0))
    credit = float(data.get('credit_note', 0))
    debit = float(data.get('debit_note', 0))
    sez = float(data.get('sez_exempted', 0))
    tally = float(data.get('sales_as_per_tally', 0))
    cgst = float(data.get('total_cgst', 0))
    sgst = float(data.get('total_sgst', 0))
    igst = float(data.get('total_igst', 0))

    total = b2b + b2c - credit + debit + sez
    variance = total - tally

    conn.execute("""
        UPDATE gstr1_records SET
            b2b_sales=?, b2c_sales=?, credit_note=?, debit_note=?, sez_exempted=?,
            total_sales=?, sales_as_per_tally=?, variance=?,
            total_cgst=?, total_sgst=?, total_igst=?, preparer_id=?
        WHERE id=?
    """, (b2b, b2c, credit, debit, sez, total, tally, variance, cgst, sgst, igst, session['user_id'], record_id))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'total_sales': total, 'variance': variance})

@app.route('/api/gstr1/checklist', methods=['POST'])
@login_required
def api_gstr1_checklist():
    data = request.json
    field = data.get('field')
    checked = data.get('checked', False)

    field_map = {'sales': 'chk_sales', 'purchase': 'chk_purchase', 'notes': 'chk_notes',
                 'continuity': 'chk_continuity', 'hsn': 'chk_hsn', 'nil': 'chk_nil'}

    if field not in field_map:
        return jsonify({'error': 'Invalid field'}), 400

    db_field = field_map[field]
    time_field = f"{db_field}_time"

    conn = get_db()
    if checked:
        conn.execute(f"UPDATE gstr1_records SET {db_field}=1, {time_field}=? WHERE id=?",
                    (datetime.now(), data['record_id']))
    else:
        conn.execute(f"UPDATE gstr1_records SET {db_field}=0, {time_field}=NULL WHERE id=?",
                    (data['record_id'],))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/gstr3b/<int:client_id>/<int:month>/<int:year>')
@login_required
def gstr3b_form(client_id, month, year):
    conn = get_db()
    client = conn.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
    gstr1 = conn.execute("""
        SELECT * FROM gstr1_records WHERE client_id=? AND month=? AND year=? AND status='locked'
    """, (client_id, month, year)).fetchone()

    if not gstr1:
        conn.close()
        flash('GSTR-1 must be locked first', 'error')
        return redirect(url_for('gstr1_form', client_id=client_id, month=month, year=year))

    record = conn.execute("""
        SELECT * FROM gstr3b_records WHERE client_id=? AND month=? AND year=?
    """, (client_id, month, year)).fetchone()

    if not record:
        conn.execute("""
            INSERT INTO gstr3b_records (client_id, month, year, gstr1_tv, gstr1_cgst, gstr1_sgst, gstr1_igst)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (client_id, month, year, gstr1['total_sales'], gstr1['total_cgst'], gstr1['total_sgst'], gstr1['total_igst']))
        conn.commit()
        record = conn.execute("""
            SELECT * FROM gstr3b_records WHERE client_id=? AND month=? AND year=?
        """, (client_id, month, year)).fetchone()

    conn.close()

    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']

    return render_template('gstr3b_form.html', client=client, record=record, gstr1=gstr1,
                         month=month, year=year, month_name=months[month-1],
                         can_edit=True, is_locked=False)

@app.route('/api/gstr3b/save', methods=['POST'])
@login_required
def api_gstr3b_save():
    data = request.json
    conn = get_db()

    fields = ['liability_tv', 'liability_cgst', 'liability_sgst', 'liability_igst',
              'tv_2b', 'cgst_2b', 'sgst_2b', 'igst_2b',
              'tv_tally', 'cgst_tally', 'sgst_tally', 'igst_tally',
              'ineligible_cgst', 'ineligible_sgst', 'ineligible_igst',
              'rcm_cgst', 'rcm_sgst', 'rcm_igst',
              'interest_cgst', 'interest_sgst', 'interest_igst', 'late_fee',
              'eligible_cgst', 'eligible_sgst', 'eligible_igst',
              'net_cgst', 'net_sgst', 'net_igst', 'tv_variance']

    values = [float(data.get(f, 0)) for f in fields]
    values.append(data.get('record_id'))

    sql = "UPDATE gstr3b_records SET " + ", ".join([f"{f}=?" for f in fields]) + " WHERE id=?"
    conn.execute(sql, values)
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# Init and run
if __name__ == '__main__':
    init_db()

    # Simple backup
    try:
        today = datetime.now()
        backup_name = f"{BACKUP_DIR}/gst_backup_{today.strftime('%Y%m')}.db"
        if not os.path.exists(backup_name) and os.path.exists('gst_database.db'):
            shutil.copy('gst_database.db', backup_name)
    except:
        pass

    print("="*60)
    print("GST Pro v2.0 Server Starting...")
    print("="*60)
    print("Access URLs:")
    print("  Local:   http://127.0.0.1:5000")
    print("  Network: http://YOUR_IP:5000")
    print("="*60)
    print("Press CTRL+C to stop")
    print("="*60)

    app.run(host='0.0.0.0', port=5000, debug=False)


# Archive route (missing)
@app.route('/admin/archive_fy', methods=['POST'])
@login_required
@role_required('admin')
def archive_fy():
    fy = request.form.get('fy')
    conn = get_db()
    archive_db = f"{ARCHIVE_DIR}/gst_archive_{fy}.db"
    if os.path.exists('gst_database.db'):
        shutil.copy('gst_database.db', archive_db)
        conn.execute("INSERT INTO archived_periods (fy, file_path) VALUES (?, ?)", (fy, archive_db))
        conn.commit()
        flash(f'Financial Year {fy} archived', 'success')
    conn.close()
    return redirect(url_for('admin_panel'))

# Check due dates API
@app.route('/api/check_due_dates')
@login_required
def check_due_dates():
    return jsonify([])

# Notifications API
@app.route('/api/notifications')
@login_required
def get_notifications_api():
    user_id = session['user_id']
    conn = get_db()
    notifs = conn.execute("SELECT * FROM notifications WHERE user_id=? AND is_read=0 ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(n) for n in notifs])

@app.route('/api/notifications/read', methods=['POST'])
@login_required
def mark_notifications_read():
    conn = get_db()
    conn.execute("UPDATE notifications SET is_read=1 WHERE user_id=?", (session['user_id'],))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# GSTR-1 Review actions
@app.route('/gstr1/submit_review', methods=['POST'])
@login_required
def submit_gstr1_review():
    record_id = request.form.get('record_id')
    reviewer_id = request.form.get('reviewer_id')
    conn = get_db()
    conn.execute("UPDATE gstr1_records SET status='under_review', reviewer_id=? WHERE id=?", (reviewer_id, record_id))
    conn.commit()
    add_notification(reviewer_id, 'New Review', 'GSTR-1 submitted for review', 'info')
    conn.close()
    flash('Submitted for review', 'success')
    return redirect(url_for('dashboard'))

@app.route('/gstr1/review_action', methods=['POST'])
@login_required
@role_required('admin', 'reviewer')
def gstr1_review_action():
    record_id = request.form.get('record_id')
    action = request.form.get('action')
    remarks = request.form.get('remarks', '')
    conn = get_db()
    record = conn.execute("SELECT * FROM gstr1_records WHERE id=?", (record_id,)).fetchone()
    if action == 'approve':
        conn.execute("UPDATE gstr1_records SET status='approved', reviewed_at=?, reviewer_id=? WHERE id=?", (datetime.now(), session['user_id'], record_id))
        if record:
            add_notification(record['preparer_id'], 'Approved', 'GSTR-1 approved', 'success')
    else:
        conn.execute("UPDATE gstr1_records SET status='draft', reviewer_id=NULL WHERE id=?", (record_id,))
        if record:
            add_notification(record['preparer_id'], 'Sent Back', remarks, 'warning')
    conn.commit()
    conn.close()
    flash('Review action completed', 'success')
    return redirect(url_for('dashboard'))

@app.route('/gstr1/file', methods=['POST'])
@login_required
def file_gstr1():
    record_id = request.form.get('record_id')
    arn = request.form.get('arn_number')
    conn = get_db()
    conn.execute("UPDATE gstr1_records SET status='locked', arn_number=?, filed_at=?, locked_at=? WHERE id=?", (arn, datetime.now(), datetime.now(), record_id))
    conn.commit()
    conn.close()
    flash('GSTR-1 filed and locked', 'success')
    return redirect(url_for('dashboard'))
