# GST Pro v2.0 - Advanced GST Compliance System

## 🎯 What Is This?
**GST Pro** is an enterprise-grade GST filing management system designed for Chartered Accountants and tax practitioners. It replaces Excel-based tracking with a secure, workflow-driven platform featuring real-time calculations, role-based access, and comprehensive compliance monitoring.

**Key Differentiators:**
- ✅ GSTR-1 & GSTR-3B workflow with approval chains
- ✅ Real-time auto-save and instant variance calculations
- ✅ Client-specific preparer allocations (separate for GSTR-1 & 3B)
- ✅ Financial Year/Monthly view toggles
- ✅ Automated due date alerts
- ✅ Excel export for all reports
- ✅ Monthly auto-backup and FY archival

---

## 💻 System Requirements

### Server (Main Computer)
- **OS**: Windows 10/11 (64-bit) / Linux / macOS
- **RAM**: 4GB+ recommended
- **Python**: 3.11 or higher
- **Network**: Ethernet/WiFi connection (for LAN access)
- **Always On**: Must remain running during office hours

### Client Computers
- Any device with Chrome/Firefox/Safari/Edge
- Must be on same office network (LAN)

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Install Python
1. Visit https://python.org/downloads
2. Download Python 3.11+ Windows installer (64-bit)
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"

### Step 2: Install GST Pro
1. Extract `GST_Pro_v2.zip` to Desktop (or any folder)
2. Double-click `install.bat`
3. Wait for installation to complete
4. Close the window when you see "Installation Successful"

### Step 3: Start Server
1. Double-click `run.bat`
2. Black window appears showing "Running on http://0.0.0.0:5000"
3. **Keep this window open!** Minimize it, but don't close.

### Step 4: Access From Any Computer
**On Server:** Open browser → `http://localhost:5000`

**On Other Computers:**
1. Find Server IP:
   - On server, press `Win+R`
   - Type `cmd` → Enter
   - Type `ipconfig` → Enter
   - Note "IPv4 Address" (e.g., `192.168.1.100`)
2. Open browser → `http://192.168.1.100:5000`

---

## 🔐 First Login & Security Setup

### Default Credentials
- **Username**: `admin`
- **Password**: `admin123`

### IMMEDIATE ACTIONS REQUIRED:
1. Login as admin
2. Go to **Admin Panel** (top menu)
3. Click **"+ Add User"**
4. Create your own admin account
5. Logout → Login with new account
6. Go back to Admin Panel → Find "admin" → Click **Deactivate** (or delete)

---

## 👥 User Roles Explained

### 🔴 Administrator (You/Partner)
**Access:** Full system control
- Create/manage users (preparers, reviewers)
- Allocate clients to specific preparers
- View all reports and dashboards
- Archive financial year data
- Toggle between Monthly/FY views
- Reset user passwords

### 🟡 Reviewer (Senior CA/Manager)
**Access:** Review and approval only
- **Inbox Dashboard**: Shows all items submitted for review
- Can approve or send back with comments
- Cannot edit numbers once submitted
- Can file returns with ARN (if authorized)

### 🟢 Preparer (Junior Staff)
**Access:** Data entry only
- My Work Dashboard: Shows only assigned clients
- Real-time data entry with auto-save
- Checklist items with timestamps
- Can submit for review (must select reviewer)
- **Cannot edit after submission** unless sent back

---

## 📊 Workflow Walkthrough

### Typical GSTR-1 Process:

**Day 1-5 (Preparer):**
1. Login → My Work Dashboard
2. See current month (auto-calculated: Previous calendar month)
3. Click client → GSTR-1 Form opens
4. Tick checklist items (auto-timestamped)
5. Enter sales data (B2B, B2C, notes)
6. Variance auto-calculates immediately
7. Select reviewer from dropdown
8. Click "Submit for Review"

**Day 6 (Reviewer):**
1. Login → Review Dashboard (Inbox style)
2. See submitted item
3. Click to review data
4. If correct → "Approve for Filing"
5. If issues → "Send Back" with comments

**Day 7 (Preparer):**
1. See notification of approval
2. Generate JSON from GST Portal
3. Upload to actual GST Website
4. Get ARN Number
5. Return to system → Enter ARN
6. Click "File & Lock" → Record frozen permanently

**Day 8+ (Preparer/Other):**
1. Now GSTR-3B available (only after GSTR-1 locked)
2. Auto-imports GSTR-1 data
3. Enter ITC details, match with 2B
4. Submit for review → Approve → File → Lock

---

## 📋 Feature Deep Dive

### 1. Real-Time Auto-Save
- **No "Save" button needed**
- Data saves automatically 1.5 seconds after you stop typing
- Green "Saved" indicator appears bottom-right
- Prevents data loss from browser crashes

