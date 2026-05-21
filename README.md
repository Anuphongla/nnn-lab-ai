# MilkLab° AI — Demi RAG Chatbot

Template สำหรับ Session 3 ของคอร์ส STSW

## วิธีเริ่ม

1. กด **Use this template** ด้านบน → Create a new repository (public)
2. เปิด repo ใหม่ของคุณ → Code → Codespaces → Create codespace
3. รอ container build เสร็จ (~1–3 นาที)
4. เขียน `rag_engine.py` และ `app.py` ตามคู่มือ Session 3
5. รัน `streamlit run app.py` เพื่อทดสอบ

## โครงสร้างที่เตรียมไว้ให้

- `.devcontainer/devcontainer.json` — Python 3.11 + Copilot + Pylance
- `requirements.txt` — streamlit, sentence-transformers, faiss-cpu, google-genai
- `knowledge/milklab_kb.txt` — knowledge base ตัวอย่างของร้าน MilkLab°
- `.gitignore` — กัน `.env` และ credential หลุดขึ้น GitHub

## ไฟล์ที่ต้องเขียนเอง

- `rag_engine.py` — RAG pipeline 5 ขั้น (Load → Chunk → Embed → Search → Generate)
- `app.py` — Streamlit UI + เรียก Gemini API
- `.env` — เก็บ `GOOGLE_API_KEY` (อย่า commit ขึ้น GitHub)

## การ Deploy ขึ้น HuggingFace Spaces

1. สร้าง Space ใหม่ที่ https://huggingface.co/new-space
   - **Owner**: เลือก username ของคุณ
   - **Space name**: ตั้งชื่อ เช่น `milklab-ai`
   - **License**: Apache 2.0
   - **Select the Space SDK**: Streamlit

2. Clone space repository ลงมา:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/milklab-ai
   cd milklab-ai
   ```

3. Copy ไฟล์เหล่านี้จาก repo ของคุณ:
   ```bash
   cp app.py rag_engine.py requirements.txt ./
   cp -r knowledge ./
   ```

4. สร้างไฟล์ `.env` และใส่ `GOOGLE_API_KEY`:
   ```bash
   echo "GOOGLE_API_KEY=your-api-key" > .env
   ```

5. Push ขึ้น HuggingFace:
   ```bash
   git add .
   git commit -m "Deploy MilkLab AI Chatbot"
   git push
   ```

6. HuggingFace จะ build และ deploy อัตโนมัติ ดูที่ "App logs" แท็บ

ดูคู่มือเต็มที่  https://ecp-rmuti.gitbook.io/ai-for-solopreneurs/sessions/session-3 
