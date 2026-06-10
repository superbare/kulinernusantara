import re

class CulinaryEngine:
    def __init__(self):
        self.menu_data = {
            "yogyakarta": {
                "sarapan": {"name": "Bubur Lemu", "price": 12000, "emoji": "🥣", "desc": "Bubur gurih krecek khas Jogja"},
                "siang": {"name": "Mangut Lele", "price": 18000, "emoji": "🐟", "desc": "Lele asap dengan kuah santan pedas"},
                "malam": {"name": "Sate Klatak", "price": 25000, "emoji": "🍢", "desc": "Sate kambing muda dengan jeruji besi"},
                "ikonik": {"name": "Gudeg Yu Djum", "price": 35000, "emoji": "🍱", "desc": "Gudeg nangka manis legendaris"}
            },
            "semarang": {
                "sarapan": {"name": "Nasi Ayam Semarang", "price": 15000, "emoji": "🍛", "desc": "Nasi gurih kuah opor encer"},
                "siang": {"name": "Tahu Gimbal", "price": 17000, "emoji": "⚱️", "desc": "Tahu goreng dengan gimbal udang krispi"},
                "malam": {"name": "Babat Gongso", "price": 22000, "emoji": "🍳", "desc": "Jeroan babat manis pedas khas Semarang"},
                "ikonik": {"name": "Lumpia Semarang", "price": 15000, "emoji": "🌯", "desc": "Lumpia isi rebung dan udang"}
            },
            "padang": {
                "sarapan": {"name": "Katupek Sayur", "price": 12000, "emoji": "🍲", "desc": "Ketupat sayur gulai pakis Padang"},
                "siang": {"name": "Nasi Padang", "price": 25000, "emoji": "🍱", "desc": "Nasi dengan lauk ayam pop atau tunjang"},
                "malam": {"name": "Sate Padang", "price": 20000, "emoji": "🍢", "desc": "Sate daging sapi dengan kuah kental berempah"},
                "ikonik": {"name": "Rendang Daging", "price": 18000, "emoji": "🥩", "desc": "Rendang daging sapi hitam autentik"}
            },
            "pontianak": {
                "sarapan": {"name": "Bubur Pedas", "price": 14000, "emoji": "🥣", "desc": "Bubur sayuran dan rempah khas Kalimantan"},
                "siang": {"name": "Asam Pedas Patin", "price": 28000, "emoji": "🐟", "desc": "Ikan patin dengan kuah asam pedas segar"},
                "malam": {"name": "Kwetiau Goreng", "price": 20000, "emoji": "🍝", "desc": "Kwetiau goreng sapi khas Pontianak"},
                "ikonik": {"name": "Choi Pan", "price": 15000, "emoji": "🥟", "desc": "Kue kukus gurih isi bengkuang"}
            },
            "jayapura": {
                "sarapan": {"name": "Keladi Tumbuk", "price": 15000, "emoji": "🍠", "desc": "Keladi kukus halus disajikan gurih"},
                "siang": {"name": "Papeda Kuah Kuning", "price": 30000, "emoji": "🍲", "desc": "Sagu kental berkuah ikan gabus kuning"},
                "malam": {"name": "Udang Selingkuh", "price": 45000, "emoji": "🦞", "desc": "Udang air tawar capit besar khas Papua"},
                "ikonik": {"name": "Ikan Asar", "price": 35000, "emoji": "🐟", "desc": "Ikan asap kering tahan lama khas Jayapura"}
            }
        }
        
        self.re_number = r"\b(\d+)\b"
        kota_keys = "|".join(self.menu_data.keys())
        self.re_kota = rf"\b({kota_keys}|jogja|yogyakarta|yogya)\b"
        self.re_kategori = r"\b(sarapan|pagi|siang|malam|ikonik|legendaris)\b"
        self.re_split = r"[,.]|\bdan\b|&"
        self.re_cancel_all = r"\b(batalkan semua|hapus semua|reset keranjang|kosongkan)\b"
        self.re_reduce = r"\b(batalkan|kurangi|tidak jadi|hapus|cancel)\b"

    def detect_intent(self, text):
        """Mendeteksi instruksi utama dari teks input pengguna"""
        text = text.lower()
        if re.search(r"\b(reset|ulang|mulai baru)\b", text):
            return "RESET"
        if re.search(self.re_cancel_all, text):
            return "CANCEL_ALL"
        if re.search(self.re_reduce, text):
            return "REDUCE_ITEM"
        if re.search(r"\b(menu|daftar|pilihan|jual apa)\b", text):
            return "ASK_MENU"
        if re.search(r"\b(selesai|bayar|checkout|cukup|hitung)\b", text):
            return "CHECKOUT"
        if re.search(r"\b(ya|yes|oke|betul|siap|baik|bisa)\b", text):
            return "YES"
        if re.search(r"\b(tidak|enggak|batal|no|salah)\b", text):
            return "NO"
        return "UNKNOWN"

    def extract_entities(self, text):
        """Mengekstrak entitas kota dan kategori dari teks bebas"""
        text = text.lower()
        city_match = re.search(self.re_kota, text)
        city = city_match.group(1) if city_match else None
        if city in ["jogja", "yogyakarta", "yogya"]:
            city = "yogyakarta"
        cat_match = re.search(self.re_kategori, text)
        category = cat_match.group(1) if cat_match else None
        if category == "pagi": category = "sarapan"
        if category == "legendaris": category = "ikonik"
        
        return {"city": city, "category": category}

    def _parse_single_segment(self, text):
        """Helper untuk memproses satu potongan klausa pesanan makanan"""
        text = text.lower().strip()
        all_items = []
        for city in self.menu_data:
            for cat in self.menu_data[city]:
                all_items.append(self.menu_data[city][cat]["name"].lower())
        
        re_items = rf"\b({'|'.join(all_items)})\b"
        
        item_match = re.search(re_items, text)
        if not item_match:
            return None
            
        item_name = item_match.group(1)
        qty_match = re.search(self.re_number, text)
        qty = int(qty_match.group(1)) if qty_match else 1
        final_item_data = None
        for city in self.menu_data:
            for cat in self.menu_data[city]:
                if self.menu_data[city][cat]["name"].lower() == item_name:
                    final_item_data = {
                        "item": self.menu_data[city][cat]["name"],
                        "qty": qty,
                        "price": self.menu_data[city][cat]["price"],
                        "emoji": self.menu_data[city][cat]["emoji"]
                    }
                    break
        return final_item_data

    def parse_orders(self, full_text):
        """Memecah kalimat majemuk pesanan menjadi deretan objek terstruktur"""
        segments = re.split(self.re_split, full_text)
        found_orders = []
        for segment in segments:
            if segment.strip():
                order = self._parse_single_segment(segment)
                if order:
                    found_orders.append(order)
        return found_orders