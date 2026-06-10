class CulinaryFSM:
    def __init__(self):
        """Inisialisasi kunci memori otomata pada Streamlit"""
        self.state_key = "bot_state"
        self.context_key = "bot_context"

    def get_current_state(self, session_state):
        """Mengambil status chatbot saat ini dari session state"""
        if self.state_key not in session_state:
            session_state[self.state_key] = "S_GREETING"
        if self.context_key not in session_state:
            session_state[self.context_key] = {"city": None, "category": None}
        if "cart" not in session_state:
            session_state["cart"] = []
        return session_state[self.state_key]

    def transition(self, session_state, intent, entities=None, engine=None):
        """Fungsi Transisi Deterministik (Delta) dengan Implementasi Alur Looping Back"""
        current_state = self.get_current_state(session_state)
        if intent == "RESET":
            session_state[self.state_key] = "S_GREETING"
            session_state[self.context_key] = {"city": None, "category": None}
            session_state["cart"] = []
            return "Sistem berhasil dikosongkan. Mari mulai dari awal! ✨ Kota mana yang ingin kamu jelajahi kulinernya?"

        if current_state == "S_GREETING":
            if entities and entities.get("city"):
                session_state[self.state_key] = "S_CHOOSE_CATEGORY"
                session_state[self.context_key]["city"] = entities["city"]
                return f"Pilihan mantap! Kita sekarang menjelajahi kota **{entities['city'].upper()}**. Kamu butuh rekomendasi untuk waktu makan kapan? (Sarapan / Siang / Malam / Ikonik)"
            else:
                return "Halo! Selamat datang di Chatbot Kuliner Nusantara. 🌟 Silakan ketik nama kota pilihanmu (Yogyakarta, Semarang, Padang, Pontianak, atau Jayapura) untuk memulai petualangan kuliner!"

        elif current_state == "S_CHOOSE_CATEGORY":
            if entities and entities.get("category"):
                session_state[self.state_key] = "S_SHOW_RECOMMENDATION"
                session_state[self.context_key]["category"] = entities["category"]
                return f"Kategori **{entities['category'].upper()}** telah dipilih. Silakan ketik **'lihat'** atau **'rekomendasi'** untuk memuat ulasan menu kulinernya!"
            elif entities and entities.get("city"):
                session_state[self.context_key]["city"] = entities["city"]
                return f"Konteks wilayah dialihkan ke kota **{entities['city'].upper()}**. Mau rekomendasi sarapan, siang, malam, atau menu ikonik?"
            else:
                current_city = session_state[self.context_key]["city"]
                return f"Kamu masih berada dalam eksplorasi kota **{current_city.upper()}**. Silakan pilih salah satu kategori: Sarapan, Siang, Malam, atau Ikonik."

        elif current_state == "S_SHOW_RECOMMENDATION":
            current_city = session_state[self.context_key]["city"]
            current_cat = session_state[self.context_key]["category"]

            if intent == "YES":
                if engine and current_city and current_cat:
                    menu_item = engine.menu_data[current_city][current_cat]
                    found = False
                    for cart_item in session_state["cart"]:
                        if cart_item["item"] == menu_item["name"]:
                            cart_item["qty"] += 1
                            found = True
                            break
                    
                    if not found:
                        session_state["cart"].append({
                            "item": menu_item["name"],
                            "qty": 1,
                            "price": menu_item["price"],
                            "emoji": menu_item["emoji"]
                        })
                    
           
                    session_state[self.state_key] = "S_CHOOSE_CATEGORY"
                    session_state[self.context_key]["category"] = None 
                    
                    return f"Sukses! **{menu_item['emoji']} {menu_item['name']}** telah ditambahkan ke keranjang belanjaanmu. Kamu masih berada di kota **{current_city.upper()}**. Ada kategori waktu makan lain yang ingin kamu coba? (Sarapan / Siang / Malam / Ikonik) atau ketik **'checkout'** jika sudah cukup."

            elif intent == "CHECKOUT":
                if not session_state["cart"]:
                    return "Keranjang belanjamu masih kosong. Silakan konfirmasi pesan menu rekomendasi terlebih dahulu dengan mengetik 'ya' atau 'oke'."
                session_state[self.state_key] = "S_CHECKOUT"
                return "Sesi dikunci. Memproses pesanan Anda ke nota penutupan aplikasi (Final State)..."
            
            if entities and entities.get("category"):
                session_state[self.context_key]["category"] = entities["category"]
                return f"Kategori dialihkan ke **{entities['category'].upper()}**. Ketik **'lihat'** untuk melihat perubahan menu."
            elif entities and entities.get("city"):
                session_state[self.state_key] = "S_CHOOSE_CATEGORY"
                session_state[self.context_key]["city"] = entities["city"]
                session_state[self.context_key]["category"] = None
                return f"Pindah haluan ke kota **{entities['city'].upper()}**. Silakan tentukan kategori makanmu yang baru."
            
            return f"Ketik **'lihat'** untuk memuat detail makanan, ketik **'ya'** untuk memasukkannya ke keranjang, atau ketik **'checkout'** untuk selesai."

        elif current_state == "S_CHECKOUT":
            return "Seluruh transaksi telah selesai diproses (Final State). Sesi dikunci demi keamanan data. Silakan klik tombol atau ketik **'reset'** jika ingin memulai petualangan baru!"

        return "Maaf, mesin FSM mendeteksi adanya token di luar jangkauan bahasa reguler sistem."