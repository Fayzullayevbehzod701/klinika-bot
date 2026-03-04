import telebot
from telebot import types
import sqlite3
from datetime import datetime, timedelta
import os
import threading
from flask import Flask

# Flask server - Render port talab qiladi
app = Flask(__name__)


@app.route('/')
def index():
    return "Bot ishlayapti!"


@app.route('/health')
def health():
    return "OK"


# Botni alohida threadda ishga tushirish
def run_bot():
    bot.infinity_polling()




    # Botni threadda ishga tushirish
    threading.Thread(target=run_bot, daemon=True).start()

    # Flask serverni ishga tushirish
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# TOKEN - o'zingizning tokeningizni qo'ying
TOKEN = '8688973963:AAG5HU8YeACMfiKKYy6_MbdCAHAvniBjFaQ'  # O'ZINGIZNING TOKENINGIZ
bot = telebot.TeleBot(TOKEN)

# Ma'lumotlar bazasiga ulanish
conn = sqlite3.connect('toshkent_klinikalar.db', check_same_thread=False)
cursor = conn.cursor()

# Tumanlar jadvali
cursor.execute('''
CREATE TABLE IF NOT EXISTS tumanlar (
    id INTEGER PRIMARY KEY,
    nomi TEXT UNIQUE
)
''')

# Muassasalar jadvali
cursor.execute('''
CREATE TABLE IF NOT EXISTS muassasalar (
    id INTEGER PRIMARY KEY,
    tuman_id INTEGER,
    nomi TEXT,
    turi TEXT,
    manzili TEXT,
    tel TEXT,
    ish_vaqti TEXT,
    qoshimcha TEXT,
    UNIQUE(tuman_id, nomi)  -- Bir tumanda bir nomdagi muassasa faqat bir marta
)
''')

# Shifokorlar jadvali
cursor.execute('''
CREATE TABLE IF NOT EXISTS shifokorlar (
    id INTEGER PRIMARY KEY,
    muassasa_id INTEGER,
    ismi TEXT,
    mutaxassisligi TEXT,
    malakasi TEXT,
    qoshimcha TEXT,
    UNIQUE(muassasa_id, ismi)  -- Bir muassasada bir shifokor faqat bir marta
)
''')

# Vaqtlar jadvali
cursor.execute('''
CREATE TABLE IF NOT EXISTS vaqtlar (
    id INTEGER PRIMARY KEY,
    shifokor_id INTEGER,
    sana TEXT,
    soat TEXT,
    bandmi INTEGER DEFAULT 0,
    UNIQUE(shifokor_id, sana, soat)  -- Bir shifokorga bir vaqt faqat bir marta
)
''')

