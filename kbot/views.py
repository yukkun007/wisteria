# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os

from django.conf import settings
from django.http import HttpResponse,\
                        HttpResponseBadRequest,\
                        HttpResponseRedirect,\
                        HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from kbot.kbot import KBot
from kbot.line import Line
from kbot.library.library import Library
from kbot.library.message import Message
from kbot.library.user import User
from kbot.library.filter import Filter
from kbot.library.yoyaku_book import YoyakuBook
from kbot.library.user_status import UserStatus
from kbot.log import Log
from kbot.google.gmail import GMail
from kbot.google.youtube import YouTube
from kbot.book.calil import Calil
from kbot.book.amazon import Amazon
from kbot.book.book import Book
from kbot.book.rakuten_books import RakutenBooks

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import ButtonsTemplate,\
                           URITemplateAction,\
                           MessageEvent,\
                           PostbackEvent,\
                           SourceGroup,\
                           SourceUser\


# 定数
KBOT_TEMPLATE_DIR = settings.PROJECT_ROOT + '/templates/kbot/'

# グローバル変数
KBOT          = KBot(settings.PROJECT_ROOT)
line_bot_api  = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
parser        = WebhookParser(os.environ['LINE_CHANNEL_SECRET'])
line          = Line(line_bot_api)
gmail         = GMail(settings.PROJECT_ROOT)
youtube       = YouTube(settings.PROJECT_ROOT)
users         = [User(os.environ['USER1']),
                User(os.environ['USER2']),
                User(os.environ['USER3']),
                User(os.environ['USER4'])]
gmail_tos     = [os.environ['GMAIL_SEND_ADDRESS1'],
                os.environ['GMAIL_SEND_ADDRESS2']]
line_tos      = [os.environ['LINE_SEND_GROUP_ID']]
if settings.DEBUG == True:
    line_tos = [os.environ['LINE_SEND_GROUP_ID_DEBUG']]
# line_tos = [os.environ['LINE_SEND_ID']]
calil         = Calil()
amazon        = Amazon()
rakuten_books = RakutenBooks()


def youtube_omoide(request):
    if request.method == 'GET':
        Log.info('GET! youtube_omoide')

        movie = youtube.get_youtube_movie()
        Log.info(movie.to_string())

        buttons_template = ButtonsTemplate(
            title=movie.title,
            text='投稿日: ' + movie.published_at,
            thumbnail_image_url=movie.url,
            actions=[
                URITemplateAction(
                    label = 'YouTubeへ',
                    uri   = 'https://www.youtube.com/watch?v=' + movie.video_id)
            ]
        )
        line.my_push_template_message(buttons_template, movie.title, line_tos)

        return HttpResponse('done! youtube_omoide')
    else:
        return HttpResponseBadRequest()


def library_test(request):
    if request.method == 'GET':
        Log.info('GET! library_test')

        xdays = 2
        library = Library(KBOT_TEMPLATE_DIR, users)
        library.fetch_status()
        library.do_filter(Filter(type=Filter.FILTER_NONE, xdays=xdays))
        # library.do_filter(Filter(type=Filter.FILTER_EXPIRE, xdays=xdays))
        # library.do_filter(Filter(type=Filter.FILTER_EXPIRED, xdays=xdays))
        short_message = library.get_message(type=Message.TYPE_SHORT)
        # line.my_push_text_message(short_message, line_tos)

        return HttpResponse('done! library_test')


def library_reserve(request):
    if request.method == 'GET':
        Log.info('GET! library_reserve')

        book_id = request.GET.get('book_id')
        if book_id != None:
            user_num = '1'
            library  = Library(KBOT_TEMPLATE_DIR, users)
            url      = library.yoyaku(user_num, book_id)

            template = YoyakuBook.make_finish_reserve_message_template(user_num)
            line.my_push_template_message(template, '予約完了', line_tos)

            return HttpResponseRedirect(url)
        else:
            line.my_push_text_message('予約失敗。。', line_tos)

        return HttpResponse('done! library_reserve')


def library_check_reserve(request):
    if request.method == 'GET':
        Log.info('GET! library_check_reserve')

        user_nums = '1,2,3,4'
        __check_reserved_books(None, user_nums)

        return HttpResponse('done! library_check_reserve')


def library_check(request):
    if request.method == 'GET':
        Log.info('GET! library_check')

        xdays = 2
        library = Library(KBOT_TEMPLATE_DIR, users)
        library.fetch_status()
        library.do_filter(Filter(type=Filter.FILTER_EXPIRE, xdays=xdays))
        if library.is_target_exist():
            short_message = library.get_message(type=Message.TYPE_SHORT)
            line.my_push_text_message(short_message, line_tos)
            long_message  = library.get_message(type=Message.TYPE_LONG)
            gmail.send_message_multi(
                gmail_tos,
                '図書館の本返却お願いします！',
                long_message)

        return HttpResponse('done! library_check')


