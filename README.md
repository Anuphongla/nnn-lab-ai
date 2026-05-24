---
title: ChillPad Store AI
emoji: ❄️
colorFrom: blue
colorTo: blue
sdk: streamlit
sdk_version: "1.43.0"
app_file: app.py
pinned: false
---

# ChillPad Store AI — อับดุล ผู้ช่วยด้านพัดลมเย็น

AI chatbot ผู้ช่วยร้าน ChillPad Store ที่ให้คำปรึกษาด้านสเปคเทคนิคและสินค้าพัดลมระบายความร้อนโน๊ตบุ๊ค

## เกี่ยวกับระบบ

ระบบนี้ใช้เทคนิค **RAG (Retrieval-Augmented Generation)** เพื่อตอบคำถามเกี่ยวกับ:
- 💻 แนะนำรุ่นพัดลมตามขนาดและลักษณะการใช้งานโน๊ตบุ๊ค
- 📊 เปรียบเทียบสเปคเทคนิค (RPM, dBA, ราคา)
- 🛡️ ข้อมูลการรับประกันและวิธีการเคลม
- 🚚 ข้อมูลการจัดส่งและบริการลูกค้า

## Live Demo

🌐 **Demo URL**: [ChillPad Store AI on HuggingFace Spaces]

## วิธีรันในเครื่องท้องถิ่น

### ข้อกำหนดเบื้องต้น
- Python 3.11+
- HuggingFace API Token (สำหรับโมเดล Qwen)

### ขั้นตอนการตั้งค่า

1. Clone repository:
   ```bash
   git clone <your-repo-url>
   cd nnn-lab-ai
   ```

2. สร้าง virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. ติดตั้ง dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. สร้างไฟล์ `.env` และเพิ่ม token:
   ```
   HF_TOKEN=<your_huggingface_token>
   ```

5. รัน Streamlit:
   ```bash
   streamlit run app.py
   ```

## โครงสร้างไฟล์

```
nnn-lab-ai/
├── app.py                  # Streamlit UI + Chat Interface
├── rag_engine.py          # RAG Pipeline (Load → Chunk → Embed → Search)
├── knowledge/
│   └── chillpad_kb.txt    # Knowledge Base (สเปค, FAQ, บริการลูกค้า)
├── requirements.txt       # Dependencies
├── .env                   # API Keys (ห้ามขึ้น GitHub)
├── PIVOT.md              # Pivot Worksheet
└── README.md             # Documentation
```

## Technical Stack

- **Frontend**: Streamlit
- **LLM**: Qwen/Qwen2.5-7B-Instruct (via HuggingFace Inference API)
- **Embeddings**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **Vector DB**: FAISS (IndexFlatL2)
- **Hosting**: HuggingFace Spaces

## Pivot Worksheet (Session 4)

ดูรายละเอียดการ Pivot จาก MilkLab° เป็น ChillPad Store ได้ที่: [PIVOT.md](PIVOT.md)

- **Domain**: ChillPad Store — ร้านขายพัดลมระบายความร้อนโน๊ตบุ๊ค
- **Target Customer**: นักศึกษา, เกมเมอร์, คนทำงานใช้โน๊ตบุ๊คสเปคสูง
- **Key Problems Solved**: 
  1. ช่วยเลือกรุ่นพัดลมให้เหมาะกับขนาดและการใช้งาน
  2. เปรียบเทียบสเปคเทคนิค (RPM, dBA)
  3. ตอบคำถามซ้ำเรื่องสต็อก, ประกัน, วิธีเคลม

## Demo Day Self-Check

- [ ] Deploy URL ใช้งานได้ (ทดสอบล่าสุด: __________)
- [ ] ไม่มี `.env` หรือ token ใน git history
- [ ] PIVOT.md ครบ 3 ข้อ
- [ ] Knowledge base ปรับเป็น ChillPad หมดแล้ว
- [ ] System prompt เป็น "อับดุล" ผู้ช่วยของ ChillPad ✓
- [ ] UI Title และ Quick Prompts เป็น ChillPad ✓
- [ ] README อธิบายระบบของ ChillPad (ไม่ใช่ MilkLab°) ✓

## Resources

- [Session 4 - Pivot Day](https://ecp-rmuti.gitbook.io/ai-for-solopreneurs/sessions/session-4)
- [Session 3 - RAG Chatbot](https://ecp-rmuti.gitbook.io/ai-for-solopreneurs/sessions/session-3)
- [Cohort & Peer Review Guide](https://ecp-rmuti.gitbook.io/ai-for-solopreneurs/resources/cohort-and-review)

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