# Bronlar jadvali
cursor.execute('''
CREATE TABLE IF NOT EXISTS bronlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vaqt_id INTEGER,
    user_id INTEGER,
    ism TEXT,
    telefon TEXT,
    yozilgan_vaqt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# TUMANLARNI TO'LDIRISH (agar bo'sh bo'lsa)
cursor.execute("SELECT COUNT(*) FROM tumanlar")
if cursor.fetchone()[0] == 0:
    tumanlar = [
        "Yunusobod", "Yashnobod", "Shayxontohur", "Mirobod",
        "Mirzo Ulug'bek", "Chilonzor", "Olmazor", "Uchtepa",
        "Yakkasaroy", "Sergeli", "Bektemir", "Yangihayot"
    ]
    for tuman in tumanlar:
        cursor.execute("INSERT INTO tumanlar (nomi) VALUES (?)", (tuman,))
    print("✅ Tumanlar qo'shildi")

# MUASSASALARNI TO'LDIRISH (agar bo'sh bo'lsa)
cursor.execute("SELECT COUNT(*) FROM muassasalar")
if cursor.fetchone()[0] == 0:
    # YUNUSOBOD
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Yunusobod'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "7-son Shahar tez yordam shifoxonasi", "shifoxona", "Yunusobod tumani", "+99871...", "24/7", "tumanlararo markaz maqomiga ega"),
        (tuman_id, "56-sonli oilaviy poliklinika", "poliklinika", "Kazitarnov ko'chasi, 2-uy, 9", "+99871...", "08:00-20:00", "TATU talabalari va xodimlariga xizmat"),
        (tuman_id, "50-sonli oilaviy poliklinika", "poliklinika", "Minor massivi, 120-uy", "+99871...", "08:00-20:00", ""),
        (tuman_id, "5-Stomatologiya", "stomatologiya", "Firdavsiy mahallasi", "+99871...", "09:00-18:00", "")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # YASHNOBOD
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Yashnobod'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "4-son Shahar tez yordam shifoxonasi", "shifoxona", "Yashnobod tumani", "+99871...", "24/7", "tumanlararo markaz maqomiga ega"),
        (tuman_id, "Bolalar milliy tibbiyot markazi", "shifoxona", "Aviasozlar 29", "+99871...", "24/7", "280 o'rin, 100+ shifokor, Koreya bilan hamkorlik"),
        (tuman_id, "Gorodskaya Detskaya Klinicheskaya bolnitsa № 2", "shifoxona", "Yashnobod tumani", "+99871...", "24/7", "Shahar bolalar klinik shifoxonasi"),
        (tuman_id, "27-sonli oilaviy poliklinika", "poliklinika", "Jarqo'rg'on mahallasi", "+99871...", "08:00-20:00", "31 967 aholiga xizmat")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # SHAYXONTOHUR
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Shayxontohur'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "1-son Shahar tez yordam shifoxonasi", "shifoxona", "Shayxontohur tumani", "+99871...", "24/7", "tumanlararo markaz maqomiga ega"),
        (tuman_id, "4-son bolalar klinik shifoxonasi", "shifoxona", "Shayxontohur tumani", "+99871...", "24/7", "140 o'rin, 24 nafar shifokor"),
        (tuman_id, "42-son oilaviy poliklinika", "poliklinika", "Taxtapul ko'chasi, 14-a uy", "+99871...", "08:00-20:00", ""),
        (tuman_id, "InSmile Family Dental Clinic", "stomatologiya", "Aloqa dahasi, 9", "+998 99 720 20 20", "09:00-18:00", "jarrohlik, estetik stomatologiya, implantologiya, breketlar")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # MIROBOD
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Mirobod'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "Ruhiy kasalliklar klinik shifoxonasi", "shifoxona", "Mehrjon ko'chasi 35", "+99871...", "24/7", ""),
        (tuman_id, "Shox Med Centre", "shifoxona", "Aybek ko'chasi 34", "+99871...", "24/7", "MRI, MSKT, endoskopiya"),
        (tuman_id, "Tibbiy xodimlar malakasini rivojlantirish markazi ko'p tarmoqli klinikasi", "poliklinika", "S.Azimov ko'chasi 74", "+99871...", "09:00-18:00", "O'quv klinikasi")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # MIRZO ULUG'BEK
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Mirzo Ulug''bek'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "Respublika akusherlik va ginekologiya markazi", "shifoxona", "M. Ulug'bek ko'chasi 132a", "+99871...", "24/7", "")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # CHILONZOR
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Chilonzor'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "Respublika gematologiya va qon quyish markazi", "shifoxona", "Arnasoy ko'chasi, 81", "+99871...", "24/7", ""),
        (tuman_id, "Toshkent shahar ftiziatriya va pulmonologiya markazi", "poliklinika", "Lutfiy 7, 33-uy", "+99871...", "09:00-18:00", "")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # OLMAZOR
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Olmazor'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "Emergency Center", "shifoxona", "Oltinsoy mahallasi", "+99871...", "24/7", ""),
        (tuman_id, "Respublika urologiya markazi", "shifoxona", "Shifokorlar ko'chasi, 7", "+99871...", "24/7", ""),
        (tuman_id, "Sinomed ko'p tarmoqli klinikasi", "shifoxona", "Olmazor tumani", "+99871...", "24/7", "$30 mln, 80+ shifokor, tug'ruq kompleksi"),
        (tuman_id, "Talabalar shaharchasi markaziy ko'p tarmoqli poliklinikasi", "poliklinika", "Talabalar shaharchasi, 95-uy", "+99871...", "09:00-18:00", "")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # UCHTEPA
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Uchtepa'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "Uchtepa Shahar tez yordam shifoxonasi", "shifoxona", "Uchtepa tumani", "+99871...", "24/7", "tumanlararo markaz maqomiga ega"),
        (tuman_id, "23-son oilaviy poliklinika Birlik filiali", "poliklinika", "Chakmoniy ko'chasi, 14-a uy", "+99871...", "08:00-20:00", "")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # YAKKASAROY
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Yakkasaroy'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "58-son oilaviy poliklinika", "poliklinika", "A.Qahhor ko'chasi, 44-uy", "+99871...", "08:00-20:00", ""),
        (tuman_id, "Bazami-medical", "poliklinika", "Rakatboshi mahallasi", "+99871...", "09:00-18:00", "")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # SERGELI
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Sergeli'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "11-son oilaviy poliklinika", "poliklinika", "Choshtepa ko'chasi, 147-uy", "+99871...", "08:00-20:00", "")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # BEKTEMIR
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Bektemir'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "Bektemir tuman markaziy ko'p tarmoqli poliklinikasi", "poliklinika", "Vodnik dahasi, 75-uy", "+99871...", "08:00-20:00", "")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    # YANGIHAYOT
    cursor.execute("SELECT id FROM tumanlar WHERE nomi='Yangihayot'")
    tuman_id = cursor.fetchone()[0]
    muassasalar_data = [
        (tuman_id, "Toshkent shahar teri-tanosil dispanseri", "dispanser", "Yo'ldosh 7, 23-uy", "+99871...", "09:00-18:00", "")
    ]
    for muassasa in muassasalar_data:
        cursor.execute('''
            INSERT INTO muassasalar (tuman_id, nomi, turi, manzili, tel, ish_vaqti, qoshimcha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', muassasa)

    print("✅ Muassasalar qo'shildi")

# SHIFOKORLARNI TO'LDIRISH (agar bo'sh bo'lsa)
cursor.execute("SELECT COUNT(*) FROM shifokorlar")
if cursor.fetchone()[0] == 0:
    # MUASSASALAR ID LARINI OLISH
    cursor.execute("SELECT id, nomi FROM muassasalar")
    muassasalar = cursor.fetchall()

    # Muassasa nomi bo'yicha ID larni lug'at ko'rinishida saqlash
    muassasa_ids = {}
    for id, nom in muassasalar:
        muassasa_ids[nom] = id

    shifokorlar_data = [
        # ===== YUNUSOBOD =====
        # 7-son Shahar tez yordam shifoxonasi
        (muassasa_ids.get("7-son Shahar tez yordam shifoxonasi"), "Prof. Karimov Aziz", "Kardioxirurg",
         "Tibbiyot fanlari doktori", "30 yil tajriba"),
        (muassasa_ids.get("7-son Shahar tez yordam shifoxonasi"), "Prof. Aliyev Bobur", "Jarroh", "Oliy toifa",
         "25 yil tajriba"),
        (muassasa_ids.get("7-son Shahar tez yordam shifoxonasi"), "Dr. Raximov Sherzod", "Travmatolog", "1-toifa",
         "15 yil tajriba"),
        (muassasa_ids.get("7-son Shahar tez yordam shifoxonasi"), "Dr. Yusupova Nilufar", "Anesteziolog", "Oliy toifa",
         "20 yil tajriba"),

        # 56-sonli oilaviy poliklinika
        (muassasa_ids.get("56-sonli oilaviy poliklinika"), "Dr. Abdurahmonova Malika", "Oila shifokori", "Oliy toifa",
         "25 yil tajriba"),
        (muassasa_ids.get("56-sonli oilaviy poliklinika"), "Dr. Hakimov Alisher", "Terapevt", "1-toifa",
         "18 yil tajriba"),
        (muassasa_ids.get("56-sonli oilaviy poliklinika"), "Dr. Ismoilova Munisa", "Pediatr", "Oliy toifa",
         "22 yil tajriba"),

        # 50-sonli oilaviy poliklinika
        (muassasa_ids.get("50-sonli oilaviy poliklinika"), "Dr. Rasulova Mohira", "Ginekolog", "1-toifa",
         "15 yil tajriba"),
        (muassasa_ids.get("50-sonli oilaviy poliklinika"), "Dr. Xolmatov Bahrom", "Stomatolog", "Oliy toifa",
         "20 yil tajriba"),

        # 5-Stomatologiya
        (muassasa_ids.get("5-Stomatologiya"), "Dr. Karimova Dilnoza", "Stomatolog-terapevt", "1-toifa",
         "12 yil tajriba"),
        (muassasa_ids.get("5-Stomatologiya"), "Dr. Tursunov Jamshid", "Stomatolog-ortoped", "Oliy toifa",
         "18 yil tajriba"),

        # ===== YASHNOBOD =====
        # 4-son Shahar tez yordam shifoxonasi
        (muassasa_ids.get("4-son Shahar tez yordam shifoxonasi"), "Prof. Xodjayev Shuxrat", "Neyroxirurg",
         "Tibbiyot fanlari doktori", "30 yil tajriba"),
        (muassasa_ids.get("4-son Shahar tez yordam shifoxonasi"), "Dr. Abdullayev Rustam", "Reanimatolog", "Oliy toifa",
         "20 yil tajriba"),

        # Bolalar milliy tibbiyot markazi
        (muassasa_ids.get("Bolalar milliy tibbiyot markazi"), "Prof. Yunusov Rustam", "Pediatr-neonatolog",
         "Tibbiyot fanlari doktori", "Koreyada malaka oshirgan"),
        (muassasa_ids.get("Bolalar milliy tibbiyot markazi"), "Prof. Karimova Malika", "Bolalar neyroxirurgi",
         "Tibbiyot fanlari doktori", "Pusan universiteti"),
        (muassasa_ids.get("Bolalar milliy tibbiyot markazi"), "Dr. Umarova Zulfiya", "Bolalar onkologi",
         "1-toifa shifokor", "15 yil tajriba"),
        (muassasa_ids.get("Bolalar milliy tibbiyot markazi"), "Dr. Jalilova Sabina", "Pediatr", "Oliy toifa",
         "20 yil tajriba"),
        (muassasa_ids.get("Bolalar milliy tibbiyot markazi"), "Dr. Sobirov Dilshod", "Bolalar kardioxirurgi",
         "Oliy toifa", "Seul milliy universiteti"),

        # Gorodskaya Detskaya Klinicheskaya bolnitsa № 2
        (muassasa_ids.get("Gorodskaya Detskaya Klinicheskaya bolnitsa № 2"), "Dr. Mirzayeva Dilnoza",
         "Bolalar shifokori", "Oliy toifa", "25 yil tajriba"),
        (muassasa_ids.get("Gorodskaya Detskaya Klinicheskaya bolnitsa № 2"), "Dr. Komilova Nargiza",
         "Bolalar nevrologi", "1-toifa", "18 yil tajriba"),

        # 27-sonli oilaviy poliklinika
        (muassasa_ids.get("27-sonli oilaviy poliklinika"), "Dr. Toshmatova Gulnora", "Oila shifokori", "Oliy toifa",
         "28 yil tajriba"),
        (muassasa_ids.get("27-sonli oilaviy poliklinika"), "Dr. Akbarova Shahnoza", "Pediatr", "1-toifa",
         "12 yil tajriba"),

        # ===== SHAYXONTOHUR =====
        # 1-son Shahar tez yordam shifoxonasi
        (muassasa_ids.get("1-son Shahar tez yordam shifoxonasi"), "Prof. Nishonova Dilorom", "LOR",
         "Tibbiyot fanlari doktori", "35 yil tajriba"),
        (muassasa_ids.get("1-son Shahar tez yordam shifoxonasi"), "Dr. Xalilov Farrux", "Otiatr", "Oliy toifa",
         "22 yil tajriba"),

        # 4-son bolalar klinik shifoxonasi
        (muassasa_ids.get("4-son bolalar klinik shifoxonasi"), "Akilova Feruza", "Bosh shifokor", "Oliy toifa",
         "4-son bolalar shifoxonasi"),
        (muassasa_ids.get("4-son bolalar klinik shifoxonasi"), "Dr. Karimova Zuxra", "Pediatr", "1-toifa",
         "20 yil tajriba"),

        # 42-son oilaviy poliklinika
        (muassasa_ids.get("42-son oilaviy poliklinika"), "Dr. Usmonova Kamola", "Oftalmolog", "Oliy toifa",
         "20 yil tajriba"),
        (muassasa_ids.get("42-son oilaviy poliklinika"), "Dr. Hamrayev Baxrom", "Oftalmolog", "Professor",
         "32 yil tajriba"),

        # InSmile Family Dental Clinic
        (muassasa_ids.get("InSmile Family Dental Clinic"), "Dr. Orifjonov Orif", "Stomatolog", "Oliy toifa",
         "Implantologiya"),
        (muassasa_ids.get("InSmile Family Dental Clinic"), "Dr. Akmalova Saida", "Ortodont", "1-toifa", "Breketlar"),

        # ===== MIROBOD =====
        # Ruhiy kasalliklar klinik shifoxonasi
        (muassasa_ids.get("Ruhiy kasalliklar klinik shifoxonasi"), "Prof. Turaev Bobir", "Psixiatr",
         "Tibbiyot fanlari doktori", "40 yil tajriba"),

        # Shox Med Centre
        (muassasa_ids.get("Shox Med Centre"), "Dr. G'ofurova Feruza", "Ginekolog", "Professor", "TIPME"),
        (muassasa_ids.get("Shox Med Centre"), "Dr. Asatova Munira", "Akusher", "Professor", "50 yillik tajriba"),
        (muassasa_ids.get("Shox Med Centre"), "Dr. Artixodjaeva Guzal", "Nevrolog", "PhD", "15 yil tajriba"),

        # Tibbiy xodimlar malakasini rivojlantirish markazi
        (muassasa_ids.get("Tibbiy xodimlar malakasini rivojlantirish markazi ko'p tarmoqli klinikasi"),
         "Prof. Xujanazarov Ilhom", "Travmatolog", "Professor", "TTA"),
        (muassasa_ids.get("Tibbiy xodimlar malakasini rivojlantirish markazi ko'p tarmoqli klinikasi"),
         "Prof. Asilova Saodat", "Ortoped", "Professor", "TTA"),

        # ===== MIRZO ULUG'BEK =====
        # Respublika akusherlik va ginekologiya markazi
        (muassasa_ids.get("Respublika akusherlik va ginekologiya markazi"), "Prof. G'ofurova Feruza",
         "Akusher-ginekolog", "Professor, kafedra mudiri", "TIPME"),
        (muassasa_ids.get("Respublika akusherlik va ginekologiya markazi"), "Prof. Asatova Munira", "Akusher-ginekolog",
         "Professor, fan doktori", "50 yillik tajriba"),
        (muassasa_ids.get("Respublika akusherlik va ginekologiya markazi"), "Prof. Yeshimbetova Gulsara", "Ginekolog",
         "Professor", "TIPME"),
        (muassasa_ids.get("Respublika akusherlik va ginekologiya markazi"), "Dr. Isanbayeva Landish", "Akusher",
         "PhD, dotsent", "20 yil tajriba"),
        (muassasa_ids.get("Respublika akusherlik va ginekologiya markazi"), "Dr. Jalolov Uktam", "Ginekolog",
         "PhD, dotsent", "18 yil tajriba"),

        # ===== CHILONZOR =====
        # Respublika gematologiya va qon quyish markazi
        (muassasa_ids.get("Respublika gematologiya va qon quyish markazi"), "Prof. Alixodjaeva Gulnaraxon", "Gematolog",
         "Professor", "TTA"),
        (muassasa_ids.get("Respublika gematologiya va qon quyish markazi"), "Dr. Kosimov A'zam", "Gematolog",
         "PhD, dotsent", "15 yil tajriba"),

        # Toshkent shahar ftiziatriya va pulmonologiya markazi
        (muassasa_ids.get("Toshkent shahar ftiziatriya va pulmonologiya markazi"), "Dr. Boboyev Bekzod", "Pulmonolog",
         "Assistant", "10 yil tajriba"),

        # ===== OLMAZOR =====
        # Emergency Center
        (muassasa_ids.get("Emergency Center"), "Prof. Tursunov Sherzod", "Reanimatolog", "Professor", "25 yil tajriba"),

        # Respublika urologiya markazi
        (muassasa_ids.get("Respublika urologiya markazi"), "Prof. Aliyev Aziz", "Urolog", "Professor",
         "30 yil tajriba"),

        # Sinomed ko'p tarmoqli klinikasi
        (muassasa_ids.get("Sinomed ko'p tarmoqli klinikasi"), "Dr. Karimov Botir", "Kardiolog", "Oliy toifa",
         "20 yil tajriba"),
        (muassasa_ids.get("Sinomed ko'p tarmoqli klinikasi"), "Dr. Raxmonova Nilufar", "Endokrinolog", "1-toifa",
         "15 yil tajriba"),

        # Talabalar shaharchasi poliklinikasi
        (muassasa_ids.get("Talabalar shaharchasi markaziy ko'p tarmoqli poliklinikasi"), "Dr. Jalilov Abdulla",
         "Terapevt", "Oliy toifa", "25 yil tajriba"),

        # ===== UCHTEPA =====
        # Uchtepa Shahar tez yordam shifoxonasi
        (muassasa_ids.get("Uchtepa Shahar tez yordam shifoxonasi"), "Dr. Xasanov Shuxrat", "Jarroh", "Oliy toifa",
         "22 yil tajriba"),

        # 23-son oilaviy poliklinika
        (muassasa_ids.get("23-son oilaviy poliklinika Birlik filiali"), "Dr. Karimova Malika", "Oila shifokori",
         "1-toifa", "18 yil tajriba"),

        # ===== YAKKASAROY =====
        # 58-son oilaviy poliklinika
        (muassasa_ids.get("58-son oilaviy poliklinika"), "Dr. Yusupov Jamshid", "Terapevt", "Oliy toifa",
         "20 yil tajriba"),

        # Bazami-medical
        (muassasa_ids.get("Bazami-medical"), "Dr. Sodiqova Nigora", "Dermatolog", "1-toifa", "15 yil tajriba"),

        # ===== SERGELI =====
        # 11-son oilaviy poliklinika
        (muassasa_ids.get("11-son oilaviy poliklinika"), "Dr. Turg'unov Anvar", "Oila shifokori", "Oliy toifa",
         "25 yil tajriba"),

        # ===== BEKTEMIR =====
        # Bektemir tuman markaziy poliklinikasi
        (muassasa_ids.get("Bektemir tuman markaziy ko'p tarmoqli poliklinikasi"), "Dr. Norboyev Rustam", "Terapevt",
         "1-toifa", "18 yil tajriba"),

        # ===== YANGIHAYOT =====
        # Toshkent shahar teri-tanosil dispanseri
        (muassasa_ids.get("Toshkent shahar teri-tanosil dispanseri"), "Dr. Xaydarov Elyor", "Dermatovenerolog",
         "Oliy toifa", "20 yil tajriba"),
    ]

    # Shifokorlarni qo'shish
    for shifokor in shifokorlar_data:
        if shifokor[0]:  # Agar muassasa ID topilgan bo'lsa
            try:
                cursor.execute('''
                    INSERT INTO shifokorlar (muassasa_id, ismi, mutaxassisligi, malakasi, qoshimcha)
                    VALUES (?, ?, ?, ?, ?)
                ''', shifokor)
            except:
                pass  # Agar shifokor avval qo'shilgan bo'lsa, o'tkazib yubor

    print(f"✅ {len(shifokorlar_data)} ta shifokor qo'shildi")
# Vaqtlar yaratish (3 kun uchun)
cursor.execute("SELECT COUNT(*) FROM vaqtlar")
if cursor.fetchone()[0] == 0:
    bugun = datetime.now().strftime('%Y-%m-%d')
    ertaga = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    indin = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')

    vaqtlar = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00']

    # Har bir shifokor uchun vaqtlar
    cursor.execute("SELECT id FROM shifokorlar")
    shifokor_ids = cursor.fetchall()
    for shifokor_id in shifokor_ids:
        for sana in [bugun, ertaga, indin]:
            for soat in vaqtlar:
                try:
                    cursor.execute('''
                        INSERT INTO vaqtlar (shifokor_id, sana, soat, bandmi)
                        VALUES (?, ?, ?, 0)
                    ''', (shifokor_id[0], sana, soat))
                except:
                    pass  # Agar vaqt avval qo'shilgan bo'lsa, o'tkazib yubor

    print("✅ Vaqtlar qo'shildi")

conn.commit()
print("✅ Toshkent shahri tibbiyot muassasalari bazaga yozildi!")


# ASOSIY BOT FUNKSIYALARI

# Asosiy menyu
def asosiy_menyu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('🏥 Tuman tanlash'),
        types.KeyboardButton('📋 Mening navbatlarim')
    )
    markup.add(
        types.KeyboardButton('🔍 Qidirish'),
        types.KeyboardButton('📞 Aloqa')
    )
    markup.add(
        types.KeyboardButton('ℹ️ Bot haqida')
    )
    return markup


# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"👋 Assalomu alaykum, {message.from_user.first_name}!\n\n"
        f"🏥 **Toshkent shahar tibbiyot muassasalari** botiga xush kelibsiz.\n\n"
        f"📊 **Botda:**\n"
        f"• 12 ta tuman\n"
        f"• 30+ klinika va shifoxona\n"
        f"• 50+ malakali shifokor\n\n"
        f"Quyidagi tugmalardan birini tanlang:",
        reply_markup=asosiy_menyu(),
        parse_mode='Markdown'
    )


