import streamlit as st
import base64
import os
from engine import CulinaryEngine
from FSM import CulinaryFSM
import templates  

st.set_page_config(page_title="NusaKuliner Premium", page_icon="🍱", layout="wide")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def safe_html(text: str) -> str:
    """Escape teks input mentah user secara total agar tidak memicu kebocoran DOM."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )

@st.cache_resource
def init_backend():
    return CulinaryEngine(), CulinaryFSM()

engine, fsm = init_backend()

try:
    with open("assets/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("Berkas assets/style.css tidak ditemukan.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Halo! Selamat datang di Chatbot Kuliner Nusantara. 🌟 Silakan ketik nama kota pilihanmu (Yogyakarta, Semarang, Padang, Pontianak, atau Jayapura) untuk memulai!",
        }
    ]

if "show_chat" not in st.session_state:
    st.session_state["show_chat"] = False

if "bot_context" not in st.session_state:
    st.session_state["bot_context"] = {"city": None, "category": None}

current_state = fsm.get_current_state(st.session_state)
context = st.session_state["bot_context"]

st.markdown(templates.get_navbar(), unsafe_allow_html=True)

hero_base64 = get_base64_image("assets/images/hero_background.webp")
hero_src = f"data:image/webp;base64,{hero_base64}" if hero_base64 else ""
st.markdown(templates.get_hero_section(hero_src), unsafe_allow_html=True)

categories_mapping = {
    "sarapan": {"id": "section_sarapan", "title": "🥣 Sarapan Pagi Pilihan"},
    "siang":   {"id": "section_siang",   "title": "🍱 Hidangan Makan Siang"},
    "malam":   {"id": "section_malam",   "title": "🍢 Kuliner Makan Malam"},
    "ikonik":  {"id": "section_ikonik",  "title": "🥩 Menu Ikonik & Spesial"},
}

for cat_key, cat_info in categories_mapping.items():

    parts = [templates.get_section_start(cat_info['id'], cat_info['title'])]

    for city_name, categories in engine.menu_data.items():
        item = categories[cat_key]
        is_active = context.get("city") == city_name
        card_class = "food-card active-city-card" if is_active else "food-card"

        img_slug = item["name"].lower().replace(" ", "_") + ".webp"
        lightbox_id = f"lb-{cat_key}-{city_name.lower().replace(' ', '_')}"
        img_b64 = get_base64_image(f"assets/images/{img_slug}")
        img_src_card = f"data:image/webp;base64,{img_b64}" if img_b64 else ""

        s_name  = safe_html(item["name"])
        s_city  = safe_html(city_name.upper())
        s_price = safe_html(f"Rp{item['price']:,}")
        s_desc  = safe_html(item["desc"])
        s_emoji = safe_html(item.get("emoji", ""))

    
        parts.append(templates.get_food_card(lightbox_id, card_class, img_src_card, s_name, s_city, s_price))
        parts.append(templates.get_lightbox_modal(lightbox_id, img_src_card, s_emoji, s_name, s_city, s_desc, s_price))

    parts.append(templates.get_section_end())
    st.markdown("".join(parts), unsafe_allow_html=True)

st.markdown(templates.get_spice_routes(), unsafe_allow_html=True)
st.markdown(templates.get_footer(), unsafe_allow_html=True)

st.markdown("<div class='floating-trigger-container'>", unsafe_allow_html=True)
if st.button("📱 Layanan Chatbot FSM", key="phone_toggle_btn"):
    st.session_state["show_chat"] = not st.session_state["show_chat"]
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state["show_chat"]:
    phone_parts = [templates.get_phone_chassis_start("phone-chassis")]
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            content = safe_html(msg["content"])
        else:
            content = msg["content"].replace("\n", "<br>")
        phone_parts.append(templates.get_chat_bubble(msg["role"], content))

    phone_parts.append(templates.get_phone_chassis_end())
    st.markdown("".join(phone_parts), unsafe_allow_html=True)

    st.markdown("<div class='phone-form-marker'></div>", unsafe_allow_html=True)
    with st.form(key="phone_input_gate", clear_on_submit=True):
        u_text = st.text_input("Input", placeholder="Ketik kota atau instruksi...", label_visibility="collapsed")
        c_send, c_res = st.columns([7, 3])
        with c_send:
            btn_send = st.form_submit_button("Kirim 🚀", use_container_width=True)
        with c_res:
            btn_res = st.form_submit_button("🔄 Reset", use_container_width=True)

    if btn_send and u_text:
        st.session_state.messages.append({"role": "user", "content": u_text})
        intent   = engine.detect_intent(u_text)
        entities = engine.extract_entities(u_text)
        bot_response = fsm.transition(st.session_state, intent, entities, engine)

        if (
            current_state == "S_SHOW_RECOMMENDATION"
            and intent in ["UNKNOWN", "ASK_MENU"]
            and ("lihat" in u_text.lower() or "rekomendasi" in u_text.lower())
        ):
            active_city = context["city"]
            active_cat  = context["category"]
            menu = engine.menu_data[active_city][active_cat]
            bot_response = (
                f"Rekomendasi Utama:<br><br>"
                f"<strong>{safe_html(menu['emoji'])} {safe_html(menu['name'])}</strong><br>"
                f"Estimasi: Rp{menu['price']:,}<br><br>"
                f"{safe_html(menu['desc'])}<br><br>"
                f"Ketik <strong>'ya'</strong> untuk membeli, atau <strong>'batal'</strong>."
            )

        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()

    if btn_res:
        fsm.transition(st.session_state, "RESET")
        st.session_state.messages = [{"role": "assistant", "content": "Sistem berhasil dikosongkan. Kota mana yang ingin kamu jelajahi kulinernya?"}]
        st.rerun()