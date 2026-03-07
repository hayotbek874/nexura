import socket
import requests
import ssl
from urllib.parse import urlparse

def analyze_target(target):
    """Domen yoki IP manzilli tahlil qiladi"""
    report = []
    
    # 1. IP Manzilni aniqlash
    try:
        domain = urlparse(target).netloc if "://" in target else target
        ip_addr = socket.gethostbyname(domain)
        report.append(f"Target Resolved: {ip_addr}")
    except:
        return "!!! XATOLIK: Domen yoki IP topilmadi."

    # 2. Muhim portlarni tekshirish (Common Ports)
    ports = [21, 22, 80, 443, 3306, 8080]
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip_addr, port))
        if result == 0:
            open_ports.append(str(port))
        sock.close()
    
    if open_ports:
        report.append(f"Ochiq portlar aniqlandi: {', '.join(open_ports)}")
    
    # 3. HTTP Header Tahlili (Agar veb-sayt bo'lsa)
    if not target.startswith("http"):
        target = "https://" + target
        
    try:
        response = requests.get(target, timeout=5)
        headers = response.headers
        
        missing_headers = []
        if 'Content-Security-Policy' not in headers: missing_headers.append("CSP")
        if 'X-Frame-Options' not in headers: missing_headers.append("X-Frame")
        
        if missing_headers:
            report.append(f"Xavfsizlik kamchiliklari: {', '.join(missing_headers)} sarlavhalari yo'q.")
    except:
        report.append("Veb-server tahlili o'tkazib bo'lmadi.")

    return " | ".join(report)
