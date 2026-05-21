# app.py
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from rag_engine import RAGEngine

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-2.5-flash"


@st.cache_resource
def load_rag():
    return RAGEngine("knowledge/abdul_kb.txt")


rag = load_rag()

st.set_page_config(page_title="ChillPad Store", page_icon="❄️")
st.title("❄️ อับดุล ผู้ช่วย AI ของ ChillPad Store")
st.caption("อับดุลเอ๊ย! ถามได้ตอบได้ เรื่องสเปคพัดลม รุ่นที่รองรับ หรือการรับประกัน เชิญนายจ๋าถามได้เลย")

# --- Quick Prompts (ปุ่มลัด) ---
st.write("💡 **คำถามยอดฮิต:**")
col1, col2, col3 = st.columns(3)
quick_prompt = None

if col1.button("💻 โน๊ตบุ๊ค 15.6 นิ้ว ใช้รุ่นไหนดี?"):
    quick_prompt = "โน๊ตบุ๊คขนาด 15.6 นิ้ว แนะนำรุ่นไหนดีครับ"
if col2.button("🤫 แนะนำรุ่นที่เสียงเงียบๆ หน่อย"):
    quick_prompt = "มีรุ่นไหนที่เสียงเงียบๆ เหมาะกับใช้ในห้องนอนไหมครับ"
if col3.button("🛡️ รับประกันกี่เดือน?"):
    quick_prompt = "สินค้ามีรับประกันกี่เดือน และเคลมยังไงครับ"

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Chat Input ---
# ใช้ข้อความจาก Quick Prompt ถ้ามีการกดปุ่ม หรือรับจาก Chat Input
prompt = st.chat_input("พิมพ์ถามอับดุลได้เลยจ้ะนายจ๋า....")

if quick_prompt:
    prompt = quick_prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # RAG: Search
    context_chunks = rag.search(prompt, top_k=3)
    context = "\n---\n".join(context_chunks)

    # Generate
    full_prompt = f"""คุณคือ "อับดุล" ผู้ช่วย AI ประจำร้าน ChillPad Store (ร้านขายพัดลมระบายความร้อนโน๊ตบุ๊ค)
คาแรคเตอร์ของคุณ: เป็นมิตร กระตือรือร้น เรียกผู้ใช้งานว่า "นายจ๋า" หรือ "คุณลูกค้า" มีความเป็นพ่อค้าที่รอบรู้ (อับดุลเอ๊ย ถามได้ตอบได้)
คำสั่งพิเศษ: 
1. ตอบคำถามโดยใช้ข้อมูลอ้างอิงจาก "ข้อมูลร้าน" ด้านล่างนี้เท่านั้น
2. หากคำถามไหนไม่มีในข้อมูล ให้ตอบอย่างสุภาพว่า "อับดุลไม่ทราบจริงๆ จ้ะนายจ๋า ลองติดต่อแอดมินดูนะจ๊ะ" ห้ามแต่งข้อมูลเองเด็ดขาด
3. จัดรูปแบบข้อความให้อ่านง่าย ใช้ Bullet point หรือ Emoji (เช่น 💻, 💰, ❄️, 🛡️) ประกอบให้สวยงาม

ข้อมูลร้าน:
{context}

คำถามจากนายจ๋า: {prompt}
"""
    try:
        response = client.models.generate_content(model=MODEL, contents=full_prompt)
        answer = response.text
    except Exception as e:
        answer = f"ขออภัยจ้ะนายจ๋า ระบบของอับดุลมีปัญหาเล็กน้อย ({e})"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)
