from django.conf.urls import url
from . import views

urlpatterns = [
    url("^youtube/omoide/", views.youtube_omoide),
    url("^youtube/recent/", views.youtube_recent),
    url("^gmail/check/", views.gmail_check),
    url("^library/check/", views.check_rental_state),
    url("^library/checkreserve/", views.check_reserve_state),
    url("^library/reserve/", views.library_reserve),
    url("^callback/", views.callback),
]
