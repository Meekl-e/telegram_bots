import re

titles = {-1:'⬇️ Последние новости ⬇️',
          88: '🎭 Последняя афиша 🎭',
          676: '🕵 Рубрика безопасность 🕵',
          1726: '💵 Новости бизнеса 💵',
          29: '🌍 Новости в регионе 🌍',
          4: '⬇️ Рубрика власть ⬇️',
          27: '⚡Городское хозяйство⚡',
          6: '🌍 Рубрика жизнь 🌍',
          26: '❤️ Новости здоровья ❤️',

          51: '📖 Новости образования 📖',
          7: '⬇️ Рубрика Происшествия ⬇️ ',
          1038: '⚖️ Рубрика "Право" ⚖️',
          25: '💪 Новости спорта 🥇',
          23: '🏛️ Новости культуры 🏛️',
          3:'🚗 Последние ДТП 🚗\n<i>(По данным сайта autoberdsk.ru)</i>'}


def compare_message(title,listNews):
    string = ""
    if len(listNews) == 0:
        return titles[title] + "\n\n" + "<i>Похоже, сегодня в моих источниках не было новостей. Попробуйте сменить категорию. </i>"
    for i in range(len(listNews)):
        string += f"{i+1}. ➡️ " + str(listNews[i][1]) + f" |<i>{listNews[i][2]}</i>" +"\n\n"

    return titles[title]+"\n\n"+string + "<b>Подробнее о каждой новости:</b>"

def compareStartMessage(name, hi=True):
    if hi:
        return f"""<b>Добро пожаловать, {name}!</b>\nВы на главной странице "Свидетеля".\nЗдесь вы можете узнать о ДТП на Бердском шоссе и посмотреть последние новости Бердска.\n\n<b>Пожалуйста, выберите интересующую вас рубрику:</b>"""
    return """Вы на главной странице <b>"Свидетеля"</b>.\nЗдесь вы можете узнать о ДТП на Бердском шоссе и посмотреть последние новости Бердска.\n\n<b>Пожалуйста, выберите интересующую вас рубрику:</b>"""
def compare_news(title, content, date):
    content = re.sub(pattern=r'</*[a-z].*?>', repl='', string=content)
    content = re.sub(pattern=r'&nbsp;', repl=' ', string=content)

    try:
        idx = content.index("<!--more-->")
        return f"<b>{title}</b>\n\n{content[:idx]}<i>{re.sub('-', '.', date)}</i>"
    except ValueError:
        try:
            idx = len(content) - content[::-1].index("отоФ") - 4
            content = content[:idx]
        except ValueError:
            pass
        s = content.split()
        if len(s) > 100:
            content = " ".join(s[:100])+"..."
        content= re.sub(r'\n\n\n','\n', content)
        return f"<b>{title}</b>\n\n{content}\n<i>{re.sub('-', '.', date)}</i>"

def compareAllNew(new):
    title = new[1]
    content = new[2]
    date = new[3]
    content = re.sub(pattern=r'</*[a-z].*?>', repl='', string=content)
    content = re.sub(pattern=r'&nbsp;', repl=' ', string=content)
    content = re.sub(pattern="<!--more-->",repl="", string=content)
    try:
        idx = len(content) - content[::-1].index("отоФ") - 4
        content = content[:idx]
    except ValueError:
        pass
    lTitle = len(title)
    if len(content) + lTitle > 4096:
        content = content[:4091-lTitle]
        return f"<b>{title}</b>\n\n{content}..."
    return f"<b>{title}</b>\n\n{content}<i>{date}</i>"




def getPhoto(content):

    string = re.search(r'https://.*/uploads/.*">', content)
    if string == None:
        return None

    return string[0][:-2]

def notFoundNews():
    return "<b>Хмм...</b> \n Странно. Новость не найдена. \n <i>Возможно, вы пытаетесь найти удаленную/измененную новость.</i>\n\n"

def choiceRubrick(rubricks):

    string = ""
    for i, rubrick in enumerate(rubricks.keys()):
        string += f"{i+1}. ➡️ " + str(rubricks[rubrick]) + "\n\n"

    return f"""Пожалуйста, выберите интересующую вас рубрику.\n<b>Все рубрики:</b>\n\n{string}"""


def compareAbout():
    return "Данный бот был создан обычным человеком для вашего удобства. Программа работает в поддержке с редакцией газеты 'Свидетель' и сайтом 'АвтоБердск'.\n\nОчень жду предложения и пожелания по улучшению бота. Также буду очень благодарен за найденные баги и ошибки.\nВы можете оставить отзыв командой <i>/rate [ваш отзыв]</i>\n\nПриятного пользования ❤️\n<i>Версия ALPHA-1.1</i>"