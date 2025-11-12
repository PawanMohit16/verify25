#!/usr/bin/env python3
"""
Simple HTTP server for testing verify25 locally
Run: python server.py
Then visit: http://localhost:8000/docs/
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000
DOCS_DIR = os.path.join(os.path.dirname(__file__), 'docs')

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOCS_DIR, **kwargs)
    
    def translate_path(self, path):
        """
        Translate a /-separated PATH to the local filename syntax.
        Components that mean special things to the OS are replaced with
        underscores. This function also handles case-insensitive lookups.
        """
        # Use the parent's translate_path but make it case-insensitive
        path = super().translate_path(path)
        
        # If the file doesn't exist exactly, try to find it case-insensitively
        if not os.path.exists(path):
            # Get the directory and filename
            directory = os.path.dirname(path)
            filename = os.path.basename(path)
            
            if os.path.exists(directory):
                # List files in directory and find case-insensitive match
                try:
                    files = os.listdir(directory)
                    for f in files:
                        if f.lower() == filename.lower():
                            path = os.path.join(directory, f)
                            break
                except OSError:
                    pass
        
        return path
    
    def end_headers(self):
        # Add headers to prevent caching during development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

def start_server():
    handler = MyHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("=" * 60)
        print("🚀 Local Server Started!")
        print("=" * 60)
        print(f"📍 Server running at: http://localhost:{PORT}/")
        print(f"\n🔗 Test URLs for hfest events:")
        print(f"  - hfestJ: http://localhost:{PORT}/hfestJ/?id=<CODE>")
        print(f"  - hfestM: http://localhost:{PORT}/hfestM/?id=<CODE>")
        print(f"  - hfestOC: http://localhost:{PORT}/hfestOC/?id=<CODE>")
        print(f"  - hfestP: http://localhost:{PORT}/hfestP/?id=<CODE>")
        print(f"  - hfestSM: http://localhost:{PORT}/hfestSM/?id=<CODE>")
        print(f"  - hfestW: http://localhost:{PORT}/hfestW/?id=<CODE>")
        print(f"\n💡 Replace <CODE> with an actual ID from data.json")
        print(f"🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        httpd.serve_forever()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped.")
    except OSError as e:
        print(f"❌ Error: {e}")
        if "Address already in use" in str(e):
            print(f"   Port {PORT} is already in use. Try closing other applications or use a different port.")
