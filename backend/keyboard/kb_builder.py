from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_stats():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='📊 Статистика', callback_data='stats'))
    return markup

def prelink():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='♻️ Создать новую ссылку', callback_data='prelink'))
    markup.add(InlineKeyboardButton(text='👻 Сбросить ссылку', callback_data='relink'))
    return markup

def cancel():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='❌ Отменить', callback_data='cancel'))
    return markup
