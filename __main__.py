import telebot
import re
from backend import const

bot = telebot.TeleBot(const.TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    username = message.chat.username if message.chat.username else "Unknown"
    const.db.add_user(message.chat.id, message.chat.id, username)  
    params = message.text.split()
    if len(params) > 1:
        unique_id = params[1]
        if unique_id == "durov":
            return bot.send_message(message.chat.id, "Мы ценим вашу уникальность, но по этой ссылке нельзя написать).")
        bot.send_message(message.chat.id, const.messages["message_write"], reply_markup=const.cancel())
        const.waiting_for_message[message.chat.id] = unique_id
    else:
        messages = const.db.get_messages(message.chat.id)
        if messages:
            for msg in messages:
                bot.send_message(msg[2], const.messages["message_newmessage"].format(msg[3]))
                const.db.update_message_view(msg[0])
        bot.send_message(message.chat.id, const.messages["message_start"], reply_markup=const.get_stats())

@bot.message_handler(func=lambda message: message.chat.id in const.waiting_for_message)
def handle_user_message(message: telebot.types.Message):
    unique_id = const.waiting_for_message[message.chat.id]
    del const.waiting_for_message[message.chat.id]
    userid = const.db.get_user_uniqueid(unique_id)
    try:
        bot.send_message(userid, const.messages["message_newmessage"].format(message.text))
        statusmessage = "И оно уже пришло получателю"
    except BaseException:
        const.db.add_message(message.chat.id, userid, message.text)
        statusmessage = "⚠Получатель получит сообщение когда запустит бота⚠"
    bot.send_message(message.chat.id, const.messages["message_successful"].format(statusmessage))
    bot.send_message(message.chat.id, const.messages["message_reject"].format(f"https://t.me/{bot.user.username}?start={const.db.get_uniqueid(message.chat.id)}"), reply_markup=const.get_stats())

@bot.callback_query_handler(func=lambda call: True)
def button_handler(call: telebot.types.CallbackQuery):
    if call.data == "stats":
        bot.answer_callback_query(call.id, None)
        received, sent = const.db.getstats(call.message.chat.id)
        bot.send_message(call.message.chat.id, const.messages["message_stats"].format(received, sent, f"https://t.me/{bot.user.username}?start={const.db.get_uniqueid(call.message.chat.id)}"), reply_markup=const.prelink())
    elif call.data == "cancel":
        cancel(call.message)
        bot.send_message(call.message.chat.id, const.messages["message_reject"].format(f"https://t.me/{bot.user.username}?start={const.db.get_uniqueid(call.message.chat.id)}"))
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "prelink":
        bot.answer_callback_query(call.id, None)
        bot.send_message(call.message.chat.id, f'Укажите свою новую ссылку!\n\nСделай те красивую ссылку, пример: https://t.me/{bot.user.username}?start=durov\n\nПросто напиши ассоциацию! (Чтобы отменить напишите "отмена")')
        bot.register_next_step_handler(call.message, process_uniqueid)
        const.waiting_for_message[call.message.chat.id]
    elif call.data == "relink":
        bot.answer_callback_query(call.id, None)
        const.db.update_uniqueid(call.message.chat.id, call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"Ваша ссылка была успешно сброшена!\n\nТеперь она выглядит: https://t.me/{bot.user.username}?start={const.db.get_uniqueid(call.message.chat.id)}")
    
    

def cancel(message):
    if message.chat.id in const.waiting_for_message:
        del const.waiting_for_message[message.chat.id]
    return

def process_uniqueid(message: telebot.types.Message):
    uniqueid = message.text.strip()
    if uniqueid.lower() == "отмена":
        bot.send_message(message.chat.id, "Процесс создания ссылки был отменен. Its so bad..//")
        cancel(message)
        return

    if not re.match("^[a-zA-Z]{1,8}$", uniqueid):
        bot.send_message(message.chat.id, "Измените ссылку, она должна быть до 8 английских букв без пробелов, символов, цифр.")
        return
    if uniqueid == "durov":
        bot.send_message(message.chat.id, "Мы ценим вашу уникальность, но эту ссылку нельзя забрать.")
        return
    if const.db.check_uniqueid(uniqueid):
        bot.send_message(message.chat.id, "Эта ссылка уже занята. Пожалуйста, выберите другой.")
    else:
        const.db.update_uniqueid(message.chat.id, uniqueid)
        bot.send_message(message.chat.id, f"Ваш уникальный ссылка была успешно обновлена!\n\nТеперь она выглядит: https://t.me/{bot.user.username}?start={uniqueid}")
    bot.delete_message(message.chat.id, message.id)

bot.infinity_polling(skip_pending=True)