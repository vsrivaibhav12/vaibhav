# GST Pro Troubleshooting Guide

## Problem: Server running but can't open website

## Step 1: Verify Server is Actually Running

Look at the black Command Prompt window (run.bat):

**✅ GOOD - Should show:**
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.X:5000  (your IP)
Press CTRL+C to quit
```

**❌ BAD - If you see:**
- Window closed immediately → ERROR
- Red error text → ERROR
- Just "Press any key to continue" and closes → ERROR

## Step 2: Check for Common Errors

### Error A: "Address already in use"
**Symptom:** Port 5000 is being used by another program

**Fix:**
1. Close run.bat window
2. Open Task Manager → Find Python processes → End them
3. Or restart computer
4. Run run.bat again

### Error B: "No module named 'flask'"
**Symptom:** Installation didn't complete

**Fix:**
```cmd
python -m pip install flask werkzeug pandas openpyxl
```
Then run run.bat again

### Error C: "sqlite3.OperationalError: unable to open database file"
**Symptom:** Permission denied on folder

**Fix:**
1. Move GST_Pro_v2 folder to Desktop (not in Downloads/Program Files)
2. Right-click run.bat → "Run as Administrator"

### Error D: Window opens then closes immediately
**Symptom:** Crash on startup

**Fix:**
1. Open Command Prompt
2. CD to your GST_Pro_v2 folder
3. Type: python app.py
4. See the actual error message
5. Screenshot it and check below

## Step 3: Test Different URLs

Try ALL of these in your browser:

1. http://localhost:5000
2. http://127.0.0.1:5000
3. http://0.0.0.0:5000
4. http://YOUR_COMPUTER_NAME:5000
   (Find your computer name in System Properties)

**If NONE work:**
→ Server isn't running properly (see Step 2)

**If SOME work:**
→ Firewall/network issue (see Step 4)

## Step 4: Firewall Fix (Most Common Solution)

Windows Defender Firewall is blocking port 5000.

### Manual Fix:
1. Open Windows Security → Firewall & network protection
2. Click "Advanced settings"
3. Click "Inbound Rules" (left panel)
4. Click "New Rule" (right panel)
5. Select "Port" → Next
6. Select "TCP", enter "5000" → Next
7. Select "Allow the connection" → Next
8. Check all three (Domain, Private, Public) → Next
9. Name: "GST Pro Server" → Finish

### Quick Fix (Command Line):
Run Command Prompt as Administrator, paste:
```cmd
netsh advfirewall firewall add rule name="GST Pro" dir=in action=allow protocol=tcp localport=5000
```

## Step 5: Browser Issues

**Try different browsers:**
- Chrome: http://localhost:5000
- Edge: http://localhost:5000
- Firefox: http://localhost:5000

**Clear cache:**
- Press Ctrl+Shift+R (hard refresh)
- Or open Incognito/Private window

## Step 6: Check If Python is Working

Open Command Prompt, type:
```cmd
python --version
```

Should show: Python 3.11.x or 3.12.x or 3.13.x

If error:
→ Python not in PATH (reinstall Python, check "Add to PATH")

## Step 7: Check Port Availability

Open Command Prompt, type:
```cmd
netstat -ano | findstr :5000
```

**If blank:** Port is free (good)
**If shows numbers:** Port is in use
→ Close other apps or change port (see below)

## Step 8: Change Port (if 5000 is blocked)

Edit app.py:
1. Find last line: `app.run(host='0.0.0.0', port=5000, ...)`
2. Change to: `app.run(host='0.0.0.0', port=8080, ...)`
3. Save
4. Access: http://localhost:8080

## Quick Diagnostic Test

Create this file as `test_server.py` in your GST_Pro_v2 folder:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Server is working!</h1><p>If you see this, Flask is installed correctly.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

Run: `python test_server.py`

**If you see "Server is working" in browser:**
→ Problem is with app.py (database or code issue)

**If you still can't connect:**
→ Problem is firewall/port/Python installation

## Emergency: Reset Everything

If nothing works:

1. Restart computer
2. Delete GST_Pro_v2 folder
3. Re-extract ZIP to Desktop
4. Open Command Prompt as Administrator
5. Run:
```cmd
cd Desktop\GST_Pro_v2
python -m pip install --upgrade pip
python -m pip install flask werkzeug pandas openpyxl
python app.py
```

6. Open browser to http://localhost:5000

## Still Not Working?

**Send me:**
1. Screenshot of the black Command Prompt window
2. Screenshot of browser error
3. Windows version (Win+R → type `winver`)
4. Python version (python --version)

**Common Quick Fixes:**
→ Move folder to Desktop (not Downloads or Program Files)
→ Disable antivirus temporarily (test if it works)
→ Make sure no VPN is active
→ Check if company firewall blocking (if office network)