# Tuman tanlash
@bot.message_handler(func=lambda message: message.text == '🏥 Tuman tanlash')
def tuman_tanlash(message):
    cursor.execute("SELECT id, nomi FROM tumanlar ORDER BY nomi")
    tumanlar = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=2)
    for tuman in tumanlar:
        markup.add(types.InlineKeyboardButton(
            tuman[1],
            callback_data=f"tuman_{tuman[0]}"
        ))

    bot.send_message(
        message.chat.id,
        "🏙️ **Tumanni tanlang:**",
        reply_markup=markup,
        parse_mode='Markdown'
    )


# Tuman tanlanganda muassasa turi tanlash
@bot.callback_query_handler(func=lambda call: call.data.startswith('tuman_'))
def muassasa_turi_tanlash(call):
    tuman_id = int(call.data.split('_')[1])

    # Tumandagi muassasalar soni
    cursor.execute("""
        SELECT turi, COUNT(*) FROM muassasalar 
        WHERE tuman_id = ? GROUP BY turi
    """, (tuman_id,))
    tur_sonlari = cursor.fetchall()

    if not tur_sonlari:
        bot.answer_callback_query(call.id, "Bu tumanda muassasa yo'q")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)

    tur_kodlari = {
        'shifoxona': '🏨 Shifoxonalar',
        'poliklinika': '🏥 Poliklinikalar',
        'stomatologiya': '🦷 Stomatologiyalar',
        'dispanser': '🏥 Dispanserlar'
    }

    for tur, son in tur_sonlari:
        if tur in tur_kodlari:
            markup.add(types.InlineKeyboardButton(
                f"{tur_kodlari[tur]} ({son} ta)",
                callback_data=f"tur_{tuman_id}_{tur}"
            ))

    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_tumanlar"))

    bot.edit_message_text(
        "🏥 **Muassasa turini tanlang:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# Muassasa turi tanlanganda ro'yxat
@bot.callback_query_handler(func=lambda call: call.data.startswith('tur_'))
def muassasalar_royxati(call):
    parts = call.data.split('_')
    tuman_id = int(parts[1])
    tur = parts[2]

    cursor.execute("""
        SELECT id, nomi, manzili FROM muassasalar 
        WHERE tuman_id = ? AND turi = ?
        ORDER BY nomi
    """, (tuman_id, tur))
    muassasalar = cursor.fetchall()

    if not muassasalar:
        bot.answer_callback_query(call.id, "Bu tumanda bunday muassasa yo'q")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for muassasa in muassasalar:
        nom_qisqa = muassasa[1][:35] + "..." if len(muassasa[1]) > 35 else muassasa[1]
        markup.add(types.InlineKeyboardButton(
            nom_qisqa,
            callback_data=f"muassasa_{muassasa[0]}"
        ))

    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data=f"orqaga_tur_{tuman_id}"))

    tur_nomi = {
        'shifoxona': '🏨 Shifoxonalar',
        'poliklinika': '🏥 Poliklinikalar',
        'stomatologiya': '🦷 Stomatologiyalar',
        'dispanser': '🏥 Dispanserlar'
    }.get(tur, tur)

    bot.edit_message_text(
        f"{tur_nomi} ro'yxati:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# MUASSASA TANLANGANDA SHIFOKORLAR RO'YXATI
@bot.callback_query_handler(func=lambda call: call.data.startswith('muassasa_'))
def shifokorlar_royxati(call):
    muassasa_id = int(call.data.split('_')[1])

    # Muassasa ma'lumotlarini olish (tuman_id ni ham olamiz)
    cursor.execute("SELECT nomi, manzili, tuman_id FROM muassasalar WHERE id = ?", (muassasa_id,))
    muassasa = cursor.fetchone()
    muassasa_nomi = muassasa[0]
    muassasa_manzili = muassasa[1]
    tuman_id = muassasa[2]

    # Shu muassasadagi shifokorlarni olish
    cursor.execute("""
        SELECT id, ismi, mutaxassisligi, malakasi 
        FROM shifokorlar 
        WHERE muassasa_id = ?
        ORDER BY ismi
    """, (muassasa_id,))
    shifokorlar = cursor.fetchall()

    if not shifokorlar:
        bot.answer_callback_query(call.id, "Bu muassasada hozircha shifokorlar yo'q")
        return

    # Tugmalar yaratish
    markup = types.InlineKeyboardMarkup(row_width=1)
    for shifokor in shifokorlar:
        markup.add(types.InlineKeyboardButton(
            f"👨‍⚕️ {shifokor[1]} - {shifokor[2]}",
            callback_data=f"shifokor_{shifokor[0]}"
        ))

    # Orqaga tugmasi
    markup.add(types.InlineKeyboardButton(
        "⬅️ Orqaga",
        callback_data=f"orqaga_tur_{tuman_id}"
    ))

    # Xabarni yangilash
    bot.edit_message_text(
        f"🏥 **{muassasa_nomi}**\n📍 {muassasa_manzili}\n\n"
        f"👨‍⚕️ **Shifokorlar ({len(shifokorlar)} nafar):**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# SHIFOKOR TANLANGANDA
@bot.callback_query_handler(func=lambda call: call.data.startswith('shifokor_'))
def shifokor_haqida(call):
    shifokor_id = int(call.data.split('_')[1])

    # Shifokor va muassasa ma'lumotlarini olish
    cursor.execute("""
        SELECT s.ismi, s.mutaxassisligi, s.malakasi, s.qoshimcha,
               m.nomi, m.manzili, m.tel, m.id
        FROM shifokorlar s
        JOIN muassasalar m ON s.muassasa_id = m.id
        WHERE s.id = ?
    """, (shifokor_id,))
    shifokor = cursor.fetchone()

    muassasa_id = shifokor[7]

    # Bo'sh vaqtlarni olish
    cursor.execute("""
        SELECT id, sana, soat FROM vaqtlar 
        WHERE shifokor_id = ? AND bandmi = 0 
        ORDER BY sana, soat
        LIMIT 8
    """, (shifokor_id,))
    vaqtlar = cursor.fetchall()

    # Tugmalar yaratish
    markup = types.InlineKeyboardMarkup(row_width=2)

    if vaqtlar:
        for vaqt in vaqtlar:
            # Sanani formatlash (2025-03-15 -> 15.03)
            sana_qism = vaqt[1][8:10] + '.' + vaqt[1][5:7]
            markup.add(types.InlineKeyboardButton(
                f"📅 {sana_qism} ⏰ {vaqt[2]}",
                callback_data=f"vaqt_{vaqt[0]}"
            ))
    else:
        markup.add(types.InlineKeyboardButton(
            "❌ Bo'sh vaqtlar yo'q",
            callback_data="none"
        ))

    # Orqaga tugmasi
    markup.add(types.InlineKeyboardButton(
        "⬅️ Orqaga",
        callback_data=f"orqaga_shifokorlar_{muassasa_id}"
    ))

    # Xabar matni
    text = f"👨‍⚕️ **{shifokor[0]}**\n"
    text += f"🏥 **Mutaxassislik:** {shifokor[1]}\n"
    text += f"⭐ **Malaka:** {shifokor[2]}\n"
    if shifokor[3]:
        text += f"ℹ️ **Qo'shimcha:** {shifokor[3]}\n"
    text += f"\n🏥 **Muassasa:** {shifokor[4]}\n"
    text += f"📍 **Manzil:** {shifokor[5]}\n"
    if shifokor[6]:
        text += f"📞 **Tel:** {shifokor[6]}\n"
    text += f"\n⏰ **Bo'sh vaqtlar:**"

    # Xabarni yangilash
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# VAQT TANLANGANDA
@bot.callback_query_handler(func=lambda call: call.data.startswith('vaqt_'))
def vaqt_tanlandi(call):
    vaqt_id = int(call.data.split('_')[1])

    # Vaqt ma'lumotlarini olish
    cursor.execute("""
        SELECT v.sana, v.soat, s.ismi, m.nomi, v.shifokor_id
        FROM vaqtlar v
        JOIN shifokorlar s ON v.shifokor_id = s.id
        JOIN muassasalar m ON s.muassasa_id = m.id
        WHERE v.id = ?
    """, (vaqt_id,))
    malumot = cursor.fetchone()

    shifokor_id = malumot[4]

    # Tasdiqlash tugmalari
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "✅ Tasdiqlash",
            callback_data=f"tasdiq_{vaqt_id}"
        ),
        types.InlineKeyboardButton(
            "❌ Bekor qilish",
            callback_data=f"bekor_vaqt_{vaqt_id}_{shifokor_id}"
        )
    )

    bot.edit_message_text(
        f"📋 **Tanlangan vaqt:**\n\n"
        f"👨‍⚕️ **Shifokor:** {malumot[2]}\n"
        f"🏥 **Muassasa:** {malumot[3]}\n"
        f"📅 **Sana:** {malumot[0]}\n"
        f"⏰ **Vaqt:** {malumot[1]}\n\n"
        f"✅ **Tasdiqlash** tugmasini bosing:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# VAQTNI TASDIQLASH
@bot.callback_query_handler(func=lambda call: call.data.startswith('tasdiq_'))
def tasdiqlash(call):
    vaqt_id = int(call.data.split('_')[1])

    # Foydalanuvchi ismini so'rash
    msg = bot.send_message(
        call.message.chat.id,
        "✏️ Iltimos, **ismingizni** kiriting:",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, ism_olish, vaqt_id)


def ism_olish(message, vaqt_id):
    ism = message.text
    msg = bot.send_message(
        message.chat.id,
        "📞 Iltimos, **telefon raqamingizni** kiriting (masalan: +998901234567):",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, telefon_olish, vaqt_id, ism)


def telefon_olish(message, vaqt_id, ism):
    telefon = message.text
    user_id = message.from_user.id

    # Vaqtni band qilish
    cursor.execute("UPDATE vaqtlar SET bandmi = 1 WHERE id = ?", (vaqt_id,))

    # Bronni saqlash
    cursor.execute("""
        INSERT INTO bronlar (vaqt_id, user_id, ism, telefon)
        VALUES (?, ?, ?, ?)
    """, (vaqt_id, user_id, ism, telefon))
    conn.commit()

    # Ma'lumotlarni olish
    cursor.execute("""
        SELECT v.sana, v.soat, s.ismi, m.nomi, m.manzili
        FROM vaqtlar v
        JOIN shifokorlar s ON v.shifokor_id = s.id
        JOIN muassasalar m ON s.muassasa_id = m.id
        WHERE v.id = ?
    """, (vaqt_id,))
    malumot = cursor.fetchone()

    bot.send_message(
        message.chat.id,
        f"✅ **Navbat muvaffaqiyatli olindi!**\n\n"
        f"🏥 **Muassasa:** {malumot[3]}\n"
        f"📍 **Manzil:** {malumot[4]}\n"
        f"👨‍⚕️ **Shifokor:** {malumot[2]}\n"
        f"📅 **Sana:** {malumot[0]}\n"
        f"⏰ **Vaqt:** {malumot[1]}\n\n"
        f"📋 '📋 Mening navbatlarim' bo'limida ko'rishingiz mumkin.",
        reply_markup=asosiy_menyu(),
        parse_mode='Markdown'
    )
# QIDIRISH
@bot.message_handler(func=lambda message: message.text == '🔍 Qidirish')
def qidirish_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👨‍⚕️ Shifokor", callback_data="q_search_doctor"),
        types.InlineKeyboardButton("🏥 Muassasa", callback_data="q_search_hospital"),
        types.InlineKeyboardButton("🔬 Mutaxassislik", callback_data="q_search_specialty"),
        types.InlineKeyboardButton("📍 Tuman", callback_data="q_search_district"),
        types.InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="orqaga_asosiy")
    )

    bot.send_message(
        message.chat.id,
        "🔍 **Qidirish turini tanlang:**",
        reply_markup=markup,
        parse_mode='Markdown'
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('q_search_'))
def qidirish_handler(call):
    q_turi = call.data.split('_')[2]

    if q_turi == "doctor":
        msg = bot.send_message(call.message.chat.id, "👨‍⚕️ **Shifokor ismini kiriting:**", parse_mode='Markdown')
        bot.register_next_step_handler(msg, qidirish_shifokor)
    elif q_turi == "hospital":
        msg = bot.send_message(call.message.chat.id, "🏥 **Muassasa nomini kiriting:**", parse_mode='Markdown')
        bot.register_next_step_handler(msg, qidirish_muassasa)
    elif q_turi == "specialty":
        msg = bot.send_message(call.message.chat.id, "🔬 **Mutaxassislikni kiriting:**", parse_mode='Markdown')
        bot.register_next_step_handler(msg, qidirish_mutaxassislik)
    elif q_turi == "district":
        cursor.execute("SELECT nomi FROM tumanlar ORDER BY nomi")
        tumanlar = cursor.fetchall()
        tuman_royxati = "\n".join([f"• {t[0]}" for t in tumanlar])
        msg = bot.send_message(
            call.message.chat.id,
            f"📍 **Tuman nomini kiriting:**\n\n{tuman_royxati}",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, qidirish_tuman)


