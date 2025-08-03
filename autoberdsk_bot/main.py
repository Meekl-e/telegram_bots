from telebot import TeleBot, types, apihelper
import json
import os
from dotenv import load_dotenv

load_dotenv()

with open("messages.json", "r", encoding="UTF-8") as f:
    messages = json.load(f)

messages_quied = {}
ADMIN_ID =os.environ["ADMIN_ID"]
LOG_ID = os.environ["LOG_ID"]

rubricks = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1 = types.KeyboardButton(messages["buttons"]["ДТП"])
bt2 = types.KeyboardButton(messages["buttons"]["Пожар"])
bt3 = types.KeyboardButton(messages["buttons"]["Другое"])
rubricks.add(bt1, bt2, bt3)

confirm = types.InlineKeyboardMarkup()
btConfirm1 = types.InlineKeyboardButton(messages["buttons"]["Confirm"], callback_data="send")
btConfirm2 = types.InlineKeyboardButton(messages["buttons"]["Deny"], callback_data="change")
btConfirm3 = types.InlineKeyboardButton(messages["buttons"]["DeleteAllPhotos"], callback_data="delete_all_photos")
confirm.add(btConfirm1, btConfirm2)
confirm.add(btConfirm3)

confirm_after_photos = types.InlineKeyboardMarkup()
afterPhotosConfBtn = types.InlineKeyboardButton(messages["buttons"]["Confirm"], callback_data="confirm_after_photos")
btnDeletePhoto = types.InlineKeyboardButton(messages["buttons"]["DeletePhoto"], callback_data="delete_photo")
confirm_after_photos.add(afterPhotosConfBtn, btConfirm2 )
confirm_after_photos.add(btnDeletePhoto)

after_deleteons = types.InlineKeyboardMarkup()
after_deleteons.add(afterPhotosConfBtn, btConfirm2)

no_photo = types.InlineKeyboardMarkup()
np1 = types.InlineKeyboardButton(messages["buttons"]["Confirm"], callback_data="continue")
np2 = types.InlineKeyboardButton(messages["buttons"]["Photo"], callback_data="photo")
no_photo.add(np1, np2)


bot = TeleBot(token=os.environ["TOKEN"])


@bot.message_handler(commands=["start"])
def start(message):
    messages_quied[message.from_user.id] = None
    bot.send_message(message.chat.id, messages["messages"]["start"].replace("{name}", message.from_user.first_name), parse_mode="html",
                     reply_markup=rubricks,)


@bot.message_handler(content_types=["text"])
def proceed(msg):
    try:
        id = msg.from_user.id
        if messages_quied.get(id) is None:
            messages_quied[id] = {
                "topic":msg.text.lower().capitalize(),
                "media":[]
            }
            bot.send_message(msg.chat.id, messages["messages"]["msg_question"],reply_markup=types.ReplyKeyboardRemove())
        else:
            messages_quied[id]["message"] = msg.text
            bot.send_message(msg.chat.id, messages["messages"]["msg_confirm"].replace("{msg}",msg.text),reply_markup=confirm)

            if len(messages_quied[id].get("media"))>0:
                bot.send_message(msg.chat.id, messages["messages"]["and_photos"])
                for p, t, i in messages_quied[id].get("media"):
                    if t == "photo":
                        bot.send_photo(msg.chat.id, p)
                    elif t=="video":
                        bot.send_video(msg.chat.id, p)
                    elif t == "document":
                        bot.send_document(msg.chat.id, p)
    except Exception as e:
        bot.send_message(LOG_ID, f"{e}\nFrom message:{msg}\nFrom user:{msg.from_user}")

@bot.callback_query_handler(func= lambda callback:callback.data == "confirm_after_photos")
def confirm_photos(callback):
    try:
        if messages_quied[callback.from_user.id].get("message") is None:
            bot.edit_message_text(messages["messages"]["msg_question"], callback.message.chat.id, callback.message.id)
            return
        text = messages_quied[callback.from_user.id]["message"]
        msg = callback.message
        bot.send_message(msg.chat.id, messages["messages"]["msg_confirm"].replace("{msg}", text), reply_markup=confirm)

        if len(messages_quied[callback.from_user.id].get("media")) > 0:
            bot.send_message(msg.chat.id, messages["messages"]["and_photos"])
            for p, t, i in messages_quied[callback.from_user.id].get("media"):
                if t == "photo":
                    bot.send_photo(msg.chat.id, p)
                elif t == "video":
                    bot.send_video(msg.chat.id, p)
                elif t == "document":
                    bot.send_document(msg.chat.id, p)
    except Exception as e:
        bot.send_message(LOG_ID, f"{e}\nFrom message:{callback.message}\nWith data:{callback.data}\nFrom user:{callback.from_user}")

