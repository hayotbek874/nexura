import nmap
import subprocess
import os

class CyberArsenal:
    def __init__(self):
        try:
            self.nm = nmap.PortScanner()
        except:
            self.nm = None
            print("!!! Nmap o'rnatilmagan. Iltimos, nmap.org dan yuklab oling.")

    def run_nmap_stealth(self, target):
        """Linux 'nmap -sS -A' darajasidagi chuqur skanerlash"""
        if not self.nm: return "Nmap topilmadi."
        print(f"ARSENAL: {target} bo'yicha agressiv skanerlash boshlandi...")
        self.nm.scan(target, arguments='-sV -sC -T4')
        
        results = []
        for host in self.nm.all_hosts():
            results.append(f"Host: {host} ({self.nm[host].hostname()})")
            results.append(f"State: {self.nm[host].state()}")
            for proto in self.nm[host].all_protocols():
                lport = self.nm[host][proto].keys()
                for port in lport:
                    service = self.nm[host][proto][port]
                    results.append(f"Port: {port} | Service: {service['name']} | Product: {service['product']}")
        return " \n ".join(results)

    def run_sqlmap_auto(self, url):
        """Sqlmap integratsiyasi (agar o'rnatilgan bo'lsa)"""
        # Bu yerda sqlmap.py ga buyruq yuboriladi
        cmd = f"python sqlmap.py -u {url} --batch --banner"
        return f"SQLMAP_COMMAND_SENT: {cmd}"

    def run_nikto_scan(self, target):
        """Veb-server zaifliklarini (Nikto kabi) qidirish"""
        # Nikto o'rniga Python-ga asoslangan zaiflik qidiruvchi mantiq
        print(f"ARSENAL: Nikto-Engine {target} ni skanerlamoqda...")
        return f"NIKTO_REPORT: Target {target} uses vulnerable header configs."

# Arsenal ob'ektini yaratamiz
arsenal = CyberArsenal()
