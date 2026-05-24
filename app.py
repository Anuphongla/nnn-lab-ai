import os

import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from rag_engine import RAGEngine

# --- Config & Initialization ---
st.set_page_config(page_title="ChillPad Store", page_icon="❄️", layout="wide")

load_dotenv()
client = InferenceClient(api_key=os.getenv("HF_TOKEN"))
MODEL = "Qwen/Qwen2.5-7B-Instruct" 

@st.cache_resource
def load_rag():
    return RAGEngine("knowledge/chillpad_kb.txt")

rag = load_rag()

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ❄️ ChillPad Store")
    st.caption("ร้านจำหน่ายพัดลมระบายความร้อนโน๊ตบุ๊คอันดับ 1")
    
    st.divider()
    
    # Navigation
    menu = st.radio("เมนูหลัก", ["💬 ปรึกษาอับดุล (AI Assistant)", "🛒 สินค้าแนะนำ"])
    
    st.divider()
    
    st.markdown("### 📍 ข้อมูลร้าน")
    st.markdown("- 🏠 **สาขา:** ห้างไอที สแควร์ ชั้น 3")
    st.markdown("- 🕒 **เวลา:** 10:00 - 20:00 น.")
    st.markdown("- 📞 **ติดต่อ:** 080-123-4567")

# --- Main Layout ---
if menu == "💬 ปรึกษาอับดุล (AI Assistant)":
    st.title("❄️ ปรึกษาอับดุล AI")
    st.caption("อับดุลเอ๊ย! ถามได้ตอบได้ เรื่องสเปคพัดลม รุ่นที่รองรับ หรือการรับประกัน เชิญนายจ๋าถามได้เลย")
    
    # Quick Prompts
    st.markdown("**💡 คำถามยอดฮิต:**")
    col1, col2, col3, col4 = st.columns(4)
    quick_prompt = None
    
    if col1.button("💻 โน๊ตบุ๊ค 15.6 นิ้ว?", use_container_width=True):
        quick_prompt = "โน๊ตบุ๊คขนาด 15.6 นิ้ว แนะนำรุ่นไหนดีครับ"
    if col2.button("🤫 รุ่นเสียงเงียบ?", use_container_width=True):
        quick_prompt = "มีรุ่นไหนที่เสียงเงียบๆ เหมาะกับใช้ในห้องนอนไหมครับ"
    if col3.button("🎮 สายเกมมิ่ง?", use_container_width=True):
        quick_prompt = "มีรุ่นไหนระบายความร้อนได้ดีที่สุดสำหรับเล่นเกมไหมครับ"
    if col4.button("🛡️ การรับประกัน?", use_container_width=True):
        quick_prompt = "สินค้ามีรับประกันกี่เดือน และเคลมยังไงครับ"

    st.divider()

    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat Input - อยู่ระดับ Root จะได้ยึดติดขอบจอด้านล่าง
    prompt = st.chat_input("พิมพ์ถามอับดุลได้เลยจ้ะนายจ๋า....")

    if quick_prompt:
        prompt = quick_prompt

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # RAG Search
        with st.chat_message("assistant"):
            with st.spinner("อับดุลกำลังค้นหาข้อมูล..."):
                context_chunks = rag.search(prompt, top_k=3)
                context = "\n---\n".join(context_chunks)

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
                    messages = [{"role": "user", "content": full_prompt}]
                    response = client.chat_completion(model=MODEL, messages=messages, max_tokens=800)
                    answer = response.choices[0].message.content
                except Exception as e:
                    answer = f"ขออภัยจ้ะนายจ๋า ระบบของอับดุลมีปัญหาเล็กน้อย ({e})"

            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

