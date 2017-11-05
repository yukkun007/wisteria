from django.conf.urls import url
from . import views

urlpatterns = [
    url('^youtube/omoide/', views.youtube_omoide),
    url('^library/check/', views.library_check),
    url('^library/checkreserve/', views.library_check_reserve),
    url('^library/reserve/', views.library_reserve),
    url('^library/test/', views.library_test),
    url('^callback/', views.callback)
]