def qidirish_shifokor(message):
    soz = message.text.lower()
    cursor.execute("""
        SELECT s.id, s.ismi, s.mutaxassisligi, m.nomi 
        FROM shifokorlar s
        JOIN muassasalar m ON s.muassasa_id = m.id
        WHERE LOWER(s.ismi) LIKE ? OR LOWER(s.mutaxassisligi) LIKE ?
        LIMIT 10
    """, (f'%{soz}%', f'%{soz}%'))

    natijalar = cursor.fetchall()

    if not natijalar:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_qidiruv"))
        bot.send_message(
            message.chat.id,
            f"❌ '{message.text}' bo'yicha hech narsa topilmadi.",
            reply_markup=markup
        )
        return

    markup = types.InlineKeyboardMarkup()
    for n in natijalar:
        markup.add(types.InlineKeyboardButton(
            f"👨‍⚕️ {n[1]} - {n[2]} ({n[3][:20]}...)",
            callback_data=f"shifokor_{n[0]}"
        ))
    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_qidiruv"))

    bot.send_message(
        message.chat.id,
        f"🔍 **{len(natijalar)} ta natija topildi:**",
        reply_markup=markup,
        parse_mode='Markdown'
    )


def qidirish_muassasa(message):
    soz = message.text.lower()
    cursor.execute("""
        SELECT id, nomi, turi, manzili 
        FROM muassasalar 
        WHERE LOWER(nomi) LIKE ? OR LOWER(turi) LIKE ?
        LIMIT 10
    """, (f'%{soz}%', f'%{soz}%'))

    natijalar = cursor.fetchall()

    if not natijalar:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_qidiruv"))
        bot.send_message(
            message.chat.id,
            f"❌ '{message.text}' bo'yicha hech narsa topilmadi.",
            reply_markup=markup
        )
        return

    markup = types.InlineKeyboardMarkup()
    for n in natijalar:
        markup.add(types.InlineKeyboardButton(
            f"🏥 {n[1]}",
            callback_data=f"muassasa_{n[0]}"
        ))
    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_qidiruv"))

    bot.send_message(
        message.chat.id,
        f"🔍 **{len(natijalar)} ta natija topildi:**",
        reply_markup=markup,
        parse_mode='Markdown'
    )


