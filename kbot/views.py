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
    PostbackEvent


# グローバル変数
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WISTERIA_DIR = os.path.join(BASE_DIR, 'wisteria')
KBOT = KBot(WISTERIA_DIR)
if os.environ.get('PRODUCTION') != 'True':
    line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN_DEBUG'])
    parser = WebhookParser(os.environ['LINE_CHANNEL_SECRET_DEBUG'])
    line_tos = [os.environ['LINE_SEND_GROUP_ID_DEBUG']]
else:
    line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
    parser = WebhookParser(os.environ['LINE_CHANNEL_SECRET'])
    line_tos = [os.environ['LINE_SEND_GROUP_ID']]
line = Line(line_bot_api)
gmail = GMail()
youtube = YouTube()
users = Users([User(os.environ['USER1']),
               User(os.environ['USER2']),
               User(os.environ['USER3']),
               User(os.environ['USER4'])])
gmail_tos = [os.environ['GMAIL_SEND_ADDRESS1'],
             os.environ['GMAIL_SEND_ADDRESS2']]


def library_check(request):
    if request.method == 'GET':
        __library_check()
        return HttpResponse('done! library_check')


def __library_check():
    Log.info('GET! library_check')

    xdays = '2'
    library = Library(users)
    filter_setting = RentalBookExpireFilter(xdays=xdays)
    target_users = library.check_rental_books(filter_setting)
    if target_users.is_rental_books_exist():
        line.my_push_message(target_users.get_rental_books_text_message(), line_tos)
        gmail.send_message_multi(
            gmail_tos,
            '図書館の本返却お願いします！',
            target_users.get_rental_books_html_message())


def library_check_reserve(request):
    if request.method == 'GET':
        __library_check_reserve()
        return HttpResponse('done! library_check_reserve')


def __library_check_reserve():
    Log.info('GET! library_check_reserve')
    rental_filter = RentalBookFilter(users='all')
    reserved_filter = ReservedBookPreparedFilter(users='all')
    __check_rental_and_reserved_books(None, rental_filter, reserved_filter)


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


def __get_rental_book_filter_of_user_specify(text):
    user_num = users.get_user_num(text)
    return RentalBookFilter(users=user_num)


def __get_rental_book_expire_filter(text):
    return RentalBookExpireFilter(xdays=text)


def __call_handler(event, handler_map):
    handler = handler_map.get('handler')
    filter = handler_map.get('filter')
    text = event.message.text
    if filter is not None:
        handler(event, filter(text))
    else:
        handler(event, text=text)


def __handle_text_event(event, handler_maps):
    # for debug
    #
    # if isinstance(event.source, SourceUser):
    #     Log.info('userId' + event.source.user_id)
    # if isinstance(event.source, SourceGroup):
    #     Log.info('groupId' + event.source.group_id)

    text = event.message.text
    maps = list(filter(lambda map: map['keyword'] in text, handler_maps))
    __call_handler(event, maps[0])

    # try:
    #     for handler_map in handler_maps:
    #         keywords = handler_map.get('keywords')
    #         for keyword in keywords:
    #             text = event.message.text
    #             if keyword in text:
    #                 __call_handler(event, handler_map)
    #                 return
    # except Exception as e:
    #     Log.logging_exception(e)

    # TODO:
    # elif KBOT.is_user_reserve_check_command(text):
    #     user_num = users.get_user_num(text)
    #     rental_filter = RentalBookFilter(users=user_num)
    #     reserved_filter = ReservedBookFilter(users=user_num)
    #     __check_rental_and_reserved_books(event, rental_filter, reserved_filter)


def __handle_postback_event(event):
    if not isinstance(event, PostbackEvent):
        return

    data = event.postback.data
    if data.startswith('isbn:'):
        __search_book_by_isbn(event, data)
    elif data.startswith('check_reserve:'):
        user_nums = data[14:]
        rental_filter = RentalBookFilter(users=user_nums)
        reserved_filter = ReservedBookPreparedFilter(users=user_nums)
        __check_rental_and_reserved_books(event, rental_filter, reserved_filter)


def __handle_events(events, handler_maps):
    for event in events:
        __handle_postback_event(event)
        __handle_text_event(event, handler_maps)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        Log.info('POST! callback')

        try:
            signature = request.META['HTTP_X_LINE_SIGNATURE']
            body = request.body.decode('utf-8')
            events = parser.parse(body, signature)

            __handle_events(events, _handler_maps)

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
        Log.info('bad request. request method is not POST')

        return HttpResponseBadRequest()


def __check_rental_books(event, filter_setting):
    library = Library(users)
    target_users = library.check_rental_books(filter_setting)
    line.my_reply_message(target_users.get_rental_books_text_message(), event)


def __check_reserved_books(event, filter_setting):
    library = Library(users)
    target_users = library.check_reserved_books(filter_setting)
    line.my_reply_message(target_users.get_reserved_books_text_message(), event)


def __reply_command_menu(event):
    template = KBOT.get_kbot_command_menu()
    line.my_reply_message(template, event)


def __reply_response_string(event):
    message = KBOT.get_reply_string()
    line.my_reply_message(message, event)


def __check_rental_and_reserved_books(event, rental_filter, reserved_filter):
    library = Library(users)
    target_users = library.check_rental_and_reserved_books(rental_filter, reserved_filter)
    for user in target_users.list:
        message = user.get_rental_and_reserved_books_message()
        if event is None:
            if user.is_prepared_reserved_book():
                line.my_push_message(message, line_tos)
        else:
            line.my_reply_message(message, event)


def __search_book(event, text=None):
    query = BookSearchQuery.get_from(text)
    books = RakutenBooksService.search_books(query)
    message = books.slice(0, 5).get_books_select_line_carousel_mseeage()
    line.my_reply_message(message, event)


def __search_library_book(event, text=None):
    query = BookSearchQuery.get_from(text)
    books = Library.search_books(query)
    message = books.slice(0, 50).get_message()
    line.my_reply_message(message, event)


def __search_book_by_isbn(event, text=None):
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


_handler_maps = [
    {'keyword': '図書？',
     'filter': __get_rental_book_filter_of_user_specify,
     'filter_param': True,
     'handler': __check_rental_books},
    {'keyword': '図書館',
     'filter': lambda: RentalBookFilter(users='all'),
     'handler': __check_rental_books},
    {'keyword': '日で延滞',
     'filter': __get_rental_book_expire_filter,
     'filter_param': True,
     'handler': __check_rental_books},
    {'keyword': '延滞',
     'filter': lambda: RentalBookExpiredFilter(),
     'handler': __check_rental_books},

    {'keyword': '予約',
     'filter': lambda: ReservedBookFilter(users='all'),
     'handler': __check_reserved_books},
    {'keyword': '予約？',
     'param': lambda: ReservedBookFilter(users='all'),
     'handler': __check_rental_and_reserved_books},

    {'keyword': '本？',
     'handler': __search_book},
    {'keyword': 'ほ？',
     'handler': __search_library_book},

    {'keyword': '文字',
     'handler': __reply_response_string},
    {'keyword': 'コマンド',
     'handler': __reply_command_menu},
]
