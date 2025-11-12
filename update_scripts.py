#!/usr/bin/env python3
"""
Update all script.js files to support both GitHub Pages and local testing.
This adds automatic detection of the environment and generates QR codes accordingly.
"""

import os
import re
from pathlib import Path

# List of events to update (the ones you focus on)
EVENTS = ['hfestJ', 'hfestM', 'hfestOC', 'hfestP', 'hfestSM', 'hfestW']

# Template for the updated script.js
NEW_SCRIPT_TEMPLATE = '''
document.addEventListener("DOMContentLoaded", function () {{
const urlParams = new URLSearchParams(window.location.search);
const odysseyCode = urlParams.get("id");

// Detect if running locally or on GitHub Pages
function getBaseURL() {{
    const hostname = window.location.hostname;
    
    // If on localhost or 127.0.0.1, use local URL
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname.startsWith('192.168.')) {{
        return window.location.protocol + '//' + window.location.host;
    }}
    
    // Otherwise use GitHub Pages URL
    return 'https://cbitosc.github.io/verify25';
}}

// Get the event name from current path
function getEventName() {{
    const path = window.location.pathname;
    const match = path.match(/\\/(hfest[A-Za-z]+)\\//);
    return match ? match[1] : '{event}';
}}

fetch("data.json")
    .then((response) => response.json())
    .then((jsonData) => {{
        const matchingEntry = jsonData.find((entry) => entry.code === odysseyCode);

        if (matchingEntry) {{
            const generalHeader = document.getElementById("general-header");
            generalHeader.classList.add("hidden");

            const nameElement = document.getElementById("name-element");
            nameElement.textContent = `${{matchingEntry.holder}}`;

            const headerNameElement = document.getElementById("header-name-element");
            headerNameElement.textContent = `${{matchingEntry.holder}}`;

            const certHeader = document.getElementById("cert-header");
            const certificate = document.getElementById("certificate");

            certHeader.classList.remove("hidden");
            certificate.classList.remove("hidden");

            const qrContainer = document.getElementById("qr-container");

            // Generate QR code with appropriate URL
            const baseURL = getBaseURL();
            const eventName = getEventName();
            const qrURL = baseURL + '/' + eventName + '/?id=' + matchingEntry.code;

            const qr = new QRCode(qrContainer, {{
                text: qrURL,
                width: 384,
                height: 384,
                typeNumber: 8,
                correctLevel: QRCode.CorrectLevel.H,
                colorDark: "#000000",
                colorLight: "#ffffff"
            }});
            
            console.log('Generated QR for:', qrURL);
        }} else {{
            console.error("No matching entry found for the provided code.");
        }}
    }})
    .catch((error) => console.error("Error loading JSON:", error));
}});
'''

def update_script_file(filepath, event_name):
    """Update a single script.js file"""
    print(f"Updating {filepath}...")
    
    # Create new content with the event name
    new_content = NEW_SCRIPT_TEMPLATE.format(event=event_name)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ Successfully updated")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    docs_dir = Path(__file__).parent / 'docs'
    
    print("=" * 60)
    print("🔄 Updating script.js files for local testing")
    print("=" * 60)
    
    success_count = 0
    
    for event in EVENTS:
        script_path = docs_dir / event / 'script.js'
        
        if script_path.exists():
            if update_script_file(str(script_path), event):
                success_count += 1
        else:
            print(f"⚠️  Not found: {script_path}")
    
    print("=" * 60)
    print(f"✅ Updated {success_count}/{len(EVENTS)} files")
    print("\n📝 Changes made:")
    print("  - Added automatic environment detection")
    print("  - QR codes now point to localhost when testing locally")
    print("  - QR codes point to GitHub Pages when deployed")
    print("\n🚀 The server is now ready for full testing!")
    print("=" * 60)

if __name__ == "__main__":
    main()
