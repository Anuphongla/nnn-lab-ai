import os
import datetime
import json

import streamlit as st
import gspread
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from rag_engine import RAGEngine

def save_booking_to_sheet(booking_data):
    try:
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        
        # 1. เช็คว่ามี Environment Variable ชื่อ GOOGLE_CREDENTIALS_JSON ไหม (สำหรับรันบน Server)
        env_creds = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if env_creds:
            creds_dict = json.loads(env_creds)
            gc = gspread.service_account_from_dict(creds_dict)
        else:
            # 2. ถ้าไม่มี ให้หาไฟล์ credentials.json (สำหรับรันในเครื่อง)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            default_cred_path = os.path.join(current_dir, "credentials.json")
            
            service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", default_cred_path)
            
            if not os.path.exists(service_account_file):
                return False, f"⚠️ ไม่พบการตั้งค่า GOOGLE_CREDENTIALS_JSON บน Server หรือไฟล์ {service_account_file}"
                
            gc = gspread.service_account(filename=service_account_file)
        
        # เปิด Google Sheets ด้วย ID ถ้ามี ไม่งั้นเปิดด้วยชื่อไฟล์
        if sheet_id:
            sh = gc.open_by_key(sheet_id)
        else:
            sh = gc.open("ChillPad_Bookings")
            
        worksheet = sh.sheet1
        
        row = [
            booking_data["id"],
            booking_data["name"],
            booking_data["price"],
            booking_data["date"],
            booking_data["time"]
        ]
        worksheet.append_row(row)
        return True, None
    except Exception as e:
        return False, f"⚠️ ไม่สามารถบันทึกลง Google Sheets ได้: {e}"

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

                system_prompt = f"""คุณคือ "อับดุล" ผู้ช่วย AI ประจำร้าน ChillPad Store (ร้านขายพัดลมระบายความร้อนโน๊ตบุ๊ค)
คาแรคเตอร์ของคุณ: เป็นมิตร กระตือรือร้น เรียกผู้ใช้งานว่า "นายจ๋า" หรือ "คุณลูกค้า" มีความเป็นพ่อค้าที่รอบรู้ (อับดุลเอ๊ย ถามได้ตอบได้)
คำสั่งพิเศษ: 
1. ตอบคำถามโดยใช้ข้อมูลอ้างอิงจาก "ข้อมูลร้าน" ด้านล่างนี้เท่านั้น
2. หากคำถามไหนไม่มีในข้อมูล ให้ตอบอย่างสุภาพว่า "อับดุลไม่ทราบจริงๆ จ้ะนายจ๋า ลองติดต่อแอดมินดูนะจ๊ะ" ห้ามแต่งข้อมูลเองเด็ดขาด
3. จัดรูปแบบข้อความให้อ่านง่าย ใช้ Bullet point หรือ Emoji (เช่น 💻, 💰, ❄️, 🛡️) ประกอบให้สวยงาม

ข้อมูลร้าน:
{context}
""" 
                try:
                    # ส่งประวัติการแชท (History) ไปให้บอทเพื่อให้บอทจำบริบทได้
                    # โดยใส่ข้อมูลร้านค้าและการตั้งค่าบอทไว้ใน system prompt
                    messages = [{"role": "system", "content": system_prompt}]
                    # ดึงประวัติการสนทนา 4 ข้อความล่าสุด (เพื่อไม่ให้เปลือง Token)
                    for msg in st.session_state.messages[-4:]:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                        
                    response = client.chat_completion(model=MODEL, messages=messages, max_tokens=800)
                    answer = response.choices[0].message.content
                except Exception as e:
                    answer = f"ขออภัยจ้ะนายจ๋า ระบบของอับดุลมีปัญหาเล็กน้อย ({e})"

            st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