def qidirish_mutaxassislik(message):
    soz = message.text.lower()
    cursor.execute("""
        SELECT s.id, s.ismi, s.mutaxassisligi, m.nomi 
        FROM shifokorlar s
        JOIN muassasalar m ON s.muassasa_id = m.id
        WHERE LOWER(s.mutaxassisligi) LIKE ?
        LIMIT 10
    """, (f'%{soz}%',))

    natijalar = cursor.fetchall()

    if not natijalar:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_qidiruv"))
        bot.send_message(
            message.chat.id,
            f"❌ '{message.text}' bo'yicha hech narsa topilmadi.",
            reply_markup=markup
        )
        return

    markup = types.InlineKeyboardMarkup()
    for n in natijalar:
        markup.add(types.InlineKeyboardButton(
            f"👨‍⚕️ {n[1]} - {n[2]}",
            callback_data=f"shifokor_{n[0]}"
        ))
    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_qidiruv"))

    bot.send_message(
        message.chat.id,
        f"🔍 **{len(natijalar)} ta natija topildi:**",
        reply_markup=markup,
        parse_mode='Markdown'
    )


def qidirish_tuman(message):
    soz = message.text.lower()
    cursor.execute("SELECT id FROM tumanlar WHERE LOWER(nomi) LIKE ?", (f'%{soz}%',))
    tuman = cursor.fetchone()

    if not tuman:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_qidiruv"))
        bot.send_message(
            message.chat.id,
            f"❌ '{message.text}' tumani topilmadi.",
            reply_markup=markup
        )
        return

    tuman_id = tuman[0]
    cursor.execute("""
        SELECT id, nomi, turi FROM muassasalar 
        WHERE tuman_id = ? 
        LIMIT 10
    """, (tuman_id,))

    muassasalar = cursor.fetchall()

    if not muassasalar:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_qidiruv"))
        bot.send_message(
            message.chat.id,
            f"❌ Bu tumanda muassasa topilmadi.",
            reply_markup=markup
        )
        return

    markup = types.InlineKeyboardMarkup()
    for m in muassasalar:
        markup.add(types.InlineKeyboardButton(
            f"🏥 {m[1]}",
            callback_data=f"muassasa_{m[0]}"
        ))
    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_qidiruv"))

    bot.send_message(
        message.chat.id,
        f"📍 **{message.text.title()} tumanidagi muassasalar:**",
        reply_markup=markup,
        parse_mode='Markdown'
    )


