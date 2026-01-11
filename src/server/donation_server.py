"""
HTTP Server for Overlay
Uses simple HTTP server compatible with Qt threading
"""

import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable, Optional, Dict, Any
from datetime import datetime
from urllib.parse import parse_qs, urlparse
import queue


# Thread-safe event storage
class EventStore:
    """Thread-safe storage for current donation event"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._current_event: Optional[Dict] = None
        self._current_theme: Dict = {}
        self._event_id: int = 0
        self._last_event_time: float = 0
    
    def set_event(self, event: Dict, theme: Dict):
        with self._lock:
            self._current_event = event
            self._current_theme = theme
            self._event_id += 1
            self._last_event_time = time.time()
    
    def get_event(self) -> tuple:
        with self._lock:
            return self._current_event, self._current_theme, self._event_id, self._last_event_time
    
    def clear_event(self):
        with self._lock:
            self._current_event = None


# Global event store
_event_store = EventStore()
_donation_callback: Optional[Callable[[Dict], None]] = None


def _create_overlay_html() -> str:
    """Generate the overlay HTML page with polling support"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StreamAlerts Overlay</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: transparent;
            font-family: 'Segoe UI', system-ui, sans-serif;
            overflow: hidden;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding-top: 50px;
        }
        
        .alert-container {
            position: relative;
            width: 500px;
            opacity: 0;
            transform: translateY(-50px) scale(0.9);
            transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            pointer-events: none;
        }
        
        .alert-container.visible {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
        
        .alert-container.exit {
            opacity: 0;
            transform: translateY(-30px) scale(0.95);
        }
        
        .alert-card {
            background: linear-gradient(135deg, var(--bg-color, #1a1a2e) 0%, var(--bg-secondary, #2a2a4e) 100%);
            border-radius: var(--border-radius, 16px);
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5),
                        0 0 var(--glow-size, 20px) var(--glow-color, #00d9ff);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
            text-align: center;
        }
        
        .alert-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color, #00d9ff), var(--secondary-color, #ff6b6b), var(--primary-color, #00d9ff));
            background-size: 200% 100%;
            animation: shimmer 2s infinite linear;
        }
        
        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        .donation-icon {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, var(--primary-color, #00d9ff), var(--secondary-color, #ff6b6b));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            animation: pulse 2s infinite;
            font-size: 32px;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 217, 255, 0.4); }
            50% { transform: scale(1.05); box-shadow: 0 0 20px 10px rgba(0, 217, 255, 0.2); }
        }
        
        .sender-name {
            font-size: var(--font-sender, 28px);
            font-weight: 600;
            color: var(--text-color, #ffffff);
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        .amount {
            font-size: var(--font-amount, 48px);
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color, #00d9ff), var(--accent-color, #ffd93d));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            animation: glow-text 2s infinite alternate;
        }
        
        @keyframes glow-text {
            0% { filter: drop-shadow(0 0 5px var(--primary-color, #00d9ff)); }
            100% { filter: drop-shadow(0 0 15px var(--primary-color, #00d9ff)); }
        }
        
        .message {
            font-size: var(--font-message, 18px);
            color: rgba(255, 255, 255, 0.85);
            line-height: 1.5;
            padding: 15px 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            border-left: 4px solid var(--primary-color, #00d9ff);
            text-align: left;
        }
        
        .particles {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            pointer-events: none;
            overflow: hidden;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            width: 8px;
            height: 8px;
            background: var(--primary-color, #00d9ff);
            border-radius: 50%;
            opacity: 0.6;
            animation: sparkle 1.5s ease-in-out infinite;
        }
        
        @keyframes sparkle {
            0%, 100% { opacity: 0; transform: scale(0); }
            50% { opacity: 0.8; transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="alert-container" id="alertContainer">
        <div class="particles" id="particles"></div>
        <div class="alert-card">
            <div class="donation-icon">💰</div>
            <div class="sender-name" id="senderName">Donor Name</div>
            <div class="amount" id="amount">₹0</div>
            <div class="message" id="message">Thank you for your donation!</div>
        </div>
    </div>
    
    <script>
        const container = document.getElementById('alertContainer');
        const senderEl = document.getElementById('senderName');
        const amountEl = document.getElementById('amount');
        const messageEl = document.getElementById('message');
        
        let lastEventId = 0;
        let hideTimeout = null;
        
        function applyTheme(theme) {
            if (!theme) return;
            const root = document.documentElement;
            root.style.setProperty('--bg-color', theme.background_color || '#1a1a2e');
            root.style.setProperty('--bg-secondary', adjustColor(theme.background_color || '#1a1a2e', 20));
            root.style.setProperty('--primary-color', theme.primary_color || '#00d9ff');
            root.style.setProperty('--secondary-color', theme.secondary_color || '#ff6b6b');
            root.style.setProperty('--accent-color', theme.accent_color || '#ffd93d');
            root.style.setProperty('--text-color', theme.text_color || '#ffffff');
            root.style.setProperty('--border-radius', (theme.border_radius || 16) + 'px');
            root.style.setProperty('--font-sender', (theme.font_size_sender || 28) + 'px');
            root.style.setProperty('--font-amount', (theme.font_size_amount || 48) + 'px');
            root.style.setProperty('--font-message', (theme.font_size_message || 18) + 'px');
            root.style.setProperty('--glow-color', theme.glow_enabled !== false ? (theme.glow_color || '#00d9ff') : 'transparent');
            root.style.setProperty('--glow-size', theme.glow_enabled !== false ? (theme.glow_intensity || 20) + 'px' : '0');
            if (theme.font_family) document.body.style.fontFamily = theme.font_family;
        }
        
        function adjustColor(color, percent) {
            const num = parseInt(color.replace('#', ''), 16);
            const amt = Math.round(2.55 * percent);
            const R = Math.min(255, (num >> 16) + amt);
            const G = Math.min(255, ((num >> 8) & 0x00FF) + amt);
            const B = Math.min(255, (num & 0x0000FF) + amt);
            return '#' + (0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1);
        }
        
        function formatAmount(amount, currency) {
            const symbols = { 'INR': '₹', 'USD': '$', 'EUR': '€', 'GBP': '£' };
            return (symbols[currency] || currency) + amount.toLocaleString();
        }
        
        function showAlert(event, theme, duration) {
            if (hideTimeout) clearTimeout(hideTimeout);
            
            applyTheme(theme);
            senderEl.textContent = event.sender || 'Anonymous';
            amountEl.textContent = formatAmount(event.amount || 0, event.currency || 'INR');
            messageEl.textContent = event.message || 'Thank you for your support!';
            
            createParticles(theme?.primary_color || '#00d9ff');
            
            container.classList.remove('exit');
            container.classList.add('visible');
            
            hideTimeout = setTimeout(() => {
                container.classList.add('exit');
                setTimeout(() => container.classList.remove('visible', 'exit'), 500);
            }, (duration || 5) * 1000);
        }
        
        function createParticles(color) {
            const p = document.getElementById('particles');
            p.innerHTML = '';
            for (let i = 0; i < 12; i++) {
                const d = document.createElement('div');
                d.className = 'particle';
                d.style.cssText = `left:${Math.random()*100}%;top:${Math.random()*100}%;background:${color};animation-delay:${Math.random()*1.5}s`;
                p.appendChild(d);
            }
        }
        
        async function pollForEvents() {
            try {
                const res = await fetch('/current');
                const data = await res.json();
                if (data.event && data.event_id > lastEventId) {
                    lastEventId = data.event_id;
                    showAlert(data.event, data.theme, data.theme?.display_duration || 5);
                }
            } catch (e) {}
            setTimeout(pollForEvents, 500);
        }
        
        pollForEvents();
    </script>
</body>
</html>'''


class DonationHandler(BaseHTTPRequestHandler):
    """HTTP request handler for donation server"""
    
    def log_message(self, format, *args):
        pass  # Suppress logging
    
    def _send_json_response(self, data: dict, status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_html_response(self, html: str):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/health':
            self._send_json_response({
                "status": "ok",
                "timestamp": datetime.now().isoformat(),
                "server": "StreamAlerts Donation Server"
            })
        elif path == '/current':
            event, theme, event_id, _ = _event_store.get_event()
            self._send_json_response({
                "event": event,
                "theme": theme,
                "event_id": event_id
            })
        elif path == '/status':
            self._send_json_response({
                "server_running": True,
                "message": "StreamAlerts is running"
            })
        else:
            self._send_json_response({"error": "Not found"}, 404)
    
    def do_POST(self):
        path = urlparse(self.path).path
        
        if path == '/donation':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body) if body else {}
                
                if "sender" not in data or "amount" not in data:
                    self._send_json_response({"error": "Missing required fields"}, 400)
                    return
                
                if "timestamp" not in data:
                    data["timestamp"] = datetime.now().isoformat()
                if "currency" not in data:
                    data["currency"] = "INR"
                
                if _donation_callback:
                    _donation_callback(data)
                
                self._send_json_response({"status": "received", "event": data})
            except Exception as e:
                self._send_json_response({"error": str(e)}, 500)
        
        elif path == '/donation/test':
            test_data = {
                "sender": "Test Donor",
                "amount": 100,
                "currency": "INR",
                "message": "Test donation!",
                "timestamp": datetime.now().isoformat()
            }
            if _donation_callback:
                _donation_callback(test_data)
            self._send_json_response({"status": "test_sent", "event": test_data})
        else:
            self._send_json_response({"error": "Not found"}, 404)


class OverlayHandler(BaseHTTPRequestHandler):
    """HTTP request handler for overlay server"""
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(_create_overlay_html().encode())
        
        elif path == '/current':
            event, theme, event_id, _ = _event_store.get_event()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "event": event,
                "theme": theme,
                "event_id": event_id
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()


class DonationServer:
    """HTTP Server for receiving donations and serving overlay"""
    
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8765,
        overlay_port: int = 8080,
        on_donation: Optional[Callable[[dict], None]] = None,
        overlay_dir: Optional[str] = None
    ):
        global _donation_callback
        
        self._host = host
        self._port = port
        self._overlay_port = overlay_port
        self._on_donation = on_donation
        _donation_callback = on_donation
        
        self._donation_server: Optional[HTTPServer] = None
        self._overlay_server: Optional[HTTPServer] = None
        self._donation_thread: Optional[threading.Thread] = None
        self._overlay_thread: Optional[threading.Thread] = None
        self._running = False
    
    def set_on_donation_callback(self, callback: Callable[[dict], None]):
        global _donation_callback
        self._on_donation = callback
        _donation_callback = callback
    
    def broadcast_donation(self, event: dict, theme: dict):
        """Broadcast donation to overlay (via polling)"""
        _event_store.set_event(event, theme)
    
    def update_theme(self, theme: dict):
        """Update theme for next broadcast"""
        current_event, _, _, _ = _event_store.get_event()
        if current_event:
            _event_store.set_event(current_event, theme)
    
    def start(self):
        """Start both servers"""
        if self._running:
            return
        
        self._running = True
        
        # Start donation server
        self._donation_server = HTTPServer((self._host, self._port), DonationHandler)
        self._donation_thread = threading.Thread(
            target=self._donation_server.serve_forever,
            daemon=True
        )
        self._donation_thread.start()
        
        # Start overlay server
        self._overlay_server = HTTPServer((self._host, self._overlay_port), OverlayHandler)
        self._overlay_thread = threading.Thread(
            target=self._overlay_server.serve_forever,
            daemon=True
        )
        self._overlay_thread.start()
        
        print(f"Donation server started on http://{self._host}:{self._port}")
        print(f"Overlay server started on http://{self._host}:{self._overlay_port}")
    
    def stop(self):
        """Stop all servers"""
        self._running = False
        if self._donation_server:
            self._donation_server.shutdown()
        if self._overlay_server:
            self._overlay_server.shutdown()
    
    @property
    def is_running(self) -> bool:
        return self._running
    
    @property
    def donation_url(self) -> str:
        return f"http://{self._host}:{self._port}/donation"
    
    @property
    def overlay_url(self) -> str:
        return f"http://{self._host}:{self._overlay_port}"
