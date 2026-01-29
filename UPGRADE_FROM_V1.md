# Upgrade Guide: GST Checklist Tool v1 → GST Pro v2.0

## What's New in v2.0

### Major Architecture Changes
- **Role-Based System**: Separate logins for Admin/Reviewer/Preparer
- **Client Allocations**: Assign specific clients to specific preparers
- **Real-time Features**: Auto-save, instant calculations
- **Notification System**: In-app alerts for workflow events
- **Financial Year Support**: View by month or entire FY
- **Excel Export**: One-click report generation
- **Backup System**: Automatic monthly backups

### Data Migration
⚠️ **BREAKING CHANGE**: v2.0 uses a completely new database structure.

**If you have data in v1:**
1. Export your Excel files from v1 before upgrading
2. Install v2.0 fresh (new database)
3. Manually recreate clients (10 minutes)
4. Start using v2.0 for new filings

**Note**: There is no automatic migration path due to schema changes.

### UI Changes
- Modern white-background design (replacing dark theme)
- Mobile-responsive layouts
- Dashboard-based navigation (replacing simple menu)
- Inbox-style review queue for reviewers

### Workflow Changes
- **Locking**: Once ARN entered, data is permanently locked (cannot unlock)
- **Approval Chain**: Draft → Review → Approve → File → Lock
- **Variance Warnings**: Real-time alerts for mismatches
- **GSTR-3B Dependency**: Can only start 3B after GSTR-1 locked

## Installation
Fresh installation recommended:
1. Backup your old folder
2. Extract GST_Pro_v2.zip to new location
3. Follow standard installation in README.md

## Rolling Back
If v2.0 doesn't work for you:
1. Stop v2.0 server (close run.bat)
2. Navigate back to your v1 folder
3. Run v1's run.bat
4. v1 database remains intact in its folder

## Support
For migration assistance, contact your system administrator.
