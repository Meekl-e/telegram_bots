import os

from telebot import *
import ClassAPI
import CompareMessage as cm
import Keyboards as kb
import datetime
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("TOKEN")


bot = TeleBot(TOKEN)

wordPressAPI = ClassAPI.API("svidetel24.info")

dailyNews = [0, str(datetime.datetime.now().date())]
dailyViews = [0, str(datetime.datetime.now().date())]
dailyStart = [0, str(datetime.datetime.now().date())]

@bot.message_handler(commands=["start"])
def sendMenu(message, hi=True):
    global dailyStart
    if str(datetime.datetime.now().date()) != dailyStart[1]:
        dailyStart = [0, str(datetime.datetime.now().date())]
    dailyStart[0] +=1
    bot.send_photo(message.chat.id, photo="https://github.com/nikita23343/imagesBot/blob/main/logo.png?raw=true",
                   caption=cm.compareStartMessage(message.from_user.first_name, hi), parse_mode="html", reply_markup=kb.menuKeyboard())
    return True


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def callback_inline(call):
    global dailyNews
    new = wordPressAPI.getNew(id=call.data)
    if new == None:
        news = wordPressAPI.rubricks
        bot.send_photo(call.from_user.id, photo="https://github.com/nikita23343/imagesBot/blob/main/404.png?raw=true",
                       caption=cm.notFoundNews() + cm.choiceRubrick(news),
                       parse_mode="html",
                       reply_markup=kb.rubrickMenu(news))
        return True
    photo = cm.getPhoto(new[2])
    if str(datetime.datetime.now().date()) != dailyNews[1]:
        dailyNews = [0, str(datetime.datetime.now().date())]
    dailyNews[0] +=1
    if photo !=None:
        bot.send_photo(call.from_user.id, photo=cm.getPhoto(new[2]),
                   caption=cm.compare_news(new[1],new[2], new[3]), parse_mode="html", reply_markup=kb.newkeyboard(new, "menuS") )
    else:
        bot.send_message(call.from_user.id,
                       text=cm.compare_news(new[1], new[2], new[3]), parse_mode="html",
                       reply_markup=kb.newkeyboard(new, "menuS"))
    return True


@bot.callback_query_handler(func=lambda call: call.data.startswith("to"))
def callback_ToMenu(call):
    global dailyStart
    d = call.data[2:]

    if d == "newNews":
        callback_inline(call)
    elif d == "menu":
        if str(datetime.datetime.now().date()) != dailyStart[1]:
            dailyStart = [0, str(datetime.datetime.now().date())]
        dailyStart[0] += 1
        bot.edit_message_caption(
            caption=cm.compareStartMessage(call.from_user.first_name),
            parse_mode="html",
            message_id=call.message.message_id, chat_id=call.message.chat.id,
            reply_markup=kb.menuKeyboard())
    elif d == "menuS":
        sendMenu(call.message, hi=False)
    return True



@bot.callback_query_handler(func=lambda call: call.data.startswith("Rubrick-"))
def callback_RubrickMenu(call):

    d = call.data[8:]

    if d == "all":
        bot.edit_message_caption(
            caption=cm.choiceRubrick(wordPressAPI.rubricks),
            parse_mode="html",
            message_id=call.message.message_id, chat_id=call.message.chat.id,
            reply_markup=kb.rubrickMenu(wordPressAPI.rubricks))
    elif d == "-1":
        d = int(d)
        news = wordPressAPI.get_todayNews()
        bot.send_message(call.message.chat.id,
                         cm.compare_message(d, list(news)),
                         parse_mode="html",
                         reply_markup=kb.newsKeyboard(news))

    elif d.isdigit():
        d = int(d)
        news = wordPressAPI.getRubrickNews(id=d)

        bot.send_message(call.message.chat.id,
                         cm.compare_message(d, list(news)),
                         parse_mode="html",
                         reply_markup=kb.newsKeyboard(news))
    return True

@bot.callback_query_handler(func=lambda call: call.data.startswith("view-"))
def veiwNew(call):
    global dailyViews
    if str(datetime.datetime.now().date()) != dailyViews[1]:
        dailyViews = [0, str(datetime.datetime.now().date())]
    dailyViews[0] +=1
    d = int(call.data[5:])
    new = wordPressAPI.getNew(d)
    bot.send_message(call.message.chat.id, text=cm.compareAllNew(new),
                     parse_mode="html", reply_markup=kb.newkeyboard(new, "menuS",False))
    return True



@bot.message_handler(commands=["about"])
def sendAboutCommand(message):
    bot.send_message(message.chat.id,
                     text=cm.compareAbout(),
                     parse_mode="html",
                     reply_markup=kb.aboutKeyboard())

@bot.callback_query_handler(func=lambda call: call.data == "about")
def sendAbout(call):
    sendAboutCommand(call.message)


@bot.message_handler(content_types=["text"])
def getMessageUser(message):
    if message.text == "Дай-Статистику281":
        bot.send_message(message.chat.id, text=f"За день просмотрели новостей: {dailyNews[0]}\nЗа день просмотрели новостей (полностью): {dailyViews[0]}")

    if message.text.startswith("/rate"):
        if message.text.split() == ["/rate"]:
            bot.send_message(message.chat.id,
                         text="Пожалуйста, напишите отзыв после /rate",
                         parse_mode="html")
            return True
        bot.send_message(1499946663, text="Отзыв от "+ message.from_user.first_name+" ( " + message.from_user.username +" )\n" + message.text)
        bot.send_message(message.chat.id,
                         text="Спасибо за ваш отзыв!",
                         parse_mode="html")
        sendMenu(message)


bot.infinity_polling()