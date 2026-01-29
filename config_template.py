# GST Pro Configuration File
# Rename this to config.py and update values for production

class Config:
    SECRET_KEY = 'your-production-secret-key-here'
    DATABASE = 'gst_database.db'
    BACKUP_DIR = 'backups'
    ARCHIVE_DIR = 'archive'

    # Auto-backup settings
    AUTO_BACKUP_ENABLED = True
    BACKUP_RETENTION_DAYS = 365

    # Session settings
    PERMANENT_SESSION_LIFETIME = 28800  # 8 hours

    # Due date warning threshold (days)
    DUE_DATE_WARNING_DAYS = 3

    # Development vs Production
    DEBUG = False
    TESTING = False