### 2. Client Allocations
- Admin allocates specific clients to specific preparers
- GSTR-1 and GSTR-3B can have **different preparers**
- Preparers only see their assigned clients on dashboard
- Allocations can be changed month-to-month

### 3. Financial Year Management
- **Auto-calculation**: If today is Jan 29, 2026 → Current month is Dec 2025
- **FY View**: Toggle in Admin Reports shows Apr 2025 - Mar 2026
- **Due Date Alerts**: Red warnings for overdue filings
- **Automatic transition**: No manual month selection needed (but option available)

### 4. Variance Detection
- **GSTR-1**: Highlights if return total ≠ Tally/books total
- **GSTR-3B**: Compares 3B taxable value with GSTR-1 auto-import
- Prevents mismatches before filing

### 5. Comprehensive 3B Calculations
| Input Section | Fields |
|--------------|--------|
| GSTR-2B Values | TV, CGST, SGST, IGST |
| Tally Books | TV, CGST, SGST, IGST |
| Ineligible ITC | CGST, SGST, IGST (Section 17 blocked) |
| RCM ITC | CGST, SGST, IGST (Reverse Charge Mechanism) |
| Interest & Fees | CGST, SGST, IGST Interest + Late Fee |
| **Auto-Calculated** | Eligible ITC, Net Liability, Payable/Carry Forward |

### 6. Notification System
- Bell icon 🔔 in top bar shows unread count
- Automatic notifications for:
  - New assignment received
  - Submission received for review
  - File approved/returned
  - Due date warnings (3 days before)

### 7. Reports & Analytics
**Available to Admin:**
- Monthly compliance status
- Financial Year overview
- Client-wise detailed status
- Pie charts (Filed vs Pending)
- **One-click Excel export** of all data
- Overdue alerts

### 8. Backup & Archival
- **Monthly Auto-Backup**: Creates `backups/gst_backup_YYYYMM.db`
- **FY Archival**: Move completed year to separate file
- **Data Safety**: Simply copy `gst_database.db` file for backup

---

## 🛠️ Troubleshooting

### Cannot access from other computers
1. Check Windows Firewall:
   - Open Control Panel → Windows Defender Firewall
   - Advanced Settings → Inbound Rules
   - New Rule → Port → TCP → 5000 → Allow
2. Ensure all computers on same WiFi/Network
3. Verify correct IP address (`ipconfig`)

### Python not found error
- Reinstall Python
- **Must check**: "Add Python to PATH"
- Restart computer after installation

### Changes not saving
- Check if record is locked (ARN entered)
- Verify preparer is assigned to that client
- Check network connection to server

### Forgot admin password
- Stop server (close run.bat window)
- Delete `gst_database.db` file
- Restart server → Default admin restored (admin/admin123)
- **Warning**: This deletes all data! Keep regular backups.

---

## 🚀 Advanced Tips

### Shortcut Commands
- **Current Month Auto-Logic**: System always assumes you're filing for previous calendar month
- **Quick Switch**: Preparer dashboard has Month/Year dropdown to file backlog
- **Bulk Export**: In Reports, select Financial Year view → Export Excel for entire year data
- **Variance Check**: If variance not zero, hover over number to see breakdown

### Best Practices
1. **Allocate clients immediately** when month starts
2. **Submit for review** at least 3 days before actual due date
3. **Check notifications daily** for updates
4. **Export Excel backup** before archiving a FY
5. **Assign separate preparers** for GSTR-1 and 3B if workload is high

### Security Checklist
- [ ] Changed default admin password day 1
- [ ] Created separate admin account for each partner
- [ ] Each preparer has unique login (no sharing)
- [ ] Deactivated users when staff leaves
- [ ] Regular backup of gst_database.db to USB/Cloud

---

## 📞 Support & Development

**This is custom-built software for your practice.**

**Version**: 2.0 Pro
**Architecture**: Flask + SQLite + Pandas
**Best For**: CA offices with 5-50 clients, 3-20 staff members
**Scalability**: Supports 1000+ clients easily

**Data Location**: All data stored locally in `gst_database.db` (SQLite)
**Remote Access**: Use VPN or TeamViewer to access server if working from home
**Updates**: Contact your developer for feature additions

---

## 🎓 Training Outline (For New Staff)

### For Preparers (30 min training):
1. Login with your username
2. Dashboard shows ONLY your clients
3. Click client → Tick checklist → Enter data
4. Watch variance number (should be 0)
5. Submit for review (select CA name)

### For Reviewers (15 min training):
1. Check Review Dashboard daily
2. Click pending items
3. Verify taxable values match supporting
4. Approve or type reason for rejection

### For Admin (1 hour training):
1. Create users in Admin Panel
2. Allocate clients (separate GSTR-1 and 3B prep)
3. Run reports monthly
4. Archive FY after March
5. Backup database file

---

**Built for compliance. Designed for efficiency.**

*GST Pro v2.0 - Making GST filing bulletproof*
