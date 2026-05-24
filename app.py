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

# --- Custom CSS ---
st.markdown("""
    <style>
    /* Theme color customization */
    .stApp {
        background-color: #f0f8ff;
    }
    .main-header {
        font-size: 2.5rem;
        color: #004d99;
        font-weight: bold;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.1rem;
        color: #0073e6;
        text-align: center;
        margin-bottom: 2rem;
    }
    .shop-info-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        text-align: center;
        border-top: 4px solid #0073e6;
    }
    .css-1d391kg {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3004/3004382.png", width=80) # Placeholder Fan Icon
    st.markdown("## ❄️ ChillPad Store")
    st.caption("ร้านจำหน่ายพัดลมระบายความร้อนโน๊ตบุ๊คอันดับ 1")
    
    st.markdown("---")
    st.markdown("### 📍 ข้อมูลร้าน")
    st.markdown("🏠 **สาขาหลัก:** ห้างไอที สแควร์ ชั้น 3")
    st.markdown("🕒 **เวลาเปิด-ปิด:** 10:00 น. - 20:00 น. (เปิดทุกวัน)")
    st.markdown("📞 **ติดต่อ:** 080-123-4567")
    
    st.markdown("---")
    st.success("✅ ระบบ AI พร้อมให้บริการ")
    st.info("อับดุลสามารถช่วยแนะนำสินค้าตามสเปคโน๊ตบุ๊คของคุณได้")

# --- Main Layout ---
st.markdown("<div class='main-header'>❄️ ยินดีต้อนรับสู่ ChillPad Store ❄️</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>ศูนย์รวมพัดลมระบายความร้อนที่เย็นที่สุดสำหรับโน๊ตบุ๊คคู่ใจของคุณ</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 ปรึกษาอับดุล (AI Assistant)", "🛒 สินค้าแนะนำ (Showcase)"])

# --- Tab 1: AI Chat ---
with tab1:
    st.write("### 🤖 อับดุล ผู้ช่วย AI ประจำร้าน")
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

    st.markdown("---")


    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Create a container for chat history so it doesn't overlap input
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Chat Input
    prompt = st.chat_input("พิมพ์ถามอับดุลได้เลยจ้ะนายจ๋า....")

    if quick_prompt:
        prompt = quick_prompt

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)

        # RAG Search with Spinner
        with st.spinner("อับดุลกำลังค้นหาข้อมูลจ้ะนายจ๋า..."):
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

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with chat_container:
            with st.chat_message("assistant"):
                st.write(answer)

# --- Tab 2: Showcase ---
with tab2:
    st.write("### 🔥 สินค้าขายดีประจำเดือน (Mockup)")
    
    sc1, sc2, sc3 = st.columns(3)
    
    with sc1:
        st.markdown("<div class='shop-info-box'>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/1085/1085188.png", width=100)
        st.subheader("❄️ ChillMaster Pro")
        st.write("พัดลม 6 ตัว ปรับความแรงได้ 3 ระดับ เย็นสะใจสำหรับสายเกมเมอร์")
        st.metric(label="ราคา", value="฿ 890", delta="-10%")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with sc2:
        st.markdown("<div class='shop-info-box'>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/1085/1085188.png", width=100)
        st.subheader("🍃 Silent Breeze V2")
        st.write("เงียบกริบ ไร้เสียงรบกวน เหมาะสำหรับการทำงานในออฟฟิศ")
        st.metric(label="ราคา", value="฿ 590")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with sc3:
        st.markdown("<div class='shop-info-box'>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/1085/1085188.png", width=100)
        st.subheader("✈️ Travel Pad Lite")
        st.write("บางเบา พกพาง่าย พับเก็บได้สะดวกสบายตอบโจทย์สายเดินทาง")
        st.metric(label="ราคา", value="฿ 350", delta="-50 บาท")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.info("💡 หมายเหตุ: ข้อมูลสินค้าด้านบนเป็นเพียงตัวอย่าง (Mockup) สำหรับประกอบ UI เท่านั้น ข้อมูลจริงในการตอบคำถามจะดึงมาจาก Knowledge Base ครับ")
