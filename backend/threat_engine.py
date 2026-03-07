import os
import pandas as pd
import joblib
import glob

class NexuraThreatEngine:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.models = {}
        self.malware_db = None
        self.is_ready = False

    def initialize(self):
        print("[DATABASE] Tahdidlar bazasi yuklanmoqda...")
        
        # 1. ML Modellarni yuklash (.pkl)
        model_files = glob.glob(os.path.join(self.data_dir, "*.pkl"))
        for f in model_files:
            name = os.path.basename(f).replace(".pkl", "")
            try:
                self.models[name] = joblib.load(f)
                print(f"   > Model yuklandi: {name}")
            except:
                print(f"   ! Xato: {name} yuklanmadi.")

        # 2. Malware CSV bazasini indekslash
        csv_files = glob.glob(os.path.join(self.data_dir, "CTU-IoT-Malware*.csv"))
        if csv_files:
            print(f"[DATABASE] {len(csv_files)} ta malware loglari topildi. Indekslanmoqda...")
            # Xotirani tejash uchun faqat kerakli ustunlarni yuklaymiz (masalan IP va Label)
            temp_list = []
            for f in csv_files[:5]: # Dastlabki 5 tasini yuklaymiz (tezlik uchun)
                try:
                    df = pd.read_csv(f, usecols=lambda x: x in ['id.resp_h', 'label', 'tunnel_parents'], low_memory=False)
                    temp_list.append(df)
                except: continue
            if temp_list:
                self.malware_db = pd.concat(temp_list, ignore_index=True)
                print(f"   > {len(self.malware_db)} ta tahdid belgisi bazaga qo'shildi.")
        
        self.is_ready = True
        print("[DATABASE] NEXURA DB ONLINE.")

    def scan_ip(self, ip):
        """IP manzilni malware bazasidan qidirish."""
        if self.malware_db is not None:
            match = self.malware_db[self.malware_db['id.resp_h'] == ip]
            if not match.empty:
                return f"⚠️ TAHID ANIQLANDI: Ushbu IP malware bazasida mavjud! Label: {match.iloc[0]['label']}"
        return "✅ TOZA: Malware bazasida topilmadi."

# Singleton obyekt
engine = NexuraThreatEngine(os.path.dirname(os.path.abspath(__file__)))
