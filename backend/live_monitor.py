from scapy.all import sniff, IP, TCP, UDP
import requests
import json
import time

# FastAPI backend manzili
API_URL = "http://localhost:8000/ai/chat"

print("="*50)
print("   NEXURA LIVE NETWORK MONITORING STARTING...")
print("   AI Engine: Random Forest Protection Active")
print("="*50)

def process_packet(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = "TCP" if TCP in packet else "UDP" if UDP in packet else "OTHER"
        size = len(packet)

        # AI ga tahlil uchun so'rov yuboramiz (Simulyatsiya uchun xabar ko'rinishida)
        # Haqiqiy tizimda bu yerda paket xususiyatlari (features) yuboriladi
        payload = f"Network Analysis Request: {proto} packet from {src_ip} size {size} bytes"

        try:
            # Backendga xabar yuboramiz
            response = requests.post(API_URL, json={"text": payload})
            result = response.json()

            if "!!!" in result['response']:
                print(f"[!] XAVF ANIQLANDI: {src_ip} -> {dst_ip} | {result['response']}")
            else:
                print(f"[+] TRAFIK TOZA: {src_ip} -> {dst_ip} | Proto: {proto} | Size: {size}")

        except Exception as e:
            print(f"Backend xatosi: {e}")

# Tarmoqni eshitishni boshlaymiz
try:
    # count=0 cheksiz degani. store=0 xotirani tejash uchun
    sniff(prn=process_packet, store=0)
except Exception as e:
    print(f"Xatolik: {e}")
    print("\nEslatma: Windows-da tarmoqni eshitish uchun Npcap yoki WinPcap o'rnatilgan bo'lishi kerak.")