@bot.callback_query_handler(func = lambda callback:callback.data == "delete_photo")
def delete_file(callback):
    try:
        id = callback.from_user.id
        msg = callback.message
        if len(messages_quied[id]["media"]) > 0:
            p_to_delete = callback.message.reply_to_message
            if p_to_delete.content_type == "video":
                idx = 0
                for p, t, i in messages_quied[id]["media"]:
                    if i == p_to_delete.video.file_id:
                        messages_quied[id]["media"].pop(idx)
                        break
                    idx+=1
            elif p_to_delete.content_type == "photo":
                idx = 0
                for p, t, i in messages_quied[id]["media"]:
                    if i == p_to_delete.photo[-1].file_id:
                        messages_quied[id]["media"].pop(idx)
                        break
                    idx+=1
            elif p_to_delete.content_type == "document":
                idx = 0
                for p, t, i in messages_quied[id]["media"]:
                    if i == p_to_delete.document.file_id:
                        messages_quied[id]["media"].pop(idx)
                        break
                    idx+=1
            bot.edit_message_text(messages["messages"]["already_deleted"], msg.chat.id, msg.id, reply_markup=after_deleteons)
        else:
            bot.send_message(msg.chat.id, messages["messages"]["file_not_found"],
                                  reply_markup=after_deleteons)
    except Exception as e:
        bot.send_message(LOG_ID, f"{e}\nFrom message:{callback.message}\nWith data:{callback.data}\nFrom user:{callback.from_user}")


@bot.callback_query_handler(func = lambda callback:callback.data == "delete_all_photos")
def delete_file(callback):
    try:
        id = callback.from_user.id
        msg = callback.message
        if len(messages_quied[id]["media"]) > 0:
            messages_quied[id]["media"].clear()
            bot.send_message(msg.chat.id, messages["messages"]["all_deleted"], reply_markup=after_deleteons)
        else:
            bot.send_message(msg.chat.id, messages["messages"]["file_not_found"], reply_markup=after_deleteons)
    except Exception as e:
        bot.send_message(LOG_ID, f"{e}\nFrom message:{callback.message}\nWith data:{callback.data}\nFrom user:{callback.from_user}")


@bot.callback_query_handler(func= lambda callback: True)
def call_back(callback):
    try:
        if callback.data == "send":
            if len(messages_quied[callback.from_user.id].get("media"))==0:
                bot.edit_message_text(messages["messages"]["no_photo"], callback.message.chat.id, callback.message.id,
                                      reply_markup=no_photo, parse_mode="html")
                return
            elif messages_quied[callback.from_user.id].get("message") is None:
                bot.edit_message_text(messages["messages"]["msg_question"], callback.message.chat.id, callback.message.id)
                return
            t = messages_quied[callback.from_user.id]["topic"]
            msgU = messages_quied[callback.from_user.id]["message"]
            if t is None:
                t = "Нет"
            if msgU is None:
                msgU = "Нет"
            txt = messages["messages"]["news"].replace("{user}", callback.from_user.username).replace("{topic}",t ).replace("{text}",msgU)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(messages["buttons"]["Contact"],url="https://t.me/"+callback.from_user.username))
            bot.send_message(ADMIN_ID, txt, reply_markup=markup)
            bot.send_message(ADMIN_ID, messages["messages"]["and_photos"])
            for p, t, i in messages_quied[callback.from_user.id].get("media"):
                if t == "photo":
                    bot.send_photo(ADMIN_ID, p)
                elif t == "video":
                    bot.send_video(ADMIN_ID, p)
                elif t == "document":
                    bot.send_document(ADMIN_ID, p)
            bot.edit_message_text( messages["messages"]["already_send"],callback.message.chat.id, callback.message.id)
            messages_quied.pop(callback.from_user.id)
        elif callback.data == "change":
            messages_quied[callback.from_user.id]["message"] = None
            bot.edit_message_text(messages["messages"]["msg_question"], callback.message.chat.id, callback.message.id)
        elif callback.data == "photo":
            bot.edit_message_text(messages["messages"]["photo_add"], callback.message.chat.id, callback.message.id)
        elif callback.data == "continue":
            t = messages_quied[callback.from_user.id]["topic"]
            msg = messages_quied[callback.from_user.id]["message"]
            if t is None:
                t = "Нет"
            if msg is None:
                msg = "Нет"
            txt = messages["messages"]["news"].replace("{user}", callback.from_user.username).replace("{topic}", t).replace(
                "{text}", msg)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(messages["buttons"]["Contact"],
                                                  url="https://t.me/" + callback.from_user.username))
            bot.send_message(ADMIN_ID, txt, reply_markup=markup)

            bot.edit_message_text(messages["messages"]["already_send"], callback.message.chat.id, callback.message.id)
            messages_quied.pop(callback.from_user.id)
    except Exception as e:
        bot.send_message(LOG_ID, f"{e}\nFrom message:{callback.message}\nWith data:{callback.data}\nFrom user:{callback.from_user}")