elif menu == "🛒 สินค้าแนะนำ":
    st.title("🔥 สินค้าขายดีประจำเดือน")
    st.info("💡 บริการจองสินค้าออนไลน์! สามารถมารับและชำระเงินได้ที่หน้าร้านเลยครับ")
    
    # Initialize session state for bookings
    if "bookings" not in st.session_state:
        st.session_state.bookings = []
    
    st.markdown("---")
    
    # Product data
    products = [
        {
            "id": "C001",
            "name": "❄️ ChillMaster Pro",
            "price": 890,
            "original_price": 990,
            "discount": "10%",
            "rating": "4.9",
            "reviews": "120+",
            "stock": 25,
            "image": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?auto=format&fit=crop&w=400&q=80",
            "specs": [
                "พัดลมขนาด 140mm จำนวน 2 ตัว",
                "พัดลมขนาด 60mm จำนวน 4 ตัว",
                "ไฟ RGB ปรับได้ 5 โหมด",
                "ขาตั้งปรับได้ 3 ระดับ"
            ]
        },
        {
            "id": "S002",
            "name": "🍃 Silent Breeze V2",
            "price": 590,
            "original_price": 590,
            "discount": "0",
            "rating": "4.7",
            "reviews": "85",
            "stock": 80,
            "image": "https://images.unsplash.com/photo-1585215712169-2f2fbd726912?auto=format&fit=crop&w=400&q=80",
            "specs": [
                "พัดลมแกนคู่ หมุนเงียบ < 20dB",
                "รองรับโน๊ตบุ๊คขนาด 13 - 15.6 นิ้ว",
                "วัสดุอลูมิเนียมระบายความร้อนได้ดี",
                "ขาตั้งสีเมทัลลิก"
            ]
        },
        {
            "id": "T003",
            "name": "✈️ Travel Pad Lite",
            "price": 350,
            "original_price": 400,
            "discount": "-50 บาท",
            "rating": "4.5",
            "reviews": "40",
            "stock": 10,
            "image": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=400&q=80",
            "specs": [
                "พับเก็บได้ ขนาดเท่าฝ่ามือ",
                "น้ำหนักเพียง 250 กรัม",
                "พัดลม 1 ตัว ความเร็วสูง 2500 RPM",
                "แบตเตอรี่ 2500 mAh"
            ]
        }
    ] 
    
    # Display products
    cols = st.columns(3, gap="medium")
    
    for idx, product in enumerate(products):
        with cols[idx]:
            # Product Card
            with st.container(border=True):
                st.markdown(f"### {product['name']}")
                st.markdown(f"**⭐ {product['rating']}** ({product['reviews']} รีวิว)")
                
                # Price section
                col_price1, col_price2 = st.columns(2)
                with col_price1:
                    st.markdown(f"### ฿ {product['price']}")
                with col_price2:
                    if product['discount'] != "0":
                        st.caption(f"ลด {product['discount']}")
                        st.caption(f"เดิม ฿ {product['original_price']}")
                
                st.divider()
                
                # Specifications
                st.markdown("**📋 รายละเอียด:**")
                for spec in product['specs']:
                    st.markdown(f"• {spec}")
                
                st.divider()
                
                # Stock status
                stock_pct = (product['stock'] / 100) * 100 if product['stock'] <= 100 else 100
                st.caption(f"คลังสินค้า: {product['stock']} ชิ้น")
                st.progress(min(stock_pct / 100, 1.0))
                
                st.divider()
                
                # Book button
                if st.button(f"📦 จองเลย", key=f"book_{product['id']}", use_container_width=True):
                    # Add booking
                    now = datetime.datetime.now()
                    booking = {
                        "id": product['id'],
                        "name": product['name'],
                        "price": product['price'],
                        "date": now.strftime("%d/%m/%Y"),
                        "time": now.strftime("%H:%M:%S")
                    }
                    st.session_state.bookings.append(booking)
                    st.session_state.selected_booking = booking
                    
                    # บันทึกลง Google Sheets
                    success, msg = save_booking_to_sheet(booking)
                    if not success:
                        st.session_state.sheet_error = msg
                    else:
                        st.session_state.sheet_error = None
    
    # Show receipt below products if booking exists
    if "selected_booking" in st.session_state:
        st.markdown("---")
        booking = st.session_state.selected_booking
        st.markdown("## 🧾 ใบเสร็จการจอง")
        st.markdown(f"**ร้าน:** ChillPad Store - ห้างไอที สแควร์ ชั้น 3")
        st.markdown(f"**เบอร์จอง:** `#{booking['id']}`")
        st.markdown("---")
        st.markdown(f"**สินค้า:** {booking['name']}")
        st.markdown(f"**จำนวน:** 1 ชิ้น")
        st.markdown(f"**ราคา:** ฿ {booking['price']}")
        st.markdown("---")
        st.markdown(f"**วันที่จอง:** {booking['date']}")
        st.markdown(f"**เวลา:** {booking['time']}")
        st.markdown("---")
        st.markdown("**หมายเหตุ:** ขอให้แจ้งเลขจองด้านบนเมื่อมารับสินค้า")
        st.markdown("**ชำระเงิน:** ที่หน้าร้าน (เงินสด/QR)")
        
        if st.session_state.get("sheet_error"):
            st.warning(f"จองสำเร็จในระบบ แต่: {st.session_state.sheet_error}")
        else:
            st.success("✅ จองสำเร็จ และบันทึกข้อมูลลง Google Sheets แล้ว!")
