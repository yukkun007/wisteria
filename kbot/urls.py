from django.conf.urls import url
from . import views

urlpatterns = [
    url('^youtube/omoide/', views.youtube_omoide),
    url('^library/check/', views.check_rental_state),
    url('^library/checkreserve/', views.check_reserve_state),
    url('^library/reserve/', views.library_reserve),
    url('^callback/', views.callback)
]
