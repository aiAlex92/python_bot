import os
import time

from replit import db

from telegram import (Bot, Update, Message, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, user)  #upm package(python-telegram-bot)
from telegram.ext import (Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext)  #upm package(python-telegram-bot)
from telegram.utils.helpers import escape_markdown 
from telegram.constants import MAX_MESSAGE_LENGTH

from parser_site import parse_techcrunch

def news_command(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_chat.id
    print(f"Show news for {user_id}")

    msg_text = f"*Главные новости:*\n\n"

    for idx, article in enumerate(parse_techcrunch()):
        new_part = f"{idx + 1}. {escape_markdown(str(article))}\n\n"

        if len(msg_text + new_part) <= MAX_MESSAGE_LENGTH:
            msg_text += new_part
        else:
            break

    update.message.reply_text(
        msg_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )

    inline_keyboard = InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton("Новость №1", callback_data="number_n:n1"), 
          InlineKeyboardButton("Новость №2", callback_data="number_n:n2"), 
          InlineKeyboardButton("Новость №3", callback_data="number_n:n3")
        ]
      ]
    )

    text = f"""
    Выберите новость
        """
    
    update.message.reply_text(text, reply_markup=inline_keyboard)


def selected_news(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    
  
    # context.bot.send_message(user_id, update.callback_query.data)


def main():
    updater = Updater("1749703925:AAFAYnEJKRZNTNhfx0FSX4YxHa5-QpVuvxA")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("news", news_command, run_async=True))
    dispatcher.add_handler(CallbackQueryHandler(selected_news, pattern="number_n:n1"))
    dispatcher.add_handler(CallbackQueryHandler(selected_news, pattern="number_n:n2"))
    dispatcher.add_handler(CallbackQueryHandler(selected_news, pattern="number_n:n3"))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()