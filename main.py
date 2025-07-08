import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = '8017774805:AAGbL_svd8A7EqPDeWF_aQhZSlDZ0vYu1dw'
bot = telebot.TeleBot(TOKEN)


def send_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📢 Elon berish", callback_data='menu_elon'),
        InlineKeyboardButton("🏠 Uy-joy izlash", callback_data='menu_uy'),
        InlineKeyboardButton("👫 Do‘stlarni taklif qilish", callback_data='menu_dost'),
        InlineKeyboardButton("📞 Reklama uchun admin", url='https://t.me/Abu200115'),
        InlineKeyboardButton("🎥 Video qo‘llanma", url='https://t.me/Yakhyojonov/614')
    )
    bot.send_message(
        chat_id,
        "🤖 Hush kelibsiz! Bo‘limni tanlang:",
        reply_markup=markup
    )

import json
import os

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""

    # Fayl mavjud emas bo‘lsa, bosh dict ochamiz
    if not os.path.exists('users.json'):
        users = {}
    else:
        with open('users.json', 'r', encoding='utf-8') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}

    # Agar user yo‘q bo‘lsa, qo‘shamiz
    if user_id not in users:
        users[user_id] = {
            'id': user_id,
            'name': first_name,
            'last': last_name,
            'num': None
        }

        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

    # Keyin menyuni yuboramiz
    send_main_menu(message.chat.id)


















ADMIN_IDS = [7899619708]
OWNER_IDS = [7577190183]  # bir nechta owner ID








broadcast_state = {}

@bot.message_handler(commands=['ad'])
def handle_ad_command(message):
    if message.from_user.id not in OWNER_IDS and message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ Sizda huquq yo‘q.")
        return

    broadcast_state[message.from_user.id] = True
    bot.reply_to(message, "📢 Reklama yuboring (media, text, sticker, nima bo‘lsa ham).")