@bot.message_handler(content_types=["photo"])
def getPhoto(msg):
    message_upload = bot.send_message(msg.chat.id, messages["messages"]["upload_loading"], reply_to_message_id=msg.id)
    if messages_quied.get(msg.from_user.id) is None:
        messages_quied[msg.from_user.id] = {"topic":"Нет","media":[]}
    elif messages_quied[msg.from_user.id].get("media") is None:
        messages_quied[msg.from_user.id]["media"] =  []
    try:
        file_info = bot.get_file(msg.photo[-1].file_id)
    except apihelper.ApiTelegramException as e:
        bot.edit_message_text(messages["messages"]["too_big_file"], msg.chat.id, message_upload.id,
                              reply_markup=confirm)
        return
    try:
        downloaded_file = bot.download_file(file_info.file_path)
        messages_quied[msg.from_user.id]["media"].append((downloaded_file, "photo", msg.photo[-1].file_id))
        bot.edit_message_text(messages["messages"]["photo_completed"], msg.chat.id,message_upload.id,  reply_markup=confirm_after_photos)
    except Exception as e:
        bot.send_message(LOG_ID, f"{e}\nFrom message:{msg}\nFrom user:{msg.from_user}")


@bot.message_handler(content_types=["video"])
def getVideo(msg):
    message_upload = bot.send_message(msg.chat.id, messages["messages"]["upload_loading"], reply_to_message_id=msg.id)
    if messages_quied.get(msg.from_user.id) is None:
        messages_quied[msg.from_user.id] = {"topic":"Нет","media":[]}
    elif messages_quied[msg.from_user.id].get("media") is None:
        messages_quied[msg.from_user.id]["media"] =  []
    try:
        file_info = bot.get_file(msg.video.file_id)
    except apihelper.ApiTelegramException as e:
        bot.edit_message_text(messages["messages"]["too_big_file"], msg.chat.id, message_upload.id,
                              reply_markup=confirm)
        return
    try:
        downloaded_file = bot.download_file(file_info.file_path)
        messages_quied[msg.from_user.id]["media"].append((downloaded_file, "video", msg.video.file_id))
        bot.edit_message_text(messages["messages"]["video_completed"], msg.chat.id,message_upload.id,  reply_markup=confirm_after_photos)
    except Exception as e:
        bot.send_message(LOG_ID, f"{e}\nFrom message:{msg}\nFrom user:{msg.from_user}")


@bot.message_handler(content_types=["document"])
def getDoc(msg):
    message_upload = bot.send_message(msg.chat.id, messages["messages"]["upload_loading"], reply_to_message_id=msg.id)
    if messages_quied.get(msg.from_user.id) is None:
        messages_quied[msg.from_user.id] = {"topic":"Нет","media":[]}
    elif messages_quied[msg.from_user.id].get("media") is None:
        messages_quied[msg.from_user.id]["media"] =  []
    try:
        file_info = bot.get_file(msg.document.file_id)
    except apihelper.ApiTelegramException as e:
        bot.edit_message_text(messages["messages"]["too_big_file"], msg.chat.id, message_upload.id,
                              reply_markup=confirm)
        return
    try:
        downloaded_file = bot.download_file(file_info.file_path)
        messages_quied[msg.from_user.id]["media"].append((downloaded_file, "document", msg.document.file_id))
        bot.edit_message_text(messages["messages"]["document_completed"], msg.chat.id,message_upload.id,  reply_markup=confirm_after_photos)
    except Exception as e:
        bot.send_message(LOG_ID, f"{e}\nFrom message:{msg}\nFrom user:{msg.from_user}")




bot.infinity_polling()
