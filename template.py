import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '7392647681:AAGlxvIThfWENxMQUx28DdlqLFZZPd53Bnc'
bot = telebot.TeleBot(TOKEN)




































import json

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

    buttons = [InlineKeyboardButton(v, callback_data=f"vilsotish_{v}") for v in viloyatlar]
    markup.add(*buttons)

    # Orqaga tugmasi
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data='back_elon'))

    bot.send_message(
        call.message.chat.id,
        "Viloyatni tanlang:",
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
        InlineKeyboardButton("🏢 Noturar bino sotib olish", callback_data='elon_noto_olish'),
        InlineKeyboardButton("🔙 Orqaga", callback_data='back_main')
    )
    bot.send_message(
        call.message.chat.id,
        "📢 Elon berish uchun kategoriya tanlang:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('vilsotish_'))
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

user_states = {}  # user_id: chat_link

user_states = {}  # user_id: chat_id

@bot.callback_query_handler(func=lambda call: call.data.startswith('hud_'))
def handle_hudud(call):
    hudud_nomi = call.data[4:]

    with open('hududlar.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    chat_id = None
    for vil in data.values():
        for h in vil:
            if h['name'] == hudud_nomi:
                chat_id = h['chat_id']
                break
        if chat_id:
            break

    if not chat_id:
        bot.send_message(call.message.chat.id, "❗ Hudud topilmadi.")
        return

    user_states[call.from_user.id] = chat_id

    bot.send_message(call.message.chat.id, "📝 Mana shunday e'lon tashlaysiz:\nNamuna e'lon matni yoki rasm/video bilan")
    bot.send_message(call.message.chat.id, "✏️ Endi e'loningizni yuboring (rasm, video, matn – farqi yo‘q):")
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, handle_user_post)

def handle_user_post(message):
    user_id = message.from_user.id
    chat_id = user_states.get(user_id)

    if not chat_id:
        bot.send_message(message.chat.id, "❗ Hudud ma'lum emas. Iltimos, boshidan tanlang.")
        return

    try:
        bot.forward_message(chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, "✅ E'loningiz muvaffaqiyatli yuborildi!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❗ Xatolik yuz berdi: {e}")