@bot.message_handler(func=lambda m: broadcast_state.get(m.from_user.id))
def handle_ad_content(message):
    # Endi reklama xabari keldi
    broadcast_state.pop(message.from_user.id, None)  # holatni o‘chir

    try:
        # User va guruh IDs ro‘yxatini o‘qiymiz
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        with open('groups.json', 'r', encoding='utf-8') as f:
            groups = json.load(f)
    except Exception as e:
        bot.reply_to(message, f"❗ Faylni o‘qishda xatolik: {e}")
        return

    all_ids = users + groups  # foydalanuvchi va guruhlarni birlashtiramiz

    success, failed = 0, 0

    for chat_id in all_ids:
        try:
            bot.forward_message(chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
            success += 1
        except Exception as e:
            failed += 1

    bot.reply_to(message, f"✅ Reklama yuborildi!\n\n✅ Yuborildi: {success}\n❌ Yuborilmadi: {failed}")

































@bot.message_handler(commands=['add_chat'])
def handle_add_chat(message):
    if message.from_user.id not in OWNER_IDS:
        bot.reply_to(message, "⛔ Sizda huquq yo‘q.")
        return

    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except:
        bot.reply_to(message, "❗ Viloyatlar faylini o‘qishda xatolik.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    for v in viloyatlar:
        markup.add(InlineKeyboardButton(v, callback_data=f'add_vil_{v}'))
    bot.send_message(message.chat.id, "Viloyatni tanlang:", reply_markup=markup)




@bot.callback_query_handler(func=lambda call: call.data.startswith('add_vil_'))
def handle_add_viloyat(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)  # eski xabarni o‘chir

    viloyat = call.data[8:]  # 'add_vil_' dan keyingi qism

    try:
        with open('hududlar.json', 'r', encoding='utf-8') as f:
            hududlar_data = json.load(f)
    except:
        bot.send_message(call.message.chat.id, "❗ Hududlar faylini o‘qishda xatolik.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    hududlar = hududlar_data.get(viloyat, [])

    for h in hududlar:
        name = h['name']
        markup.add(InlineKeyboardButton(name, callback_data=f'add_hud_{viloyat}_{name}'))

    # Yangi hudud qo‘shish
    markup.add(InlineKeyboardButton("➕ Yangi hudud qo‘shish", callback_data=f'add_newhud_{viloyat}'))
    bot.send_message(call.message.chat.id, f"📍 {viloyat} hududlarini tanlang yoki yangi qo‘shing:", reply_markup=markup)



user_states = {}

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_hud_'))
def handle_add_hud(call):
    bot.answer_callback_query(call.id)
    parts = call.data.split('_', 3)
    viloyat = parts[2]
    hudud = parts[3]
    user_id = call.from_user.id

    user_states[user_id] = {'action': 'edit_chat_id', 'viloyat': viloyat, 'hudud': hudud}
    bot.send_message(call.message.chat.id, f"✏️ Yangi chat_id kiriting (masalan, -100...):")

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_newhud_'))
def handle_add_new_hud(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)  # eski xabarni o‘chir

    viloyat = call.data[11:]  # 'add_newhud_' dan keyin
    user_id = call.from_user.id

    user_states[user_id] = {'action': 'add_new_hud', 'viloyat': viloyat}
    bot.send_message(call.message.chat.id, "✏️ Yangi hudud nomini kiriting:")



@bot.message_handler(func=lambda message: message.from_user.id in user_states)
def process_user_input(message):
    state = user_states.get(message.from_user.id)
    if not state:
        return

    user_id = message.from_user.id

    if state['action'] == 'add_new_hud':
        # Hudud nomini oldik, endi chat_id so‘raymiz
        state['hudud'] = message.text
        state['action'] = 'add_new_chat_id'
        bot.send_message(message.chat.id, "✅ Endi chat_id ni kiriting (masalan, -100...)")

    elif state['action'] in ['add_new_chat_id', 'edit_chat_id']:
        chat_id = message.text.strip()
        if not chat_id.startswith("-100"):
            bot.send_message(message.chat.id, "❗ Chat ID -100 bilan boshlanishi kerak. Qayta kiriting:")
            return

        state['chat_id'] = chat_id
        # Endi link so‘raymiz
        state['action'] = 'add_new_link' if state['action'] == 'add_new_chat_id' else 'edit_link'
        bot.send_message(message.chat.id, "🔗 Endi link ni kiriting (masalan, https://t.me/....):")

    elif state['action'] in ['add_new_link', 'edit_link']:
        link = message.text.strip()

        if not link.startswith("https://t.me/"):
            bot.send_message(message.chat.id, "❗ Link https://t.me/ bilan boshlanishi kerak. Qayta kiriting:")
            return

        viloyat = state['viloyat']
        hudud = state['hudud']
        chat_id = state['chat_id']

        try:
            with open('hududlar.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {}

        if viloyat not in data:
            data[viloyat] = []

        if state['action'] == 'add_new_link':
            # Yangi hudud qo‘shamiz
            data[viloyat].append({"name": hudud, "chat_id": chat_id, "link": link})
            bot.send_message(message.chat.id, f"✅ Yangi hudud qo‘shildi: {hudud}")
        else:
            # Mavjud hudud chat_id va link ni yangilaymiz
            for h in data[viloyat]:
                if h['name'] == hudud:
                    h['chat_id'] = chat_id
                    h['link'] = link
                    break
            bot.send_message(message.chat.id, f"✅ Chat ID va link yangilandi: {hudud}")

        with open('hududlar.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        user_states.pop(user_id, None)











OWNER_IDS = [7577190183, 123456789, 987654321]  # bir nechta owner ID

@bot.message_handler(commands=['remove_chat'])
def handle_remove_chat(message):
    if message.from_user.id not in OWNER_IDS:
        bot.reply_to(message, "⛔ Sizda huquq yo‘q.")
        return

    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except:
        bot.reply_to(message, "❗ Viloyatlar faylini o‘qishda xatolik.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    for v in viloyatlar:
        markup.add(InlineKeyboardButton(v, callback_data=f'remove_vil_{v}'))

    bot.send_message(message.chat.id, "🗑 O‘chirish uchun viloyatni tanlang:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('remove_vil_'))
def handle_remove_viloyat(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)  # eski xabarni o‘chir

    viloyat = call.data[11:]  # 'remove_vil_' dan keyin

    try:
        with open('hududlar.json', 'r', encoding='utf-8') as f:
            hududlar_data = json.load(f)
    except:
        bot.send_message(call.message.chat.id, "❗ Hududlar faylini o‘qishda xatolik.")
        return

    hududlar = hududlar_data.get(viloyat, [])
    if not hududlar:
        bot.send_message(call.message.chat.id, "❗ Bu viloyatda hududlar topilmadi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    for h in hududlar:
        name = h['name']
        markup.add(InlineKeyboardButton(f"🗑 {name}", callback_data=f'remove_hud_{viloyat}_{name}'))

    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='remove_chat'))
    bot.send_message(call.message.chat.id, f"🗑 {viloyat} hududidan qaysini o‘chiramiz?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('remove_hud_'))
def handle_remove_hudud(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)  # eski xabarni o‘chir

    parts = call.data.split('_', 3)
    viloyat = parts[2]
    hudud = parts[3]

    try:
        with open('hududlar.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        bot.send_message(call.message.chat.id, "❗ Faylni o‘qishda xatolik.")
        return

    hududlar = data.get(viloyat, [])
    new_hududlar = [h for h in hududlar if h['name'] != hudud]

    if len(new_hududlar) == len(hududlar):
        bot.send_message(call.message.chat.id, "❗ Hudud topilmadi.")
        return

    data[viloyat] = new_hududlar

    try:
        with open('hududlar.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        bot.send_message(call.message.chat.id, f"✅ Hudud o‘chirildi: {hudud}")
    except:
        bot.send_message(call.message.chat.id, "❗ Saqlashda xatolik yuz berdi.")



@bot.message_handler(commands=['download'])
def handle_download(message):
    if message.from_user.id not in OWNER_IDS:
        bot.reply_to(message, "⛔ Sizda huquq yo‘q.")
        return

    folder = '.'  # joriy papka (botning papkasi)
    json_files = [f for f in os.listdir(folder) if f.endswith('.json')]

    if not json_files:
        bot.reply_to(message, "❗ Hech qanday JSON fayl topilmadi.")
        return

    for file_name in json_files:
        try:
            with open(file_name, 'rb') as f:
                bot.send_document(message.chat.id, f)
        except Exception as e:
            bot.reply_to(message, f"❗ Xatolik: {file_name} - {e}")

    bot.reply_to(message, "✅ Barcha JSON fayllar yuborildi!")







@bot.callback_query_handler(func=lambda call: call.data == 'menu_uy')
def handle_menu_uy(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    markup = InlineKeyboardMarkup(row_width=2)

    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            data = json.load(f)   # data endi list bo‘ladi
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    buttons = []
    for viloyat in data:
        buttons.append(InlineKeyboardButton(viloyat, callback_data=f'vil1_{viloyat}'))

    # endi har 2 tasini bir qatorda qo‘yamiz
    for i in range(0, len(buttons), 2):
        if i+1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])

    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_main'))

    bot.send_message(call.message.chat.id, "Viloyatni tanlang:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('vil1_'))
def handle_viloyat1(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    viloyat_nomi = call.data[5:]  # "vil1_" dan keyingi qism

    try:
        with open('hududlar.json', 'r', encoding='utf-8') as f:
            hududlar_data = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❗ Hududlar faylini o‘qishda xatolik yuz berdi: {e}")
        return

    hududlar = hududlar_data.get(viloyat_nomi)
    if not hududlar:
        bot.send_message(call.message.chat.id, "❗ Bu viloyat uchun hududlar topilmadi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    for h in hududlar:
        name = h['name']
        link = h.get('link')
        if link:
            markup.add(InlineKeyboardButton(name, url=link))

    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='menu_uy'))

    bot.send_message(
        call.message.chat.id,
        f"📍 {viloyat_nomi} viloyati hududlarini tanlang:",
        reply_markup=markup
    )



# Elon berish tugmasi bosilganda
@bot.callback_query_handler(func=lambda call: call.data == 'menu_elon')
def handle_elon(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🏠 Uy-joy ijaraga berish", callback_data='elon_ijaraga'),
        InlineKeyboardButton("🏠 Uy-joy sotish", callback_data='elon_sotish'),
        InlineKeyboardButton("🌿 Bo'sh yer sotish", callback_data='elon_yer'),
        InlineKeyboardButton("🏪 Do'konni sotish", callback_data='elon_dokon_sot'),
        InlineKeyboardButton("🏪 Do'konni ijaraga berish", callback_data='elon_dokon_ijara'),
        InlineKeyboardButton("🏢 Noturar bino sotish", callback_data='elon_noto_sot'),
        InlineKeyboardButton("🏢 Noturar bino ijaraga berish", callback_data='elon_noto_olish'),
        InlineKeyboardButton("🔙 Orqaga", callback_data='back_main')
    )
    bot.send_message(
        call.message.chat.id,
        "📢 Elon berish uchun kategoriya tanlang:",
        reply_markup=markup
    )

# Orqaga tugmasi bosilganda
@bot.callback_query_handler(func=lambda call: call.data == 'back_main')
def handle_back(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    send_main_menu(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == 'menu_uy')
def handle_uy(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "🏠 Siz uy-joy izlash bo‘limini tanladingiz.")

@bot.callback_query_handler(func=lambda call: call.data == 'menu_dost')
def handle_dost(call):
    bot.answer_callback_query(call.id)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="📲 Do‘stga ulashish",
            switch_inline_query="Salom! Mana zo‘r bot, kirib ko‘r 👉 https://t.me/YOUR_BOT_USERNAME"
        )
    )

    bot.send_message(
        call.message.chat.id,
        "Do‘stlaringizga botni ulashing:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'menu_video')
def handle_video(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "🎥 Siz video qo‘llanma bo‘limini tanladingiz.")








import json

@bot.callback_query_handler(func=lambda call: call.data == 'elon_ijaraga')
def handle_ijaraga(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Viloyatlar ro‘yxatini fayldan o‘qish
    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(v, callback_data=f"vil_{v}") for v in viloyatlar]
    markup.add(*buttons)

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Ijara sotib olsih uchun viloyatni tanlang:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'back_elon')
def handle_back_elon(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    # Orqaga – elon menyusiga qaytaradi
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🏠 Uy-joy ijaraga", callback_data='elon_ijaraga'),
        InlineKeyboardButton("🏠 Uy-joy sotish", callback_data='elon_sotish'),
        InlineKeyboardButton("🌿 Bo'sh yer sotish", callback_data='elon_yer'),
        InlineKeyboardButton("🏪 Do'konni sotish", callback_data='elon_dokon_sot'),
        InlineKeyboardButton("🏪 Do'konni ijaraga berish", callback_data='elon_dokon_ijara'),
        InlineKeyboardButton("🏢 Noturar bino sotish", callback_data='elon_noto_sot'),
        InlineKeyboardButton("🏢 Noturar bino ijaraga berish", callback_data='elon_noto_olish'),
        InlineKeyboardButton("🔙 Orqaga", callback_data='back_main')
    )
    bot.send_message(
        call.message.chat.id,
        "📢 Elon berish uchun kategoriya tanlang:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('vil_'))
def handle_viloyat(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    viloyat_nomi = call.data[4:]  # "vil_" dan keyingi qism

    try:
        with open('hududlar.json', 'r', encoding='utf-8') as f:
            hududlar_data = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Hududlar faylini o‘qishda xatolik yuz berdi.")
        return

    hududlar = hududlar_data.get(viloyat_nomi)
    if not hududlar:
        bot.send_message(call.message.chat.id, "❗ Bu viloyat uchun hududlar topilmadi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    for h in hududlar:
        name = h['name']
        # callback_data orqali hudud nomini yuboramiz
        markup.add(InlineKeyboardButton(name, callback_data='hud_' + name))

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_viloyatlar'))

    bot.send_message(
        call.message.chat.id,
        f"{viloyat_nomi} viloyati hududlarini tanlang:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'back_viloyatlar')
def handle_back_viloyatlar(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Viloyatlar.json dan o‘qib, bosh menyuni ko‘rsatamiz
    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(v, callback_data=f"vil_{v}") for v in viloyatlar]
    markup.add(*buttons)
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Viloyatni tanlang:",
        reply_markup=markup
    )

import os
import shutil
from telebot import types

user_states = {}   # user_id: {'chat_id': int, 'caption': str, 'expected_photos': int, 'received_photos': int, 'photos': []}

@bot.callback_query_handler(func=lambda call: call.data.startswith('hud_'))
def handle_hudud(call):
    hudud_nomi = call.data[4:]
    with open('hududlar.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    chat_id = next((h['chat_id'] for vil in data.values() for h in vil if h['name'] == hudud_nomi), None)

    if not chat_id:
        bot.send_message(call.message.chat.id, "❗ Hudud topilmadi.")
        return

    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    except Exception:
        pass

    user_states[call.from_user.id] = {'chat_id': chat_id}
    bot.send_message(
        call.message.chat.id,
        """📝 E'lon mazmunini yozing.

Shu namuna asosida e’loningizni yozing!

🏠 KVARTIRA IJARAGA BERILADI

📍 Shahar, Tuman 5-kvartal
💰 Narxi: 300$–400$
🛏 Xonalar: 2 xonali
♨️ Kommunal: gaz, suv, svet bor
🪚 Holati: yevro remont yoki o‘rtacha
🛋 Jihoz: jihozli yoki jihozsiz
🕒 Muddat: qisqa yoki uzoq muddatga
👥 Kimga: Shariy nikohga / oilaga / studentlarga

🔴 Eslatma
Rasm tashlash jarayonida alohida-alohida rasm kiriting, 8ta rasmgacha mumkin."""
    )
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, receive_caption)

def receive_caption(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if not state:
        bot.send_message(message.chat.id, "❗ Avval hududni tanlang.")
        return

    caption_text = message.text.strip()
    state['caption'] = caption_text

    bot.send_message(message.chat.id, "📸 Endi nechta rasm yubormoqchisiz? (faqat raqam, maksimal 8 ta):")
    bot.register_next_step_handler_by_chat_id(message.chat.id, ask_number_of_photos)

def ask_number_of_photos(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if not state or 'caption' not in state:
        bot.send_message(message.chat.id, "❗ Avval izoh yuboring.")
        return

    try:
        count = int(message.text.strip())
        if count < 1 or count > 8:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "❗ Iltimos, 1 dan 8 gacha bo‘lgan raqam kiriting.")
        bot.register_next_step_handler_by_chat_id(message.chat.id, ask_number_of_photos)
        return

    state['expected_photos'] = count
    state['received_photos'] = 0
    state['photos'] = []

    # Papka ochamiz
    folder = f'downloads/user_{user_id}'
    os.makedirs(folder, exist_ok=True)

    bot.send_message(message.chat.id, f"📤 Iltimos, 1-rasmni yuboring:")
    bot.register_next_step_handler_by_chat_id(message.chat.id, receive_photo)

def receive_photo(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if not state or 'caption' not in state:
        bot.send_message(message.chat.id, "❗ Avval hududni tanlang va izoh yuboring.")
        return

    folder = f'downloads/user_{user_id}'

    # Faqat rasm bo‘lishini tekshiramiz
    if not message.photo:
        bot.send_message(message.chat.id, "❗ Iltimos, rasm yuboring (matn emas).")
        bot.register_next_step_handler_by_chat_id(message.chat.id, receive_photo)
        return

    state['received_photos'] += 1
    idx = state['received_photos']

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    file_path = os.path.join(folder, f"{idx}.jpg")
    with open(file_path, 'wb') as f:
        f.write(downloaded)

    state['photos'].append(file_path)

    if state['received_photos'] < state['expected_photos']:
        bot.send_message(message.chat.id, f"📤 Endi {idx+1}-rasmni yuboring:")
        bot.register_next_step_handler_by_chat_id(message.chat.id, receive_photo)
    else:
        # Hammasi tayyor, rasm va izohni yuboramiz
        send_album(message)

def send_album(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if not state or not state['photos']:
        bot.send_message(message.chat.id, "❗ Rasmlar topilmadi.")
        return

    # Endi userdan telefon raqamini so‘raymiz
    bot.send_message(message.chat.id, "📞 Iltimos, telefon raqamingizni kiriting. Masalan: +998901234567")
    bot.register_next_step_handler_by_chat_id(message.chat.id, save_user_phone)


def save_user_phone(message):
    user_id = str(message.from_user.id)
    phone = message.text.strip()

    # Telefon raqamini tekshirish
    if not (phone.startswith('+998') and len(phone) == 13 and phone[1:].isdigit()):
        bot.send_message(message.chat.id, "❗ Noto‘g‘ri format! Telefon raqamingizni +998 bilan, to‘g‘ri yozing. Masalan: +998901234567")
        bot.register_next_step_handler_by_chat_id(message.chat.id, save_user_phone)
        return

    # users.json ga yozamiz yoki yangilaymiz
    import json
    import os

    if not os.path.exists('users.json'):
        users = {}
    else:
        with open('users.json', 'r', encoding='utf-8') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}

    users[user_id] = users.get(user_id, {})
    users[user_id]['num'] = phone
    users[user_id]['id'] = user_id
    users[user_id]['name'] = message.from_user.first_name or ""
    users[user_id]['last'] = message.from_user.last_name or ""

    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    # Endi rasmlar va caption bilan e'lonni guruhga jo‘natamiz
    state = user_states.get(int(user_id))
    if not state or not state['photos']:
        bot.send_message(message.chat.id, "❗ Rasmlar topilmadi.")
        return

    caption_text = state['caption']
    media = []
    for idx, photo_path in enumerate(state['photos']):
        if idx == 0:
            media.append(types.InputMediaPhoto(open(photo_path, 'rb'), caption=caption_text))
        else:
            media.append(types.InputMediaPhoto(open(photo_path, 'rb')))

    try:
        bot.send_media_group(state['chat_id'], media)
    except Exception as e:
        bot.send_message(message.chat.id, f"❗ Xatolik yuz berdi: {e}")

    # Fayllarni yopamiz
    for m in media:
        if hasattr(m.media, 'close'):
            m.media.close()

    # Papkani o‘chir
    shutil.rmtree(f'downloads/user_{user_id}', ignore_errors=True)
    user_states.pop(int(user_id), None)

    bot.send_message(message.chat.id, "✅ E'lon jo'natildi!")
    send_main_menu(message.chat.id)















@bot.callback_query_handler(func=lambda call: call.data == 'elon_sotish')
def handle_sotish(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Viloyatlar ro‘yxatini fayldan o‘qish
    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(v, callback_data=f"vil_{v}") for v in viloyatlar]
    markup.add(*buttons)

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Uy sotib olish uchun viloyatni tanlang:",
        reply_markup=markup
    )










@bot.callback_query_handler(func=lambda call: call.data == 'elon_sotish')
def handle_sotish(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Viloyatlar ro‘yxatini fayldan o‘qish
    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(v, callback_data=f"vil_{v}") for v in viloyatlar]
    markup.add(*buttons)

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Uy sotish uchun viloyatni tanlang:",
        reply_markup=markup
    )



@bot.callback_query_handler(func=lambda call: call.data == 'elon_yer')
def handle_sotish(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Viloyatlar ro‘yxatini fayldan o‘qish
    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(v, callback_data=f"vil_{v}") for v in viloyatlar]
    markup.add(*buttons)

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Bo'sh yer sotish uchun viloyatni tanlang:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == 'elon_dokon_sot')
def handle_sotish(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Viloyatlar ro‘yxatini fayldan o‘qish
    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(v, callback_data=f"vil_{v}") for v in viloyatlar]
    markup.add(*buttons)

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Do'kon sotish uchun viloyatni tanlang:",
        reply_markup=markup
    )



@bot.callback_query_handler(func=lambda call: call.data == 'elon_dokon_ijara')
def handle_sotish(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Viloyatlar ro‘yxatini fayldan o‘qish
    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(v, callback_data=f"vil_{v}") for v in viloyatlar]
    markup.add(*buttons)

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Do'kon ijaraga berish uchun viloyatni tanlang:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == 'elon_dokon_ijara')
def handle_sotish(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Viloyatlar ro‘yxatini fayldan o‘qish
    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(v, callback_data=f"vil_{v}") for v in viloyatlar]
    markup.add(*buttons)

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Noturar bino sotish uchun viloyatni tanlang:",
        reply_markup=markup
    )



@bot.callback_query_handler(func=lambda call: call.data == 'elon_noto_sot')
def handle_sotish(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Viloyatlar ro‘yxatini fayldan o‘qish
    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(v, callback_data=f"vil_{v}") for v in viloyatlar]
    markup.add(*buttons)

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Noturar sotish uchun viloyatni tanlang:",
        reply_markup=markup
    )



@bot.callback_query_handler(func=lambda call: call.data == 'elon_noto_olish')
def handle_sotish(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # Viloyatlar ro‘yxatini fayldan o‘qish
    try:
        with open('viloyatlar.json', 'r', encoding='utf-8') as f:
            viloyatlar = json.load(f)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❗ Viloyatlar faylini o‘qishda xatolik yuz berdi.")
        return

    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [InlineKeyboardButton(v, callback_data=f"vil_{v}") for v in viloyatlar]
    markup.add(*buttons)

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Noturar ijaraga berish uchun viloyatni tanlang:",
        reply_markup=markup
    )

import threading
import time

# Ishga tushirish
print("Bot ishga tushdi...")
from requests.exceptions import ReadTimeout, ConnectionError

def start_polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except (ReadTimeout, ConnectionError) as e:
            print(f"Internet bilan bog'liq muammo: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"Boshqa xatolik: {e}")
            time.sleep(5)

# Pollingni alohida oqimda ishga tushiramiz
polling_thread = threading.Thread(target=start_polling)
polling_thread.daemon = True  # Ctrl+C bo‘lganda asosiy oqim bilan birga to‘xtaydi
polling_thread.start()

# Asosiy oqim faqat kutadi va Ctrl+C ni ushlab turadi
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nBot to‘xtatildi (Ctrl+C bosildi).")