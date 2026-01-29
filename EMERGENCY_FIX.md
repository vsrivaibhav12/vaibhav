
# IMMEDIATE WINDOW CLOSE - Emergency Fix

## Step 1: See the Actual Error

The window is closing too fast to see the error. Let's capture it:

### Method A: Command Prompt (Recommended)
1. Press `Win + R` (Run dialog)
2. Type `cmd` and press Enter
3. Type this (replace path with your actual location):
```cmd
cd C:\Users\welcome\Desktop\GST_Pro_v2
```
Or if in Downloads:
```cmd
cd C:\Users\welcome\Downloads\GST_Pro_v2
```
4. Then type:
```cmd
python app.py
```
5. **Now you'll see the error message that doesn't disappear!**
6. Take a screenshot or copy the text

### Method B: Modified run.bat
1. Right-click `run.bat` → Edit
2. At the end, add a new line:
```
pause
```
3. Save
4. Double-click run.bat again
5. Now window stays open showing error

## Common Errors & Fixes

### Error 1: "No module named 'flask'"
**Cause:** Packages didn't install properly

**Fix:**
```cmd
python -m pip install flask werkzeug pandas openpyxl
```
Then try again.

### Error 2: "sqlite3.OperationalError: unable to open database file"
**Cause:** Folder permissions (usually in Downloads/Program Files)

**Fix:**
1. Move GST_Pro_v2 folder to **Desktop**
2. Run from Desktop

### Error 3: "Permission denied"
**Cause:** Need administrator rights

**Fix:**
Right-click on app.py → Open with → Python (make sure it's the one you installed)
OR
Move folder to Desktop

### Error 4: "Address already in use"
**Cause:** Another program using port 5000

**Fix:**
1. Restart computer
2. Or change port: Edit app.py, find `port=5000`, change to `port=8080`

### Error 5: "ModuleNotFoundError: No module named 'pandas'"
**Cause:** Pandas didn't install (Python 3.13 issue we fixed earlier)

**Fix:**
```cmd
python -m pip install pandas==2.2.3
```

## I Can't See Any Error Text

If you type `python app.py` and it just returns to prompt with no error:

**Problem:** Python not in PATH
**Fix:**
1. Find where you installed Python
   Usually: `C:\Users\welcome\AppData\Local\Programs\Python\Python313`
2. Use full path:
```cmd
"C:\Users\welcome\AppData\Local\Programs\Python\Python313\python.exe" app.py
```

## Quick Check: Is Flask Installed?

Type this in Command Prompt:
```cmd
python -c "import flask; print('Flask OK')"
```

**If says "Flask OK"** → Flask installed, different problem
**If error** → Flask not installed

To install Flask:
```cmd
python -m pip install flask
```

## Still Not Working?

Send me the EXACT error message from Step 1 (Method A)

Common patterns:
- "ModuleNotFoundError" → Need to install packages
- "PermissionError" → Move folder to Desktop
- "Address already in use" → Port 5000 busy
- "SyntaxError" → File got corrupted, re-download ZIP