elif menu == "🛒 สินค้าแนะนำ":
    st.title("🔥 สินค้าขายดีประจำเดือน")
    st.info("💡 บริการจองสินค้าออนไลน์! สามารถมารับและชำระเงินได้ที่หน้าร้านเลยครับ")
    
    st.markdown("---")
    
    sc1, sc2, sc3 = st.columns(3)
    
    with sc1:
        # ภาพเกมมิ่งที่โหลดเร็วและเสถียร
        st.image("https://images.unsplash.com/photo-1593640408182-31c70c8268f5?auto=format&fit=crop&w=400&q=80", caption="รุ่น Top สำหรับสายเกม")
        st.subheader("❄️ ChillMaster Pro")
        st.markdown("**⭐ 4.9** (รีวิว 120+)")
        st.metric(label="ราคาพิเศษ", value="฿ 890", delta="-10% จากราคาปกติ")
        
        st.caption("ความจุคลังสินค้า")
        st.progress(25) # เหลือ 25%
        
        with st.expander("📝 ดูสเปคแบบละเอียด"):
            st.markdown("- พัดลมขนาด 140mm จำนวน 2 ตัว\n- พัดลมขนาด 60mm จำนวน 4 ตัว\n- ไฟ RGB ปรับได้ 5 โหมด\n- ขาตั้งปรับได้ 3 ระดับ")
            
        if st.button("📦 จองสินค้ารับหน้าร้าน", key="btn1", use_container_width=True):
            st.toast("✅ จอง 'ChillMaster Pro' สำเร็จ! รหัสจอง: #C001 กรุณาชำระเงินที่หน้าร้านครับ")
            st.success("🎉 จองสำเร็จ! โปรดแจ้งรหัส **#C001** เพื่อรับสินค้าที่สาขา ไอที สแควร์")
            st.balloons()
        
    with sc2:
        # ภาพเรียบหรูสไตล์ออฟฟิศ
        st.image("https://images.unsplash.com/photo-1585215712169-2f2fbd726912?auto=format&fit=crop&w=400&q=80", caption="ขายดีอันดับ 1 สำหรับคนทำงาน")
        st.subheader("🍃 Silent Breeze V2")
        st.markdown("**⭐ 4.7** (รีวิว 85)")
        st.metric(label="ราคาพิเศษ", value="฿ 590", delta="สินค้าขายดี", delta_color="off")
        
        st.caption("ความจุคลังสินค้า")
        st.progress(80) # เหลือ 80%
        
        with st.expander("📝 ดูสเปคแบบละเอียด"):
            st.markdown("- พัดลมแกนคู่ หมุนเงียบ < 20dB\n- รองรับโน๊ตบุ๊คขนาด 13 - 15.6 นิ้ว\n- วัสดุอลูมิเนียมระบายความร้อนได้ดี")
            
        if st.button("📦 จองสินค้ารับหน้าร้าน", key="btn2", use_container_width=True):
            st.toast("✅ จอง 'Silent Breeze V2' สำเร็จ! รหัสจอง: #S002 กรุณาชำระเงินที่หน้าร้านครับ")
            st.success("🎉 จองสำเร็จ! โปรดแจ้งรหัส **#S002** เพื่อรับสินค้าที่สาขา ไอที สแควร์")
        
    with sc3:
        # ภาพขาตั้ง/พัดลมแบบมินิมอล
        st.image("https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=400&q=80", caption="น้ำหนักเบา พกพาสะดวก")
        st.subheader("✈️ Travel Pad Lite")
        st.markdown("**⭐ 4.5** (รีวิว 40)")
        st.metric(label="ราคาพิเศษ", value="฿ 350", delta="-50 บาท (โค้ดลด)")
        
        st.caption("ความจุคลังสินค้า")
        st.progress(10) # เหลือ 10%
        
        with st.expander("📝 ดูสเปคแบบละเอียด"):
            st.markdown("- พับเก็บได้ ขนาดเท่าฝ่ามือ\n- น้ำหนักเพียง 250 กรัม\n- พัดลม 1 ตัว ความเร็วสูง 2500 RPM")
            
        if st.button("📦 จองสินค้ารับหน้าร้าน", key="btn3", use_container_width=True):
            st.toast("✅ จอง 'Travel Pad Lite' สำเร็จ! รหัสจอง: #T003 กรุณาชำระเงินที่หน้าร้านครับ")
            st.success("🎉 จองสำเร็จ! โปรดแจ้งรหัส **#T003** เพื่อรับสินค้าที่สาขา ไอที สแควร์")
            st.snow()