# ALOQA
# ============================================
# ALOQA FUNKSIYASI (MUSTAQIL)
# ============================================
@bot.message_handler(func=lambda message: message.text == '📞 Aloqa')
def aloqa_handler(message):
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📞 Yordam", url="https://t.me/"),
            types.InlineKeyboardButton("🌐 Web", url="http://"),
            types.InlineKeyboardButton("📧 Email", callback_data="aloqa_email_callback"),
            types.InlineKeyboardButton("📱 Telegram", callback_data="aloqa_telegram_callback"),
            types.InlineKeyboardButton("🏠 Asosiy menyu", callback_data="asosiy_menyu_callback")
        )

        bot.send_message(
            message.chat.id,
            "📞 **ALOQA MA'LUMOTLARI**\n\n"
            "🏥 **Toshkent shahar tibbiyot boshqarmasi**\n"
            "📍 **Manzil:** Toshkent sh., Yunusobod tumani\n"
            "📞 **Ishonch telefoni:** +99871 200 00 00\n"
            "📧 **Email:** info@toshmed.uz\n"
            "⏰ **Ish vaqti:** Dushanba-Juma 09:00-18:00\n\n"
            "🚑 **Tez yordam:** 103\n"
            "🔥 **Favqulodda vaziyatlar:** 101\n\n"
            "💬 **Bot yordami:** @ToshMedBot_support",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Aloqa xatoligi: {e}")
        bot.send_message(message.chat.id, "Aloqa bo'limida xatolik yuz berdi.")


@bot.callback_query_handler(func=lambda call: call.data == 'aloqa_email_callback')
def aloqa_email_callback(call):
    bot.answer_callback_query(call.id, "Email: info@toshmed.uz", show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == 'aloqa_telegram_callback')
def aloqa_telegram_callback(call):
    bot.answer_callback_query(call.id, "Telegram: @ToshMedBot_support", show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == 'asosiy_menyu_callback')
def asosiy_menyu_callback(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(
        call.message.chat.id,
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=asosiy_menyu()
    )


# MENING NAVBATLARIM
@bot.message_handler(func=lambda message: message.text == '📋 Mening navbatlarim')
def mening_navbatlarim(message):
    user_id = message.from_user.id

    cursor.execute("""
        SELECT b.id, m.nomi, s.ismi, v.sana, v.soat
        FROM bronlar b
        JOIN vaqtlar v ON b.vaqt_id = v.id
        JOIN shifokorlar s ON v.shifokor_id = s.id
        JOIN muassasalar m ON s.muassasa_id = m.id
        WHERE b.user_id = ? AND v.sana >= date('now')
        ORDER BY v.sana, v.soat
    """, (user_id,))

    navbatlar = cursor.fetchall()

    if not navbatlar:
        bot.send_message(
            message.chat.id,
            "📭 **Sizda aktiv navbatlar yo'q.**\n\n🏥 Tuman tanlash orqali yangi navbat oling.",
            parse_mode='Markdown'
        )
        return

    for navbat in navbatlar:
        sana = datetime.strptime(navbat[3], '%Y-%m-%d').strftime('%d.%m.%Y')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "❌ Bekor qilish",
            callback_data=f"cancel_booking_{navbat[0]}"
        ))

        bot.send_message(
            message.chat.id,
            f"📋 **Navbat ma'lumotlari**\n\n"
            f"🏥 **Muassasa:** {navbat[1]}\n"
            f"👨‍⚕️ **Shifokor:** {navbat[2]}\n"
            f"📅 **Sana:** {sana}\n"
            f"⏰ **Vaqt:** {navbat[4]}\n\n"
            f"_Agar kela olmasangiz, bekor qiling_",
            reply_markup=markup,
            parse_mode='Markdown'
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith('cancel_booking_'))
def cancel_booking(call):
    bron_id = int(call.data.split('_')[2])

    cursor.execute("SELECT vaqt_id FROM bronlar WHERE id = ?", (bron_id,))
    vaqt_id = cursor.fetchone()

    if vaqt_id:
        cursor.execute("DELETE FROM bronlar WHERE id = ?", (bron_id,))
        cursor.execute("UPDATE vaqtlar SET bandmi = 0 WHERE id = ?", (vaqt_id[0],))
        conn.commit()

        bot.edit_message_text(
            "✅ **Navbat bekor qilindi!**",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(call.id, "Xatolik yuz berdi")


# ORQAGA QAYTISH (SHIFOKORLAR RO'YXATIGA)
@bot.callback_query_handler(func=lambda call: call.data == 'orqaga_shifokorlar')
def orqaga_shifokorlar(call):
    # Foydalanuvchi qaysi muassasadan kelganini aniqlash
    cursor.execute("""
        SELECT s.muassasa_id 
        FROM shifokorlar s 
        JOIN vaqtlar v ON s.id = v.shifokor_id 
        WHERE v.id = (
            SELECT vaqt_id FROM bronlar WHERE user_id = ? ORDER BY id DESC LIMIT 1
        )
    """, (call.from_user.id,))

    # Agar topilmasa, oddiygina tumanlar ro'yxatiga qaytish
    cursor.execute("SELECT id, nomi FROM tumanlar ORDER BY nomi")
    tumanlar = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=2)
    for tuman in tumanlar:
        markup.add(types.InlineKeyboardButton(
            tuman[1],
            callback_data=f"tuman_{tuman[0]}"
        ))

    bot.edit_message_text(
        "🏙️ **Tumanni tanlang:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# TUMANLARGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data == 'orqaga_tumanlar')
def orqaga_tumanlar(call):
    cursor.execute("SELECT id, nomi FROM tumanlar ORDER BY nomi")
    tumanlar = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=2)
    for tuman in tumanlar:
        markup.add(types.InlineKeyboardButton(
            tuman[1],
            callback_data=f"tuman_{tuman[0]}"
        ))

    bot.edit_message_text(
        "🏙️ **Tumanni tanlang:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# MUASSASA TURIGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data.startswith('orqaga_tur_'))
def orqaga_tur(call):
    tuman_id = int(call.data.split('_')[2])

    cursor.execute("""
        SELECT turi, COUNT(*) FROM muassasalar 
        WHERE tuman_id = ? GROUP BY turi
    """, (tuman_id,))
    tur_sonlari = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=2)
    tur_kodlari = {
        'shifoxona': '🏨 Shifoxonalar',
        'poliklinika': '🏥 Poliklinikalar',
        'stomatologiya': '🦷 Stomatologiyalar',
        'dispanser': '🏥 Dispanserlar'
    }

    for tur, son in tur_sonlari:
        if tur in tur_kodlari:
            markup.add(types.InlineKeyboardButton(
                f"{tur_kodlari[tur]} ({son} ta)",
                callback_data=f"tur_{tuman_id}_{tur}"
            ))

    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_tumanlar"))

    bot.edit_message_text(
        "🏥 **Muassasa turini tanlang:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# MUASSASALAR RO'YXATIGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data.startswith('orqaga_muassasalar_'))
def orqaga_muassasalar(call):
    parts = call.data.split('_')
    tuman_id = int(parts[2])
    tur = parts[3]

    cursor.execute("""
        SELECT id, nomi, manzili FROM muassasalar 
        WHERE tuman_id = ? AND turi = ?
        ORDER BY nomi
    """, (tuman_id, tur))
    muassasalar = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=1)
    for muassasa in muassasalar:
        nom_qisqa = muassasa[1][:35] + "..." if len(muassasa[1]) > 35 else muassasa[1]
        markup.add(types.InlineKeyboardButton(
            nom_qisqa,
            callback_data=f"muassasa_{muassasa[0]}"
        ))

    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data=f"orqaga_tur_{tuman_id}"))

    tur_nomi = {
        'shifoxona': '🏨 Shifoxonalar',
        'poliklinika': '🏥 Poliklinikalar',
        'stomatologiya': '🦷 Stomatologiyalar',
        'dispanser': '🏥 Dispanserlar'
    }.get(tur, tur)

    bot.edit_message_text(
        f"{tur_nomi} ro'yxati:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# SHIFOKORLAR RO'YXATIGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data.startswith('orqaga_shifokorlar_'))
def orqaga_shifokorlar(call):
    muassasa_id = int(call.data.split('_')[2])

    cursor.execute("SELECT nomi, manzili FROM muassasalar WHERE id = ?", (muassasa_id,))
    muassasa = cursor.fetchone()

    cursor.execute("""
        SELECT id, ismi, mutaxassisligi, malakasi 
        FROM shifokorlar 
        WHERE muassasa_id = ?
    """, (muassasa_id,))
    shifokorlar = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=1)
    for shifokor in shifokorlar:
        markup.add(types.InlineKeyboardButton(
            f"👨‍⚕️ {shifokor[1]} - {shifokor[2]}",
            callback_data=f"shifokor_{shifokor[0]}"
        ))

    # Tumanga qaytish uchun
    cursor.execute("SELECT tuman_id FROM muassasalar WHERE id = ?", (muassasa_id,))
    tuman_id = cursor.fetchone()[0]

    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_qidiruv"))

    bot.edit_message_text(
        f"🏥 **{muassasa[0]}**\n📍 {muassasa[1]}\n\n"
        f"👨‍⚕️ **Shifokorlar:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# ASOSIY MENYUGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data == 'orqaga_asosiy')
def orqaga_asosiy(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(
        call.message.chat.id,
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=asosiy_menyu()
    )


# NAVBATLARDAN QAYTISH
@bot.callback_query_handler(func=lambda call: call.data == 'orqaga_navbatlar')
def orqaga_navbatlar(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    mening_navbatlarim(call.message)


# QIDIRUVDAN QAYTISH
@bot.callback_query_handler(func=lambda call: call.data == 'orqaga_qidiruv')
def orqaga_qidiruv(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👨‍⚕️ Shifokor", callback_data="q_search_doctor"),
        types.InlineKeyboardButton("🏥 Muassasa", callback_data="q_search_hospital"),
        types.InlineKeyboardButton("🔬 Mutaxassislik", callback_data="q_search_specialty"),
        types.InlineKeyboardButton("📍 Tuman", callback_data="q_search_district"),
        types.InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="orqaga_asosiy")
    )

    bot.edit_message_text(
        "🔍 **Qidirish turini tanlang:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )



# MUASSASA TURIGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data.startswith('orqaga_tur_'))
def orqaga_tur(call):
    tuman_id = int(call.data.split('_')[2])

    cursor.execute("""
        SELECT turi, COUNT(*) FROM muassasalar 
        WHERE tuman_id = ? GROUP BY turi
    """, (tuman_id,))
    tur_sonlari = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=2)
    tur_kodlari = {
        'shifoxona': '🏨 Shifoxonalar',
        'poliklinika': '🏥 Poliklinikalar',
        'stomatologiya': '🦷 Stomatologiyalar',
        'dispanser': '🏥 Dispanserlar'
    }

    for tur, son in tur_sonlari:
        if tur in tur_kodlari:
            markup.add(types.InlineKeyboardButton(
                f"{tur_kodlari[tur]} ({son} ta)",
                callback_data=f"tur_{tuman_id}_{tur}"
            ))

    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_tumanlar"))

    bot.edit_message_text(
        "🏥 **Muassasa turini tanlang:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# MUASSASALAR RO'YXATIGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data.startswith('orqaga_muassasalar_'))
def orqaga_muassasalar(call):
    parts = call.data.split('_')
    tuman_id = int(parts[2])
    tur = parts[3]

    cursor.execute("""
        SELECT id, nomi, manzili FROM muassasalar 
        WHERE tuman_id = ? AND turi = ?
        ORDER BY nomi
    """, (tuman_id, tur))
    muassasalar = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=1)
    for muassasa in muassasalar:
        nom_qisqa = muassasa[1][:35] + "..." if len(muassasa[1]) > 35 else muassasa[1]
        markup.add(types.InlineKeyboardButton(
            nom_qisqa,
            callback_data=f"muassasa_{muassasa[0]}"
        ))

    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data=f"orqaga_tur_{tuman_id}"))

    tur_nomi = {
        'shifoxona': '🏨 Shifoxonalar',
        'poliklinika': '🏥 Poliklinikalar',
        'stomatologiya': '🦷 Stomatologiyalar',
        'dispanser': '🏥 Dispanserlar'
    }.get(tur, tur)

    bot.edit_message_text(
        f"{tur_nomi} ro'yxati:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# SHIFOKORLAR RO'YXATIGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data.startswith('orqaga_shifokorlar_'))
def orqaga_shifokorlar_(call):
    muassasa_id = int(call.data.split('_')[2])

    cursor.execute("SELECT nomi, manzili FROM muassasalar WHERE id = ?", (muassasa_id,))
    muassasa = cursor.fetchone()

    cursor.execute("""
        SELECT id, ismi, mutaxassisligi, malakasi 
        FROM shifokorlar 
        WHERE muassasa_id = ?
    """, (muassasa_id,))
    shifokorlar = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=1)
    for shifokor in shifokorlar:
        markup.add(types.InlineKeyboardButton(
            f"👨‍⚕️ {shifokor[1]} - {shifokor[2]}",
            callback_data=f"shifokor_{shifokor[0]}"
        ))

    # Muassasaning tumani va turini olish
    cursor.execute("SELECT tuman_id, turi FROM muassasalar WHERE id = ?", (muassasa_id,))
    tuman_tur = cursor.fetchone()
    tuman_id = tuman_tur[0]
    tur = tuman_tur[1]

    markup.add(types.InlineKeyboardButton(
        "⬅️ Muassasalar ro'yxati",
        callback_data=f"orqaga_muassasalar_{tuman_id}_{tur}"
    ))

    bot.edit_message_text(
        f"🏥 **{muassasa[0]}**\n📍 {muassasa[1]}\n\n"
        f"👨‍⚕️ **Shifokorlar:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# ASOSIY MENYUGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data == 'orqaga_asosiy')
def orqaga_asosiy(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(
        call.message.chat.id,
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=asosiy_menyu()
    )


# NAVBATLARDAN QAYTISH
@bot.callback_query_handler(func=lambda call: call.data == 'orqaga_navbatlar')
def orqaga_navbatlar(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    mening_navbatlarim(call.message)


# QIDIRUVDAN QAYTISH
@bot.callback_query_handler(func=lambda call: call.data == 'orqaga_qidiruv')
def orqaga_qidiruv(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👨‍⚕️ Shifokor", callback_data="q_search_doctor"),
        types.InlineKeyboardButton("🏥 Muassasa", callback_data="q_search_hospital"),
        types.InlineKeyboardButton("🔬 Mutaxassislik", callback_data="q_search_specialty"),
        types.InlineKeyboardButton("📍 Tuman", callback_data="q_search_district"),
        types.InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="orqaga_asosiy")
    )

    bot.edit_message_text(
        "🔍 **Qidirish turini tanlang:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# MUASSASA TURIGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data.startswith('orqaga_tur_'))
def orqaga_tur(call):
    tuman_id = int(call.data.split('_')[2])

    cursor.execute("""
        SELECT turi, COUNT(*) FROM muassasalar 
        WHERE tuman_id = ? GROUP BY turi
    """, (tuman_id,))
    tur_sonlari = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=2)
    tur_kodlari = {
        'shifoxona': '🏨 Shifoxonalar',
        'poliklinika': '🏥 Poliklinikalar',
        'stomatologiya': '🦷 Stomatologiyalar',
        'dispanser': '🏥 Dispanserlar'
    }

    for tur, son in tur_sonlari:
        if tur in tur_kodlari:
            markup.add(types.InlineKeyboardButton(
                f"{tur_kodlari[tur]} ({son} ta)",
                callback_data=f"tur_{tuman_id}_{tur}"
            ))

    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="orqaga_tumanlar"))

    bot.edit_message_text(
        "🏥 **Muassasa turini tanlang:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# MUASSASALAR RO'YXATIGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data.startswith('orqaga_muassasalar_'))
def orqaga_muassasalar(call):
    parts = call.data.split('_')
    tuman_id = int(parts[2])
    tur = parts[3]

    cursor.execute("""
        SELECT id, nomi, manzili FROM muassasalar 
        WHERE tuman_id = ? AND turi = ?
        ORDER BY nomi
    """, (tuman_id, tur))
    muassasalar = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=1)
    for muassasa in muassasalar:
        nom_qisqa = muassasa[1][:35] + "..." if len(muassasa[1]) > 35 else muassasa[1]
        markup.add(types.InlineKeyboardButton(
            nom_qisqa,
            callback_data=f"muassasa_{muassasa[0]}"
        ))

    markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data=f"orqaga_tur_{tuman_id}"))

    tur_nomi = {
        'shifoxona': '🏨 Shifoxonalar',
        'poliklinika': '🏥 Poliklinikalar',
        'stomatologiya': '🦷 Stomatologiyalar',
        'dispanser': '🏥 Dispanserlar'
    }.get(tur, tur)

    bot.edit_message_text(
        f"{tur_nomi} ro'yxati:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# SHIFOKORLAR RO'YXATIGA QAYTISH
@bot.callback_query_handler(func=lambda call: call.data.startswith('orqaga_shifokorlar_'))
def orqaga_shifokorlar(call):
    muassasa_id = int(call.data.split('_')[2])

    cursor.execute("SELECT nomi, manzili FROM muassasalar WHERE id = ?", (muassasa_id,))
    muassasa = cursor.fetchone()

    cursor.execute("""
        SELECT id, ismi, mutaxassisligi, malakasi 
        FROM shifokorlar 
        WHERE muassasa_id = ?
        ORDER BY ismi
    """, (muassasa_id,))
    shifokorlar = cursor.fetchall()

    if not shifokorlar:
        bot.answer_callback_query(call.id, "Bu muassasada shifokorlar yo'q")
        # Tumanga qaytish
        cursor.execute("SELECT tuman_id FROM muassasalar WHERE id = ?", (muassasa_id,))
        tuman_id = cursor.fetchone()[0]

        cursor.execute("SELECT id, nomi FROM tumanlar ORDER BY nomi")
        tumanlar = cursor.fetchall()

        markup = types.InlineKeyboardMarkup(row_width=2)
        for tuman in tumanlar:
            markup.add(types.InlineKeyboardButton(
                tuman[1],
                callback_data=f"tuman_{tuman[0]}"
            ))

        bot.edit_message_text(
            "🏙️ **Tumanni tanlang:**",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for shifokor in shifokorlar:
        markup.add(types.InlineKeyboardButton(
            f"👨‍⚕️ {shifokor[1]} - {shifokor[2]}",
            callback_data=f"shifokor_{shifokor[0]}"
        ))

    # Tumanga qaytish uchun
    cursor.execute("SELECT tuman_id, turi FROM muassasalar WHERE id = ?", (muassasa_id,))
    tuman_tur = cursor.fetchone()
    tuman_id = tuman_tur[0]
    tur = tuman_tur[1]

    markup.add(types.InlineKeyboardButton(
        "⬅️ Muassasalar ro'yxati",
        callback_data=f"orqaga_muassasalar_{tuman_id}_{tur}"
    ))

    bot.edit_message_text(
        f"🏥 **{muassasa[0]}**\n📍 {muassasa[1]}\n\n"
        f"👨‍⚕️ **Shifokorlar ({len(shifokorlar)} nafar):**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# QIDIRUVDAN QAYTISH
@bot.callback_query_handler(func=lambda call: call.data == 'orqaga_qidiruv')
def orqaga_qidiruv(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👨‍⚕️ Shifokor", callback_data="q_search_doctor"),
        types.InlineKeyboardButton("🏥 Muassasa", callback_data="q_search_hospital"),
        types.InlineKeyboardButton("🔬 Mutaxassislik", callback_data="q_search_specialty"),
        types.InlineKeyboardButton("📍 Tuman", callback_data="q_search_district"),
        types.InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="orqaga_asosiy")
    )

    bot.edit_message_text(
        "🔍 **Qidirish turini tanlang:**",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# VAQTNI BEKOR QILISH (SHIFOKOR SAHIFASIGA QAYTISH)
@bot.callback_query_handler(func=lambda call: call.data.startswith('bekor_vaqt_'))
def bekor_vaqt(call):
    parts = call.data.split('_')
    vaqt_id = int(parts[2])
    shifokor_id = int(parts[3])

    # Vaqtni bo'shatish (agar band qilingan bo'lsa)
    cursor.execute("UPDATE vaqtlar SET bandmi = 0 WHERE id = ?", (vaqt_id,))
    conn.commit()

    # Shifokor ma'lumotlarini olish
    cursor.execute("""
        SELECT s.ismi, s.mutaxassisligi, s.malakasi, s.qoshimcha,
               m.nomi, m.manzili, m.tel, m.id
        FROM shifokorlar s
        JOIN muassasalar m ON s.muassasa_id = m.id
        WHERE s.id = ?
    """, (shifokor_id,))
    shifokor = cursor.fetchone()

    # Bo'sh vaqtlarni olish
    cursor.execute("""
        SELECT id, sana, soat FROM vaqtlar 
        WHERE shifokor_id = ? AND bandmi = 0 
        ORDER BY sana, soat
        LIMIT 8
    """, (shifokor_id,))
    vaqtlar = cursor.fetchall()

    # Tugmalar yaratish
    markup = types.InlineKeyboardMarkup(row_width=2)

    if vaqtlar:
        for vaqt in vaqtlar:
            sana_qism = vaqt[1][8:10] + '.' + vaqt[1][5:7]
            markup.add(types.InlineKeyboardButton(
                f"📅 {sana_qism} ⏰ {vaqt[2]}",
                callback_data=f"vaqt_{vaqt[0]}"
            ))
    else:
        markup.add(types.InlineKeyboardButton(
            "❌ Bo'sh vaqtlar yo'q",
            callback_data="none"
        ))

    # Orqaga tugmasi (shifokorlar ro'yxatiga)
    markup.add(types.InlineKeyboardButton(
        "⬅️ Orqaga",
        callback_data=f"orqaga_shifokorlar_{shifokor[7]}"
    ))

    # Xabar matni
    text = f"👨‍⚕️ **{shifokor[0]}**\n"
    text += f"🏥 **Mutaxassislik:** {shifokor[1]}\n"
    text += f"⭐ **Malaka:** {shifokor[2]}\n"
    if shifokor[3]:
        text += f"ℹ️ **Qo'shimcha:** {shifokor[3]}\n"
    text += f"\n🏥 **Muassasa:** {shifokor[4]}\n"
    text += f"📍 **Manzil:** {shifokor[5]}\n"
    if shifokor[6]:
        text += f"📞 **Tel:** {shifokor[6]}\n"
    text += f"\n⏰ **Bo'sh vaqtlar:**"

    # Xabarni yangilash
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# TUMANLARGA QAYTISH (funksiya allaqachon 3-qismda bor, lekin qayta yozilmasligi uchun)
# Bu funksiya 3-qismda mavjud, shuning uchun bu yerda qayta yozilmadi
# BOT HAQIDA
@bot.message_handler(func=lambda message: message.text == 'ℹ️ Bot haqida')
def bot_haqida(message):
    bot.send_message(
        message.chat.id,
        "🤖 **Toshkent Tibbiyot Boti v1.0**\n\n"
        "📊 **Ma'lumotlar:**\n"
        "• 12 ta tuman\n"
        "• 30+ klinika va shifoxona\n"
        "• 60+ malakali shifokor\n"
        "• 3 kunlik bo'sh vaqtlar\n\n"
        "✅ **Funksiyalar:**\n"
        "• Tumanlar bo'yicha qidirish\n"
        "• Shifoxona, poliklinika, stomatologiya\n"
        "• Shifokorlar ro'yxati\n"
        "• Onlayn navbat olish\n"
        "• Navbatni bekor qilish\n"
        "• Shifokor va muassasa qidirish\n\n"
        "📅 **Oxirgi yangilanish:** Mart 2026\n"
        "👨‍💻 **Dasturchi:** @b_2406",
        parse_mode='Markdown'
    )


# Botni ishga tushirish
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 TOSHKENT TIBBIYOT BOTI")
    print("=" * 50)
    print("✅ Bot ishga tushmoqda...")
    print("=" * 50)

    # Botni alohida threadda ishga tushirish
    def run_bot():
        bot.infinity_polling()

    threading.Thread(target=run_bot, daemon=True).start()

    # Flask serverni ishga tushirish
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)