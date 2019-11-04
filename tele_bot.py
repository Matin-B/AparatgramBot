from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, \
    CallbackQueryHandler, InlineQueryHandler
from telegram import InlineKeyboardButton, \
    InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    ChatAction, ParseMode, \
    InputTextMessageContent, \
    InlineQueryResultArticle
from Aparat import Search, Downloader
from uuid import uuid4
from time import sleep


def start(bot, update):
    chatId = update.message.chat_id
    fromUser = update.message.from_user
    userFullName = fromUser.full_name
    bot.sendMessage(chatId, f'Welcome {userFullName}')


def help(bot, update):
    chatId = update.message.chat_id
    messageId = update.message.message_id
    bot.sendMessage(chatId,
        'This is help text',
        reply_to_message_id = messageId)


def searchInline(bot, update):
    query = update.inline_query.query
    if len(query) != 0:
        searchData, searchThumb, searchDuration = Search(query)
        if searchData != 'error':
            results = list()
            for count, item in enumerate(searchData.items()):
                key = item[0]
                value = item[1]
                results.append(
                    InlineQueryResultArticle(
                        id = uuid4(),
                        title = key,
                        thumb_url = searchThumb[count],
                        description = searchDuration[count],
                        input_message_content = InputTextMessageContent(value)))
        bot.answerInlineQuery(update.inline_query.id, results=results)


def dl(bot, update):
    chatId = update.message.chat_id
    messageId = update.message.message_id
    text = update.message.text
    if 'aparat.com' in text:
        url = text
        if Downloader(url) != 'error':
            vidTitle, dlData = Downloader(url)
            keyboard = list()
            for key, value in dlData.items():
                keyboard.append([InlineKeyboardButton(f'کیفیت {key}', value)])
            bot.sendMessage(chatId,
                text = f'Name: `{vidTitle}`\n\n\nDownload Links:',
                reply_markup = InlineKeyboardMarkup(keyboard),
                parse_mode = ParseMode.MARKDOWN)
        else:
            bot.sendMessage(chatId,
                'Your Link is Wrong, Please Check it !!',
                reply_to_message_id = messageId)
    else:
        bot.sendMessage(chatId,
            'Link is wrong !!!',
            reply_to_message_id = messageId)


def main():
    token = Updater('854700824:AAHhVDnL97JmJZzGKRwAtfJyL4QDIPIYe_8')

    dp = token.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))

    dp.add_handler(InlineQueryHandler(searchInline))

    dp.add_handler(MessageHandler(Filters.text, dl))


    token.start_polling()
    token.idle()

if __name__ == '__main__':
    main()