@csrf_exempt
def callback(request):

    if request.method == 'POST':
        Log.info('POST! callback')

        try:
            signature = request.META['HTTP_X_LINE_SIGNATURE']
            body      = request.body.decode('utf-8')
            events    = parser.parse(body, signature)

            for event in events:

                if isinstance(event, MessageEvent):
                    text = event.message.text

                    if isinstance(event.source, SourceUser):
                        Log.info('userId' + event.source.user_id)
                    if isinstance(event.source, SourceGroup):
                        Log.info('groupId' + event.source.group_id)

                    if KBOT.is_search_book_command(text):
                        query = KBOT.get_search_book_query(text)
                        __search_book(event, query)

                    elif KBOT.is_check_reserve_command(text):
                        user_nums = '1,2,3,4'
                        __check_reserved_books(event, user_nums)

                    elif KBOT.is_rental_check_command(text):
                        __check_rental(event)

                    elif KBOT.is_expire_check_command(text):
                        xdays = KBOT.get_xdays(text)
                        __check_expire(event, xdays)

                    elif KBOT.is_expired_check_command(text):
                        __check_expired(event)

                    elif KBOT.is_reply_string_show_command(text):
                        __show_reply_string(event)

                    else:
                        template = KBOT.get_kbot_command_menu()
                        line.my_reply_template_message(template, event)

                elif isinstance(event, PostbackEvent):
                    data = event.postback.data
                    if data.startswith('isbn:'):
                        __search_book_by_isbn(event, data)
                    elif data.startswith('check_reserve:'):
                        user_nums = data[14:]
                        __check_reserved_books(event, user_nums)
                    # if data == 'check_rental':
                    #     __check_rental(event)
                    # elif data == 'check_expire':
                    #     xdays = 2
                    #     __check_expire(event, xdays)
                    # elif data == 'show_reply_string':
                    #     __show_reply_string(event)

        except InvalidSignatureError as e:
            Log.logging_exception(e)
            return HttpResponseForbidden()
        except LineBotApiError as e:
            Log.logging_exception(e)
            return HttpResponseBadRequest()
        except Exception as e:
            Log.logging_exception(e)

        return HttpResponse('done! callback')
    else:
        return HttpResponseBadRequest()


def __check_rental(event):
    library = Library(KBOT_TEMPLATE_DIR, users)
    library.fetch_status()
    library.do_filter(Filter(type=Filter.FILTER_NONE))
    short_message = library.get_message(type=Message.TYPE_SHORT)
    line.my_reply_text_message(short_message, event)

def __check_expire(event, xdays):
    library = Library(KBOT_TEMPLATE_DIR, users)
    library.fetch_status()
    library.do_filter(Filter(type=Filter.FILTER_EXPIRE, xdays=xdays))
    short_message = library.get_message(type=Message.TYPE_SHORT)
    line.my_reply_text_message(short_message, event)

def __check_expired(event):
    library = Library(KBOT_TEMPLATE_DIR, users)
    library.fetch_status()
    library.do_filter(Filter(type=Filter.FILTER_EXPIRED))
    short_message = library.get_message(type=Message.TYPE_SHORT)
    line.my_reply_text_message(short_message, event)

def __show_reply_string(event):
    message = KBOT.get_reply_string()
    line.my_reply_text_message(message, event)

def __check_reserved_books(event, user_nums):
    library     = Library(KBOT_TEMPLATE_DIR, users)
    user_status = library.check_reserved_books(user_nums)
    message     = UserStatus.make_user_reserved_books_message(KBOT_TEMPLATE_DIR, user_status)
    if event != None:
        line.my_reply_text_message(message, event)
    else:
        if UserStatus.prepared_reserved_book(user_status):
            line.my_push_text_message(message, line_tos)

def __search_book(event, query):
    rakuten        = RakutenBooks()
    books          = rakuten.search_books(query)

    if len(books) == 0:
        line.my_reply_text_message('見つかりませんでした。。', event)
    else:
        message = Book.get_books_select_line_carousel_mseeage(books)
        line.my_reply_template_message(message, event)

def __search_book_by_isbn(event, text):
    isbn = text[5:]
    # calilで検索
    book = calil.get_book(isbn)
    # amazonで検索
    # book.merge(amazon.get_book(isbn))
    book.merge(rakuten_books.get_book(isbn))
    # メッセージ作成
    message = Book.get_book_info_line_text_message(settings.PROJECT_ROOT, book)
    line.my_reply_text_message(message, event)

# @csrf_exempt
# def sample(request):
#
#     if request.method == 'POST':
#         Log.info('POST!!!!!!!!!!!!!')
#
#         try:
#             signature = request.META['HTTP_X_LINE_SIGNATURE']
#             body = request.body.decode('utf-8')
#             events = parser.parse(body, signature)
#
#             for event in events:
#
#                 if isinstance(event, MessageEvent):
#                     text = event.message.text
#
#                     if text == 'confirm':
#                         template = line.get_confirm_template_sample()
#                         line.my_reply_template_message(template, event)
#                     elif text == 'buttons':
#                         template = line.get_buttons_template_sample()
#                         line.my_reply_template_message(template, event)
#                     else:
#                         pass
#
#                 elif isinstance(event, PostbackEvent):
#                     data = event.postback.data
#
#                     if data == 'ping':
#                         line.my_reply_message('ping postback received!', event)
#                     else:
#                         line.my_reply_message(data, event)
#
#         except InvalidSignatureError as e:
#             Log.logging_exception(e)
#             return HttpResponseForbidden()
#         except LineBotApiError as e:
#             Log.logging_exception(e)
#             return HttpResponseBadRequest()
#         except Exception as e:
#             Log.logging_exception(e)
#
#         return HttpResponse()
#     else:
#         return HttpResponseBadRequest()

