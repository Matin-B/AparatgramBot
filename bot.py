from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, \
    CallbackQueryHandler, InlineQueryHandler
from telegram import InlineKeyboardButton, \
    InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    ChatAction, ParseMode, \
    InputTextMessageContent, \
    InlineQueryResultArticle
from Aparat import search, download, playlist
from config import BOT_TOKEN, ADMIN
from time import sleep
from uuid import uuid4


def start_command(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(
        chat_id,
        'سلام ✋\n\n✅ اگه برای من لینک ویدیو آپارات بفرستی میتونم'
        ' بصورت فایل یا لینک دانلود مستقیم برات بفرستم.\n\n\n'
        '🔍 برای سرچ تو آپارات میتونی طبق دستور زیر عمل کنی :\n'
        '`@AparatgramBot آموزش پایتون`',
        parse_mode=ParseMode.MARKDOWN)


def help_command(bot, update):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    bot.sendMessage(
        chat_id,
        'This is help text',
        reply_to_message_id=message_id)


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
                        id=uuid4(),
                        title=key,
                        thumb_url=searchThumb[count],
                        description=searchDuration[count],
                        input_message_content=InputTextMessageContent(value)))
        bot.answerInlineQuery(update.inline_query.id, results=results)


def generate_keyboard(links):
    keyboard = list()
    for link in links:
        quality = link.split('-')[-1].split('__')[0]
        keyboard.append([InlineKeyboardButton(quality, url=link)])
    return keyboard


def text(bot, update):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    user_text = update.message.text
    if 'aparat.com' in user_text and '/playlist/' in user_text:
        playlist_detail = playlist(user_text)
        if 'Error' in playlist_detail:
            bot.sendMessage(
                ADMIN,
                f'⚠️ Error\n\nLink: {user_text}\nError: `{playlist_detail}`',
                parse_mode=ParseMode.MARKDOWN
            )
            bot.sendMessage(
                chat_id,
                'مشکلی در پردازش لینک رخ داد.\n'
                'لینک مورد نظر جهت بررسی برای پشتیبانی ارسال شد',
                reply_to_message_id=message_id
            )
        else:
            title = playlist_detail['title']
            links = playlist_detail['links']
            count = playlist_detail['count']
            channel_name = playlist_detail['channel-name']
            channel_link = playlist_detail['channel-link']
            bot.sendMessage(
                chat_id,
                f'🖊 عنوان لیست پخش: {title}\n\n\n'
                f'ℹ️ کانال: {channel_name}\n'
                f'🔄 تعداد ویدیو: {count}',
                parse_mode=ParseMode.MARKDOWN,
                reply_to_message_id=message_id
            )
            for link in links:
                video_detail = download(link)
                title = video_detail['title']
                image = video_detail['image']
                links = video_detail['links']
                count = video_detail['count']
                likes = video_detail['likes']
                date = video_detail['date']
                description = video_detail['description']
                bot.sendPhoto(
                    chat_id,
                    image,
                    f'🖊 عنوان: {title}\n'
                    f'👁‍🗨 بازدید: {count}\n'
                    f'👍 لایک: {likes}\n'
                    f'📅 زمان آپلود: {date}\n'
                    f'📜 توضیحات: \n{description}\n',
                    reply_to_message_id=message_id + 1,
                    reply_markup=InlineKeyboardMarkup(generate_keyboard(links))
                )
                sleep(0.5)
    elif 'aparat.com' in user_text:
        video_detail = download(user_text)
        if 'Error' in video_detail:
            bot.sendMessage(
                ADMIN,
                f'⚠️ Error\n\nLink: {user_text}\nError: `{video_detail}`',
                parse_mode=ParseMode.MARKDOWN
            )
            bot.sendMessage(
                chat_id,
                'مشکلی در پردازش لینک رخ داد.\n'
                'لینک مورد نظر جهت بررسی برای پشتیبانی ارسال شد',
                reply_to_message_id=message_id
            )
        else:
            title = video_detail['title']
            image = video_detail['image']
            links = video_detail['links']
            count = video_detail['count']
            likes = video_detail['likes']
            date = video_detail['date']
            description = video_detail['description']
            bot.sendPhoto(
                chat_id,
                image,
                f'🖊 عنوان: {title}\n'
                f'👁‍🗨 بازدید: {count}\n'
                f'👍 لایک: {likes}\n'
                f'📅 زمان آپلود: {date}\n'
                f'📜 توضیحات: \n{description}\n',
                reply_to_message_id=message_id,
                reply_markup=InlineKeyboardMarkup(generate_keyboard(links))
            )
    else:
        bot.sendMessage(
            chat_id,
            'Link is wrong !!!',
            reply_to_message_id=message_id)


token = Updater(BOT_TOKEN)

dp = token.dispatcher

dp.add_handler(CommandHandler('start', start_command))
dp.add_handler(CommandHandler('help', help_command))

dp.add_handler(InlineQueryHandler(searchInline))

dp.add_handler(MessageHandler(Filters.text, text))


token.start_polling()
