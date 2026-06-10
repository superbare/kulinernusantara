import datetime

def get_navbar() -> str:
    
    return """<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>



<nav class="navbar navbar-expand-lg fixed-top premium-bs-navbar">

<div class="container">

<a class="navbar-brand custom-logo" href="#">NusaKuliner.</a>

<button class="navbar-toggler shadow-none border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

<span class="navbar-toggler-icon" style="filter: invert(1);"></span>

</button>

<div class="collapse navbar-collapse justify-content-end" id="navbarNav">

<ul class="navbar-nav gap-2 mt-3 mt-lg-0">

<li class="nav-item"><a class="nav-link custom-link" href="#section_sarapan">🥣 SARAPAN</a></li>

<li class="nav-item"><a class="nav-link custom-link" href="#section_siang">🍱 MAKAN SIANG</a></li>

<li class="nav-item"><a class="nav-link custom-link" href="#section_malam">🍢 MAKAN MALAM</a></li>

<li class="nav-item"><a class="nav-link custom-link" href="#section_ikonik">🥩 IKONIK</a></li>

<li class="nav-item"><a class="nav-link custom-link" href="#section_rempah">🌿 REMPAH</a></li>

</ul>

</div>

</div>

</nav>"""


def get_hero_section(img_src: str) -> str:
    utc_now = datetime.datetime.utcnow()
    wib_time = utc_now + datetime.timedelta(hours=7)
    hour = wib_time.hour
    
    if 4 <= hour < 11: sapaan = "SELAMAT PAGI"
    elif 11 <= hour < 15: sapaan = "SELAMAT SIANG"
    elif 15 <= hour < 18: sapaan = "SELAMAT SORE"
    else: sapaan = "SELAMAT MALAM"

    img_tag = f'<img src="{img_src}" class="hero-img" alt="Hero food" />' if img_src else '<div class="hero-img-placeholder"></div>'
    
    return f"""<section class='hero-section'>
<div class='hero-content'>
<span class='hero-eyebrow'>{sapaan} &mdash; NUSAKULINER</span>
<h1 class='hero-title'>Selamat<br>Datang</h1>
<p class='hero-desc'>Eksplorasi mendalam cita rasa autentik dari lima penjuru Nusantara — dipandu kecerdasan Finite State Machine yang memahami seleramu secara presisi.</p>
<a href='#section_sarapan' class='hero-cta'>Mulai Eksplorasi ↓</a>
</div>
<div class='hero-image-container'>
{img_tag}
<div class='hero-img-overlay'></div>
</div>
</section>"""

def get_section_start(section_id: str, title: str) -> str:
    return f"""<section id='{section_id}' class='section-container'>
<h2 class='section-title'>{title}</h2>
<div class='scrolling-wrapper'>"""

def get_food_card(lightbox_id: str, card_class: str, img_src: str, name: str, city: str, price: str) -> str:
    img_tag = f'<img src="{img_src}" alt="{name}">' if img_src else '<div class="food-img-placeholder"></div>'
    return f"""<a href='#{lightbox_id}' class='card-link' aria-label='{name}'>
<div class='{card_class}'>
<div class='food-img-box'>{img_tag}</div>
<div class='food-info'>
<span class='food-city'>{city}</span>
<div class='food-name'>{name}</div>
<div class='food-price'>{price}</div>
</div>
</div>
</a>"""

def get_lightbox_modal(lightbox_id: str, img_src: str, emoji: str, name: str, city: str, desc: str, price: str) -> str:
    img_tag = f'<img src="{img_src}" style="width:100%; height:100%; object-fit:cover; display:block;" alt="{name}">' if img_src else '<div class="food-img-placeholder"></div>'
    return f"""<div id='{lightbox_id}' class='lightbox-overlay' role='dialog' aria-modal='true'>
<a href='#' class='lightbox-close-area' aria-label='Tutup'></a>
<div class='lightbox-content'>
<a href='#' class='lightbox-close-btn' aria-label='Tutup'>&times;</a>
<div class='lightbox-img-wrap'>{img_tag}</div>
<div class='lightbox-caption'>
<h3>{emoji} {name}</h3>
<p class='lightbox-origin'>ASAL: {city}</p>
<p class='lightbox-desc'>{desc}</p>
<p class='lightbox-price'>{price}</p>
</div>
</div>
</div>"""

def get_section_end() -> str:
    return "</div></section>"

def get_spice_routes() -> str:
    return """<section id='section_rempah' class='section-container'>
<h2 class='section-title'>🌿 Filosofi Jalur Rempah Nusantara</h2>
<div class='container-fluid px-0 mt-4'>
<div class='row g-4'>
<div class='col-12 col-md-6 col-xl-3'>
<div class='rempah-card'>
<span class='rempah-badge'>WILAYAH JAWA</span>
<h5 class='rempah-title'>Dominasi: Ketumbar, Jinten, Gula Aren.</h5>
<p class='rempah-desc'>Kehangatan tradisi lewat perpaduan rasa manis-gurih lembut yang berakar dari akulturasi budaya pedalaman Jawa.</p>
</div>
</div>
<div class='col-12 col-md-6 col-xl-3'>
<div class='rempah-card'>
<span class='rempah-badge'>WILAYAH SUMATRA</span>
<h5 class='rempah-title'>Dominasi: Lada, Pala, Kapulaga, Kunyit.</h5>
<p class='rempah-desc'>Ketegasan cita rasa pesisir maritim yang berani lewat kuah kental beraroma tajam dan bumbu pekat berkarakter.</p>
</div>
</div>
<div class='col-12 col-md-6 col-xl-3'>
<div class='rempah-card'>
<span class='rempah-badge'>WILAYAH KALIMANTAN</span>
<h5 class='rempah-title'>Dominasi: Asam Kandis, Daun Kesum, Terasi.</h5>
<p class='rempah-desc'>Kesegaran wilayah perairan sungai besar lewat cita rasa gurih-asam eksotis yang menggugah selera.</p>
</div>
</div>
<div class='col-12 col-md-6 col-xl-3'>
<div class='rempah-card'>
<span class='rempah-badge'>WILAYAH PAPUA</span>
<h5 class='rempah-title'>Dominasi: Kenari, Jahe Hutan, Kunyit Alam.</h5>
<p class='rempah-desc'>Kemurnian ikatan alam timur yang bersahaja lewat teknik pengolahan minimalis yang menjaga keaslian nutrisi asli.</p>
</div>
</div>
</div>
</div>
</section>"""

def get_footer() -> str:
    return """<footer class='custom-footer'>
<p class='text-muted m-0'>© 2026 Projek Akhir Teori Bahasa dan Otomata — Jalur Eksplorasi Kuliner Nusantara Terkontrol</p>
</footer>"""

def get_phone_chassis_start(position_class: str = "phone-chassis") -> str:
    return f"""<div class='{position_class}'>
<div class='phone-side-button volume-up'></div>
<div class='phone-side-button volume-down'></div>
<div class='phone-side-button power-btn'></div>
<div class='dynamic-island'></div>
<div class='phone-screen-header'>NUSA-BOT ASSISTANT</div>
<div class='phone-chat-scrollview' id='chat-scroll'>"""

def get_chat_bubble(role: str, content: str) -> str:
    bubble_class = "bubble-user-style" if role == "user" else "bubble-bot-style"
    return f"<div class='chat-bubble-wrap {bubble_class}'>{content}</div>"

def get_phone_chassis_end() -> str:
    return """</div><div class='home-indicator'></div></div>"""