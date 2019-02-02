# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import urllib

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import redirect

from kbot.kbot import KBot
from kbot.line import Line
from kbot.library.library import Library
from kbot.library.user import User, Users
from kbot.library.rental_book_filter import (
    RentalBookFilter,
    RentalBookExpireFilter,
    RentalBookExpiredFilter
)
from kbot.library.reserved_book import ReservedBookFilter, ReservedBookPreparedFilter
from kbot.log import Log
from kbot.google.gmail import GMail
from kbot.google.youtube import YouTube
from kbot.google.movie import Movie
from kbot.book.calil import CalilService
from kbot.book.rakuten_books import RakutenBooksService
from kbot.book.common import BookSearchQueryFactory

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import ButtonsTemplate, URITemplateAction, PostbackEvent


# グローバル変数
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WISTERIA_DIR = os.path.join(BASE_DIR, "wisteria")
KBOT = KBot(WISTERIA_DIR)
if os.environ.get("PRODUCTION") != "True":
    line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN_DEBUG"])
    parser = WebhookParser(os.environ["LINE_CHANNEL_SECRET_DEBUG"])
    line_tos = [os.environ["LINE_SEND_GROUP_ID_DEBUG"]]
else:
    line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
    parser = WebhookParser(os.environ["LINE_CHANNEL_SECRET"])
    line_tos = [os.environ["LINE_SEND_GROUP_ID"]]
line = Line(line_bot_api)
gmail = GMail()
users = Users(
    [
        User(os.environ["USER1"]),
        User(os.environ["USER2"]),
        User(os.environ["USER3"]),
        User(os.environ["USER4"]),
    ]
)
gmail_tos = [os.environ["GMAIL_SEND_ADDRESS1"], os.environ["GMAIL_SEND_ADDRESS2"]]


def check_rental_state(request):
    try:
        if request.method == "GET":
            user_id = request.GET.get("user")
            __check_rental_state(user_id)
            return HttpResponse("done! check_rental_status")
    except Exception as e:
        Log.info("library_check_rental_state: failed.")
        Log.logging_exception(e)


def __check_rental_state(user_id: str):
    Log.info("GET! library_check")

    xdays = "2"
    library = Library(users)
    config = RentalBookExpireFilter(xdays=xdays, users=user_id)
    target_users = library.check_books(config)
    if target_users.is_rental_books_exist():
        line.my_push_message(
            target_users.get_check_books_text_message(config.books_class_name), line_tos
        )
        gmail.send_message_multi(
            gmail_tos,
            "図書館の本返却お願いします！",
            target_users.get_check_books_html_message(config.books_class_name),
        )


def check_reserve_state(request):
    try:
        if request.method == "GET":
            user_id = request.GET.get("user")
            __check_reserve_state(user_id)
            return HttpResponse("done! check_reserve_status")
    except Exception as e:
        Log.info("library_check_reserve: failed.")
        Log.logging_exception(e)


def __check_reserve_state(user_id: str):
    Log.info("GET! library_check_reserve")
    rental_filter = RentalBookFilter(users=user_id)
    reserved_filter = ReservedBookPreparedFilter(users=user_id)
    __check_rental_and_reserved_books(None, rental_filter, reserved_filter)


def gmail_check(request):
    try:
        if request.method == "GET":
            query = "from:info@keishicho.metro.tokyo.jp is:unread"
            _gmail_check(query)
            return HttpResponse("done! gmail_check")
        else:
            return HttpResponseBadRequest()
    except Exception as e:
        Log.info("gmail_check: failed.")
        Log.logging_exception(e)


def _gmail_check(query):
    Log.info("GET! gmail_check")

    messages = gmail.get_messages(query)
    for message in messages:
        line.my_push_message(message, line_tos)


def youtube_omoide(request):
    try:
        if request.method == "GET":
            __youtube_omoide()
            return HttpResponse("done! youtube_omoide")
        else:
            return HttpResponseBadRequest()
    except Exception as e:
        Log.info("youtube_omoide: failed.")
        Log.logging_exception(e)


