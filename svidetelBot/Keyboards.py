from telebot.types import *


def newsKeyboard(news):
    keyboard = InlineKeyboardMarkup(row_width=1)
    if len(news) == 10:
        keyboard.row(*[InlineKeyboardButton(i + 1, callback_data=news[i][0]) for i in range(5)])
        keyboard.row(*[InlineKeyboardButton(i + 1, callback_data=news[i][0]) for i in range(5,10)])
    else:
        keyboard.row(*[InlineKeyboardButton(i + 1, callback_data=news[i][0]) for i in range(len(news))])

    keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="tomenuS"))
    return keyboard


def rubrickMenu(rubricks):
    rubricks = list(rubricks.keys())
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.row(*[InlineKeyboardButton(i + 1, callback_data="Rubrick-"+str(rubricks[i])) for i,r in enumerate(rubricks)])
    keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="tomenu"))
    return keyboard

def newkeyboard(new,title,view=True):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="to"+title), InlineKeyboardButton("Подробнее 🔗",url=new[0] ))
    if view:
        keyboard.row(InlineKeyboardButton("💬 Просмотреть новость здесь", callback_data="view-"+str(new[4])))
    return keyboard


def menuKeyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.row(InlineKeyboardButton("ДТП", callback_data="Rubrick-3"), InlineKeyboardButton("Афиша", callback_data="Rubrick-88"))
    keyboard.row(InlineKeyboardButton("Коммуналка", callback_data="Rubrick-27"), InlineKeyboardButton("Все рубрики", callback_data="Rubrick-all"))
    keyboard.row(InlineKeyboardButton("Последние новости", callback_data="Rubrick--1"), InlineKeyboardButton("О боте", callback_data="about"))
    return keyboard

def customKeyboard(titles, rubrick):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(*[InlineKeyboardButton(i, callback_data="Rubrick-"+rubrick+i) for i in titles])
    keyboard.row(InlineKeyboardButton("⬅️ Назад",callback_data="tomenu"))
    return keyboard

def aboutKeyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="tomenuS"))
    return keyboard

