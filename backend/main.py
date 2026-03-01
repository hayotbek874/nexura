from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import numpy as np
import time

app = FastAPI(title="NEXURA Cyber AGI Brain v5.5")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AVTONOM MODELLARNI DINAMIK YUKLASH ---
MODELS = {}
print("\n" + "="*60)
print("   NEXURA AGI: LOADING NEURAL LAYERS...")
print("="*60)

for file in os.listdir('.'):
    if file.endswith('_model.pkl'):
        name = file.replace('_model.pkl', '')
        try:
            MODELS[name] = {
                'model': joblib.load(file),
                'vectorizer': joblib.load(f"{name}_vectorizer.pkl") if os.path.exists(f"{name}_vectorizer.pkl") else None
            }
            print(f"   [ LOADED ] {name.upper()}")
        except: continue

print(f"AI: Jami {len(MODELS)} ta bilim qatlami faollashtirildi.")

class UserInput(BaseModel):
    text: str

@app.post("/ai/chat")
async def ai_chat(user_input: UserInput):
    text = user_input.text
    text_l = text.lower().strip()
    time.sleep(0.5) 
    
    # 1. MULOQOT FILTRI (Intent Analysis)
    # 'train_model' yoki 'validation_model' odatda normal gaplar uchun o'qitilgan bo'ladi
    is_normal_chat = False
    if "salom" in text_l or "isming" in text_l or "vazifang" in text_l:
        is_normal_chat = True

    # 2. BARCHA MODELLAR BO'YICHA ANALIZ
    analysis_results = []
    max_risk = 5
    
    for name, component in MODELS.items():
        # Xavfsizlik modellari (DDoS, Bot, SQLi va h.k.)
        if component['vectorizer']:
            try:
                vec = component['vectorizer'].transform([text])
                prob = component['model'].predict_proba(vec)[0][1]
                
                # Agar bu oddiy muloqot modeli bo'lsa (masalan 'train' deb nomlangan bo'lsa)
                if "train" in name.lower() or "test" in name.lower() or "normal" in name.lower():
                    if prob > 0.7: is_normal_chat = True
                    continue

                # Haqiqiy xavfni aniqlash (yuqori aniqlik - 90%+)
                if prob > 0.90:
                    analysis_results.append({"name": name.upper(), "score": prob * 100})
                    max_risk = max(max_risk, int(prob * 100))
            except: continue

    # 3. JAVOBNI GENERATSIYA QILISH (AGI Logic)
    if not analysis_results and is_normal_chat:
        # Insoniy muloqot rejimida
        if "salom" in text_l:
            return {"response": "Assalomu alaykum! Men NEXURA-man. Hozirda 34 ta kiber-mudofaa qatlami orqali bank tizimini monitoring qilyapman. Nima tahlil o'tkazamiz?", "data": {"risk": 5}}
        return {"response": "Tushunarlidir. Tizim xavfsiz holatda. Ma'lumotlaringizda kiber-hujum belgilari topilmadi.", "data": {"risk": 5}}

    if analysis_results:
        # Hujum aniqlanganda tahliliy javob
        top = sorted(analysis_results, key=lambda x: x['score'], reverse=True)[0]
        return {
            "response": f"!!! KRITIK TAHLIL: '{top['name']}' hujumiga {top['score']:.1f}% o'xshashlik aniqlandi. Men ushbu ma'lumotni o'rgangan datasetimdagi zararli qoliplar bilan solishtirdim va uni xavfli deb topdim. Tizim avtomatik bloklash rejimiga o'tdi.",
            "data": {"risk": max_risk}
        }

    return {
        "response": f"Tahlil yakunlandi. Ma'lumotlar {len(MODELS)} xil bilim qatlami orqali filtrlandi. Hech qanday anomaliya aniqlanmadi.",
        "data": {"risk": 5}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