def __send_youtube_movie_message(movie: Movie, description: str) -> None:
    Log.info(movie.to_string())

    buttons_template = ButtonsTemplate(
        title=movie.title,
        text=description,
        thumbnail_image_url=movie.url,
        actions=[
            URITemplateAction(
                label="YouTubeへ", uri="https://www.youtube.com/watch?v=" + movie.video_id
            )
        ],
    )
    line.my_push_message(buttons_template, line_tos)


def __youtube_omoide():
    Log.info("GET! youtube_omoide")

    description = ""
    youtube = YouTube()
    movie = youtube.get_youtube_movie_match_today()
    if movie is None:
        youtube = YouTube()
        movie = youtube.get_youtube_movie()
        description = "投稿日: " + movie.published_at
    else:
        description = "★　 " + str(movie.past_years) + " 年前の今日　★"

    __send_youtube_movie_message(movie, description)


def youtube_recent(request):
    try:
        if request.method == "GET":
            _youtube_recent()
            return HttpResponse("done! youtube_recent")
        else:
            return HttpResponseBadRequest()
    except Exception as e:
        Log.info("youtube_recent: failed.")
        Log.logging_exception(e)


def _youtube_recent():
    Log.info("GET! youtube_recent")

    youtube = YouTube()
    movies = youtube.get_youtube_movies_recent()
    Log.info("youtube_recent: len of movie=" + str(len(movies)))
    for movie in movies:
        if movie is None:
            # 何もしない
            Log.info("youtube_recent: movie is none.")
            pass
        else:
            description = "投稿日: " + movie.published_at
            __send_youtube_movie_message(movie, description)


def __get_reserved_book_filter_of_user_specify(text):
    user_num = users.get_user_num(text)
    return ReservedBookFilter(users=user_num)


def __get_rental_book_filter_of_user_specify(text):
    user_num = users.get_user_num(text)
    return RentalBookFilter(users=user_num)


def __get_rental_book_expire_filter(text):
    return RentalBookExpireFilter(xdays=text)


def __call_handler(event, handler_map):
    handler = handler_map.get("handler")
    filter = handler_map.get("filter")
    filter2 = handler_map.get("filter2")
    text = event.message.text
    if filter is None:
        handler(event, text=text)
    elif filter is not None and filter2 is not None:
        handler(event, filter(text), filter2(text))
    else:
        handler(event, filter(text))


def __handle_text_event(event, handler_maps):
    # for debug
    #
    # if isinstance(event.source, SourceUser):
    #     Log.info('userId' + event.source.user_id)
    # if isinstance(event.source, SourceGroup):
    #     Log.info('groupId' + event.source.group_id)

    text = event.message.text
    maps = list(filter(lambda map: map["keyword"] in text, handler_maps))
    if len(maps) > 0:
        __call_handler(event, maps[0])


def __handle_postback_event(event):
    if not isinstance(event, PostbackEvent):
        return

    data = event.postback.data
    if data.startswith("isbn:"):
        __search_book_by_isbn(event, data)
    elif data.startswith("check_reserve:"):
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
    if request.method != "POST":
        Log.info("bad request. request method is not POST")
        return HttpResponseBadRequest()

    Log.info("POST! callback")
    events = None
    try:
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        events = parser.parse(body, signature)

        __handle_events(events, _handler_maps)

    except InvalidSignatureError as e:
        Log.logging_exception(e)
        __reply_line_error_message(events)
        return HttpResponseForbidden()
    except LineBotApiError as e:
        Log.logging_exception(e)
        __reply_line_error_message(events)
        return HttpResponseBadRequest()
    except Exception as e:
        Log.logging_exception(e)
        __reply_line_error_message(events)

    return HttpResponse("done! callback")


def __reply_line_error_message(events):
    if events is not None:
        for event in events:
            line.my_reply_message("エラー発生。。すみません、もう一度送ってください。", event)


