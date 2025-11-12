# Local Testing Guide for verify25

## Quick Start (Windows)

### Option 1: Double-Click Start (Easiest)
1. Double-click **`start-server.bat`** in the project root
2. A terminal will open showing the server URL
3. Open your browser and visit: **`http://localhost:8000/docs/`**

### Option 2: Command Line
1. Open PowerShell in the project directory
2. Run:
   ```powershell
   python server.py
   ```
3. Visit **`http://localhost:8000/docs/`**

## Testing the Verification System

### 1. Check Available Codes
Before testing, check what participant codes are available in the data files:
- `docs/hfestJ/data.json`
- `docs/hfestM/data.json`
- `docs/hfestOC/data.json`
- `docs/hfestP/data.json`
- `docs/hfestSM/data.json`
- `docs/hfestW/data.json`

### 2. Test URLs
Use one of these formats with an actual code from the JSON file:

```
http://localhost:8000/docs/hfestJ/?id=CODE
http://localhost:8000/docs/hfestM/?id=CODE
http://localhost:8000/docs/hfestOC/?id=CODE
http://localhost:8000/docs/hfestP/?id=CODE
http://localhost:8000/docs/hfestSM/?id=CODE
http://localhost:8000/docs/hfestW/?id=CODE
```

**Example:**
```
http://localhost:8000/docs/hfestJ/?id=abc123
```

### 3. QR Code Testing
Once the server is running, you can:
1. Generate QR codes that point to `http://localhost:8000/docs/hfestJ/?id=CODE` etc.
2. Scan the QR codes with your phone/device
3. Your device should connect to `localhost:8000` if on the same network, or you can test on the same computer

## How It Works

The verification system:
1. Reads the `?id=CODE` parameter from the URL
2. Looks up the code in `data.json`
3. If found, displays the certificate with participant details
4. Generates a QR code for that certificate

## Troubleshooting

### Port 8000 already in use
If you get "Address already in use" error:
- Edit `server.py` and change `PORT = 8000` to `PORT = 8001` (or another number)
- Update test URLs accordingly

### Can't access from phone on same network
You need your computer's IP address:
1. Open PowerShell and run: `ipconfig`
2. Look for "IPv4 Address" (usually `192.168.x.x`)
3. Use: `http://YOUR_IP:8000/docs/hfestJ/?id=CODE`

### Files show old content
The server automatically prevents caching, so refresh your browser (Ctrl+F5) to see changes.

## Switching Back to GitHub Pages

Simply visit: `https://cbitosc.github.io/verify25/`

All URLs will work the same way as the local version.
