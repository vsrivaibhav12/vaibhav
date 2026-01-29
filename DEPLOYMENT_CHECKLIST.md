# GST Pro v2.0 - Production Deployment Checklist

## ✅ Pre-Deployment (Server Computer)

### 1. Hardware Check
- [ ] Server has 4GB+ RAM
- [ ] 10GB+ free disk space
- [ ] Stable power supply (UPS recommended)
- [ ] Connected to LAN via Ethernet (preferred over WiFi)

### 2. Software Installation
- [ ] Python 3.11+ installed
- [ ] "Add Python to PATH" was checked during install
- [ ] Verified: `python --version` works in Command Prompt
- [ ] Windows Firewall configured (Port 5000 open)

### 3. File Setup
- [ ] Extracted GST_Pro_v2.zip to C:\GSTPro\ (or similar)
- [ ] Ran install.bat successfully (no red errors)
- [ ] Verified requirements.txt packages installed

## 🚀 Deployment

### 4. Initial Configuration
- [ ] Renamed config_template.py to config.py
- [ ] Changed SECRET_KEY in config.py to random string
- [ ] Ran run.bat for first time
- [ ] Database file (gst_database.db) auto-created

### 5. Security Setup (CRITICAL)
- [ ] Accessed http://localhost:5000
- [ ] Logged in with admin/admin123
- [ ] Created new admin account for owner/partner
- [ ] Logged out
- [ ] Logged back in with new admin account
- [ ] Deactivated default "admin" account (do not delete, just deactivate)
- [ ] Created unique accounts for all staff (no shared logins)

### 6. Master Data Setup
- [ ] Created all clients in system
- [ ] Added GSTIN for each client (optional but recommended)
- [ ] Set up client allocations for current month
- [ ] Assigned preparers to clients (separate GSTR-1 and 3B if needed)
- [ ] Verified allocations appear on preparer dashboards

## 🧪 Testing Phase

### 7. Connectivity Testing
- [ ] Server can access: http://localhost:5000
- [ ] Server can access: http://127.0.0.1:5000
- [ ] Found server IP using `ipconfig`
- [ ] **From another computer**: Accessed http://[SERVER-IP]:5000
- [ ] Mobile phone (on WiFi) can access the site
- [ ] All pages load without errors (check browser console)

### 8. Workflow Testing
- [ ] Preparer logged in, sees only assigned clients
- [ ] Preparer opened GSTR-1, entered sample data
- [ ] Auto-save triggered (saw green notification)
- [ ] Preparer checked checklist items (verified timestamps appeared)
- [ ] Preparer submitted for review
- [ ] Reviewer received notification
- [ ] Reviewer saw item in review queue
- [ ] Reviewer approved the test submission
- [ ] Preparer entered dummy ARN and locked record
- [ ] Verified record shows LOCKED status
- [ ] GSTR-3B became available after GSTR-1 locking
- [ ] Admin exported Excel report successfully

### 9. Data Integrity Testing
- [ ] Calculated variance manually, matched system calculation
- [ ] Verified GSTR-3B auto-imports GSTR-1 data correctly
- [ ] Checked eligible ITC calculations are accurate
- [ ] Tested negative liability (carry forward) scenario
- [ ] Verified interest calculations work

## 🔒 Security & Backup

### 10. Backup System
- [ ] Located gst_database.db file
- [ ] Created first manual backup (copy db file to USB/Drive)
- [ ] Verified backups/ folder exists and is writable
- [ ] Confirmed auto-backup is running (check logs/ folder next day)

### 11. User Training
- [ ] Prepared user manual printed/emailed to staff
- [ ] Trained preparers (30 min session each)
- [ ] Trained reviewers (15 min session each)
- [ ] Admin (you) comfortable with all functions

## 📊 Go-Live

### 12. Transition from Excel
- [ ] Identified which client to start with (pilot)
- [ ] Prepared last month's data in parallel (GST Pro + Excel for first month)
- [ ] Confirmed calculations match between old Excel and new system
- [ ] Staff confident to use exclusively

### 13. Monitoring
- [ ] First week: Daily check of logs/gstpro.log
- [ ] Monitored disk space usage
- [ ] Verified backups are being created
- [ ] Checked for any error messages

## 🆘 Rollback Plan (If Critical Issues)
- [ ] Know how to stop server (close run.bat window)
- [ ] Have Excel templates ready as backup
- [ ] Know location of gst_database.db for emergency access
- [ ] Have my contact details for emergency support

---

## POST-DEPLOYMENT BEST PRACTICES

### Daily (Admin)
- Check dashboard for overdue items
- Review any failed login attempts in logs
- Ensure server is still running

### Weekly (Admin)
- Export Excel backup of all data
- Review preparer productivity
- Check for variance trends

### Monthly (Admin)
- Verify auto-backup file created in backups/ folder
- Archive old data if needed (after FY end)
- Review and optimize allocations for next month

### Quarterly (Admin)
- Change passwords (recommended)
- Review user access (remove inactive users)
- Verify data integrity (random sample checking)

---

**DEPLOYMENT VERIFIED BY:** _________________ Date: _________

**GO-LIVE DECISION:** ☐ APPROVED  ☐ NEEDS MORE TESTING
