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
    
    st.markdown("### 📍 ข้อมูลร้าน")
    st.markdown("- 🏠 **สาขา:** ห้างไอที สแควร์ ชั้น 3")
    st.markdown("- 🕒 **เวลา:** 10:00 - 20:00 น.")
    st.markdown("- 📞 **ติดต่อ:** 080-123-4567")
    
    st.divider()
    
    st.success("✅ อับดุล AI พร้อมให้บริการ")

# --- Main Layout ---
st.title("❄️ ChillPad Store")
st.subheader("ศูนย์รวมพัดลมระบายความร้อนโน๊ตบุ๊ค")

# --- Tabs ---
tab1, tab2 = st.tabs(["💬 ปรึกษาอับดุล (AI Assistant)", "🛒 สินค้าแนะนำ"])

# --- Tab 1: AI Chat ---
with tab1:
    st.markdown("#### 🤖 อับดุลเอ๊ย! ถามได้ตอบได้")
    st.caption("เรื่องสเปคพัดลม รุ่นที่รองรับ หรือการรับประกัน เชิญนายจ๋าถามได้เลย")
    
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

    # Chat Input
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

# --- Tab 2: Showcase ---
with tab2:
    st.markdown("#### 🔥 สินค้าขายดีประจำเดือน")
    st.info("💡 ข้อมูลสินค้าด้านล่างเป็นเพียงตัวอย่างสำหรับโชว์ UI หน้าร้าน")
    
    sc1, sc2, sc3 = st.columns(3)
    
    with sc1:
        st.image("https://images.unsplash.com/photo-1614812513172-567d2fe9bf62?q=80&w=400&auto=format&fit=crop", caption="พัดลมระบายความร้อน") # ภาพตัวอย่าง
        st.subheader("❄️ ChillMaster Pro")
        st.write("พัดลม 6 ตัว ปรับความแรง 3 ระดับ")
        st.metric(label="ราคา", value="฿ 890", delta="-10%")
        st.button("ดูรายละเอียด", key="btn1", use_container_width=True)
        
    with sc2:
        st.image("https://images.unsplash.com/photo-1585215712169-2f2fbd726912?q=80&w=400&auto=format&fit=crop", caption="พัดลมแบบพกพา")
        st.subheader("🍃 Silent Breeze V2")
        st.write("เงียบกริบ ไร้เสียงรบกวน")
        st.metric(label="ราคา", value="฿ 590")
        st.button("ดูรายละเอียด", key="btn2", use_container_width=True)
        
    with sc3:
        st.image("https://images.unsplash.com/photo-1593640408182-31c70c8268f5?q=80&w=400&auto=format&fit=crop", caption="ที่วางโน๊ตบุ๊ค")
        st.subheader("✈️ Travel Pad Lite")
        st.write("บางเบา พกพาง่าย พับเก็บได้")
        st.metric(label="ราคา", value="฿ 350", delta="-50 บาท")
        st.button("ดูรายละเอียด", key="btn3", use_container_width=True)
