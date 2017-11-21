# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os

from django.http import HttpResponse,\
    HttpResponseBadRequest,\
    HttpResponseRedirect,\
    HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from kbot.kbot import KBot
from kbot.line import Line
from kbot.library.library import Library
from kbot.library.user import User, Users
from kbot.library.rental_book import RentalBookFilter, RentalBookExpireFilter, RentalBookExpiredFilter
from kbot.library.reserved_book import ReservedBook, ReservedBookFilter, ReservedBookPreparedFilter
from kbot.log import Log
from kbot.google.gmail import GMail
from kbot.google.youtube import YouTube
from kbot.book.calil import CalilService
from kbot.book.rakuten_books import RakutenBooksService
from kbot.book.common import BookSearchQuery

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import ButtonsTemplate,\
    URITemplateAction,\
    MessageEvent,\
    PostbackEvent,\
    SourceGroup,\
    SourceUser\


# グローバル変数
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WISTERIA_DIR = os.path.join(BASE_DIR, 'wisteria')
KBOT = KBot(WISTERIA_DIR)
line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
parser = WebhookParser(os.environ['LINE_CHANNEL_SECRET'])
line = Line(line_bot_api)
gmail = GMail()
youtube = YouTube()
users = Users([User(os.environ['USER1']),
               User(os.environ['USER2']),
               User(os.environ['USER3']),
               User(os.environ['USER4'])])
gmail_tos = [os.environ['GMAIL_SEND_ADDRESS1'],
             os.environ['GMAIL_SEND_ADDRESS2']]
line_tos = [os.environ['LINE_SEND_GROUP_ID']]
if os.environ.get('PRODUCTION') != 'True':
    line_tos = [os.environ['LINE_SEND_GROUP_ID_DEBUG']]
# line_tos = [os.environ['LINE_SEND_ID']]


def library_check(request):
    if request.method == 'GET':
        __library_check()
        return HttpResponse('done! library_check')


def __library_check():
    Log.info('GET! library_check')

    xdays = 2
    library = Library(users)
    filter_setting = RentalBookExpireFilter(xdays=xdays)
    library.check_rental_books(filter_setting)
    if library.is_rental_books_exist():
        line.my_push_message(library.get_text_message(), line_tos)
        gmail.send_message_multi(
            gmail_tos,
            '図書館の本返却お願いします！',
            library.get_html_message())


def library_check_reserve(request):
    if request.method == 'GET':
        __library_check_reserve()
        return HttpResponse('done! library_check_reserve')


def __library_check_reserve():
    Log.info('GET! library_check_reserve')
    rental_filter = RentalBookFilter(users='all')
    reserved_filter = ReservedBookPreparedFilter(users='all')
    __check_rental_and_reserved_books(rental_filter, reserved_filter)


def library_reserve(request):
    if request.method == 'GET':
        book_id = request.GET.get('book_id')
        __library_reserve(book_id)
        return HttpResponse('done! library_reserve')


def __library_reserve(book_id):
    Log.info('GET! library_reserve')

    if book_id is not None:
        user_num = '0'
        library = Library(users)
        url = library.reserve(user_num, book_id)

        template = ReservedBook.make_finish_reserve_message_template(user_num)
        line.my_push_message(template, line_tos)

        return HttpResponseRedirect(url)
    else:
        line.my_push_message('予約失敗。。', line_tos)


def youtube_omoide(request):
    if request.method == 'GET':
        __youtube_omoide()
        return HttpResponse('done! youtube_omoide')
    else:
        return HttpResponseBadRequest()


def __youtube_omoide():
    Log.info('GET! youtube_omoide')

    movie = youtube.get_youtube_movie()
    Log.info(movie.to_string())

    buttons_template = ButtonsTemplate(
        title=movie.title,
        text='投稿日: ' + movie.published_at,
        thumbnail_image_url=movie.url,
        actions=[
            URITemplateAction(
                label='YouTubeへ',
                uri='https://www.youtube.com/watch?v=' + movie.video_id)
        ]
    )
    line.my_push_message(buttons_template, line_tos)


@csrf_exempt
def callback(request):

    if request.method == 'POST':
        Log.info('POST! callback')

        try:
            signature = request.META['HTTP_X_LINE_SIGNATURE']
            body = request.body.decode('utf-8')
            events = parser.parse(body, signature)

            for event in events:

                if isinstance(event, MessageEvent):
                    text = event.message.text

                    if isinstance(event.source, SourceUser):
                        Log.info('userId' + event.source.user_id)
                    if isinstance(event.source, SourceGroup):
                        Log.info('groupId' + event.source.group_id)

                    if KBOT.is_search_book_command(text):
                        __search_book(event, text)

                    elif KBOT.is_check_reserve_command(text):
                        filter_setting = ReservedBookFilter(users='all')
                        __check_reserved_books(event, filter_setting)

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
                        line.my_reply_message(template, event)

                elif isinstance(event, PostbackEvent):
                    data = event.postback.data
                    if data.startswith('isbn:'):
                        __search_book_by_isbn(event, data)
                    elif data.startswith('check_reserve:'):
                        user_nums = data[14:]
                        filter_setting = ReservedBookFilter(users=user_nums)
                        __check_reserved_books(event, filter_setting)
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
    library = Library(users)
    filter_setting = RentalBookFilter()
    library.check_rental_books(filter_setting)
    line.my_reply_message(library.get_text_message(), event)


def __check_expire(event, xdays):
    library = Library(users)
    filter_setting = RentalBookExpireFilter(xdays=xdays)
    library.check_rental_books(filter_setting)
    line.my_reply_message(library.get_text_message(), event)


def __check_expired(event):
    library = Library(users)
    filter_setting = RentalBookExpiredFilter()
    library.check_rental_books(filter_setting)
    line.my_reply_message(library.get_text_message(), event)


def __show_reply_string(event):
    message = KBOT.get_reply_string()
    line.my_reply_message(message, event)


def __check_reserved_books(event, filter_setting):
    library = Library(users)
    library.check_reserved_books(filter_setting)
    message = library.get_text_reserved_books_message()
    if event is not None:
        line.my_reply_message(message, event)
    else:
        if library.is_prepared_reserved_book():
            line.my_push_message(message, line_tos)


def __check_rental_and_reserved_books(rental_filter, reserved_filter):
    library = Library(users)
    library.check_rental_and_reserved_books(rental_filter, reserved_filter)
    users.filter(rental_filter.users)
    for user in users.list:
        message = library.get_text_rental_and_reserved_books_message(user)
        if library.is_prepared_reserved_book_at_one_user(user):
            line.my_push_message(message, line_tos)


def __search_book(event, text):
    query = BookSearchQuery.get_from(text)
    books = RakutenBooksService.search_books(query)
    message = books.slice(0, 5).get_books_select_line_carousel_mseeage()
    line.my_reply_message(message, event)


def __search_book_by_isbn(event, text):
    # calilで検索
    query = BookSearchQuery.get_from(text)
    calil_book = CalilService.get_one_book(query)
    # amazonで検索
    # book.merge(amazon.get_book(isbn))
    query = BookSearchQuery.get_from(text)
    rakuten_book = RakutenBooksService.get_one_book(query)
    # メッセージ作成
    message = rakuten_book.get_text_message() + calil_book.get_text_message()
    line.my_reply_message(message, event)
