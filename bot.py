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


def start_command(update, contex):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    contex.bot.send_message(
        chat_id,
        'سلام ✋\n\n✅ اگه برای من لینک ویدیو آپارات بفرستی میتونم'
        ' بصورت فایل یا لینک دانلود مستقیم برات بفرستم.\n\n\n'
        '🔍 برای سرچ تو آپارات میتونی طبق دستور زیر عمل کنی :\n'
        '`@AparatgramBot آموزش پایتون`',
        parse_mode=ParseMode.MARKDOWN,
        reply_to_message_id=message_id)


def help_command(update, contex):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    contex.bot.send_message(
        chat_id,
        'This is help text',
        reply_to_message_id=message_id)


def searchInline(update, contex):
    query = update.inline_query.query
    if len(query) != 0:
        searchData, searchThumb, searchDuration = search(query)
        if searchData != 'error':
            results = []
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
        contex.bot.answerInlineQuery(update.inline_query.id, results=results)


def generate_keyboard(links):
    keyboard = []
    for link in links:
        quality = link.split('-')[-1].split('__')[0]
        keyboard.append([InlineKeyboardButton(quality, url=link)])
    return keyboard


def text(update, contex):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    user_text = update.message.text
    if 'aparat.com' in user_text and '/playlist/' in user_text:
        playlist_detail = playlist(user_text)
        if 'Error' in playlist_detail:
            contex.bot.send_message(
                ADMIN,
                f'⚠️ Error\n\nLink: {user_text}\nError: `{playlist_detail}`',
                parse_mode=ParseMode.MARKDOWN
            )
            contex.bot.send_message(
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
            contex.bot.send_message(
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
                contex.bot.send_photo(
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
            contex.bot.send_message(
                ADMIN,
                f'⚠️ Error\n\nLink: {user_text}\nError: `{video_detail}`',
                parse_mode=ParseMode.MARKDOWN
            )
            contex.bot.send_message(
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
            contex.bot.send_photo(
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
        contex.bot.send_message(
            chat_id,
            'Link is wrong !!!',
            reply_to_message_id=message_id)


token = Updater(BOT_TOKEN, use_context=True)

dp = token.dispatcher

dp.add_handler(CommandHandler('start', start_command))
dp.add_handler(CommandHandler('help', help_command))

dp.add_handler(InlineQueryHandler(searchInline))

dp.add_handler(MessageHandler(Filters.text, text))


token.start_polling()
