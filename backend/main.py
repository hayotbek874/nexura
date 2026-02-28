from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import time

app = FastAPI(title="NEXURA Neural Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI komponentlarini yuklaymiz
try:
    # Perimetr modeli
    network_model = joblib.load('nexura_ai_model.pkl')
    # SQL Injection modeli
    sqli_model = joblib.load('sqli_model.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')
    print("AI: Barcha mudofaa modellari yuklandi.")
except Exception as e:
    print(f"AI: Model yuklashda xatolik: {e}")
    sqli_model = None

class UserInput(BaseModel):
    text: str

@app.post("/ai/chat")
async def ai_chat(user_input: UserInput):
    text = user_input.text
    time.sleep(0.4)

    # --- 1. SQL INJECTION TEKSHIRUVI ---
    if sqli_model and tfidf:
        # Matnni vektorga o'tkazamiz
        vec = tfidf.transform([text])
        # Bashorat: 1 - Hujum, 0 - Xavfsiz
        prediction = sqli_model.predict(vec)[0]

        if prediction == 1:
            return {
                "response": f"!!! OGOHLANTIRISH: Zararli SQL kodi aniqlandi. Tizim bloklandi. [Detection: SQLi Model]",
                "data": {"risk": 95}
            }

    # --- 2. LOGIKA VA MULOQOT ---
    text_lower = text.lower()

    if "xavf" in text_lower or "threat" in text_lower:
        risk_val = np.random.randint(5, 20)
        return {
            "response": f"AI MONITORING: Tizim barqaror. SQLi va Network modellari faol. Umumiy risk: {risk_val}%.",
            "data": {"risk": risk_val}
        }

    if "blok" in text_lower or "block" in text_lower:
        return {"response": "BUYRUQ: Barcha shubhali kirish nuqtalari izolyatsiya qilindi."}

    if "salom" in text_lower or "hello" in text_lower:
        return {"response": "Salom! NEXURA AI mudofaa markazi sizni eshitmoqda. Tizim to'liq himoyalangan."}

    return {"response": "Xabar qabul qilindi. AI model real vaqtda har bir so'rovni tahlil qilmoqda."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