def __check_books(event, config):
    library = Library(users)
    target_users = library.check_books(config)
    line.my_reply_message(target_users.get_check_books_text_message(config.books_class_name), event)


def __reply_command_menu(event, text=None):
    template = KBOT.get_kbot_command_menu()
    line.my_reply_message(template, event)


def __reply_response_string(event, text=None):
    message = KBOT.get_reply_string()
    line.my_reply_message(message, event)


def __check_rental_and_reserved_books(event, rental_filter, reserved_filter):
    library = Library(users)
    target_users = library.check_rental_and_reserved_books(rental_filter, reserved_filter)
    for user in target_users.list:
        message = user.get_rental_and_reserved_books_message()
        __send_line_message(event, message, user.is_prepared_reserved_book())


def __send_line_message(event, message, is_push):
    if event is None:
        if is_push:
            line.my_push_message(message, line_tos)
    else:
        line.my_reply_message(message, event)


def __search_book(event, search_class, max_count, text=None):
    query = BookSearchQueryFactory.create(text)
    books = search_class.search_books(query)
    books.slice(0, max_count)
    message = books.get_message()
    line.my_reply_message(message, event)


def __search_rakuten_book(event, text=None):
    __search_book(event, RakutenBooksService, 5, text)


LIBRALY_SEARCH_URL = (
    "https://www.lib.nerima.tokyo.jp/opw/OPW/OPWSRCHLIST.CSP?"
    "DB=LIB&FLG=SEARCH&LOCAL%28%22LIB%22%2c%22SK41%22%2c1%29=on&MODE=1&"
    "PID2=OPWSRCH2&SORT=-3&opr%281%29=OR&qual%281%29={0}&WRTCOUNT=100&text%281%29="
)


def __search_library_book_title(event, text=None):
    query = BookSearchQueryFactory.create(text)
    url = LIBRALY_SEARCH_URL.format("MZTI") + urllib.parse.quote(query.get("title"))
    message = "URLをクリック: " + url
    line.my_reply_message(message, event)


def __search_library_book_author(event, text=None):
    query = BookSearchQueryFactory.create(text)
    url = LIBRALY_SEARCH_URL.format("MZAU") + urllib.parse.quote(query.get("author"))
    message = "URLをクリック: " + url
    line.my_reply_message(message, event)


def __search_book_by_isbn(event, text=None):
    # 楽天ブックスで検索
    query = BookSearchQueryFactory.create(text)
    rakuten_book = RakutenBooksService.get_one_book(query)
    # calilで検索
    query = BookSearchQueryFactory.create(text)
    calil_book = CalilService.get_one_book(query)
    # メッセージ作成
    message = rakuten_book.get_text_message() + calil_book.get_text_message()
    line.my_reply_message(message, event)


_handler_maps = [
    {
        "keyword": "図書？",
        "filter": __get_rental_book_filter_of_user_specify,
        "handler": __check_books,
    },
    {
        "keyword": "図書館",
        "filter": lambda text: RentalBookFilter(users="all"),
        "handler": __check_books,
    },
    {"keyword": "日で延滞", "filter": __get_rental_book_expire_filter, "handler": __check_books},
    {"keyword": "延滞", "filter": lambda text: RentalBookExpiredFilter(), "handler": __check_books},
    {
        "keyword": "予約？",
        "filter": __get_rental_book_filter_of_user_specify,
        "filter2": __get_reserved_book_filter_of_user_specify,
        "handler": __check_rental_and_reserved_books,
    },
    {
        "keyword": "予約",
        "filter": lambda text: ReservedBookFilter(users="all"),
        "handler": __check_books,
    },
    {"keyword": "ほ？", "handler": __search_rakuten_book},
    {"keyword": "本？", "handler": __search_library_book_title},
    {"keyword": "著？", "handler": __search_library_book_author},
    {"keyword": "文字", "handler": __reply_response_string},
    {"keyword": "コマンド", "handler": __reply_command_menu},
]
