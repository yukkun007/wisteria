from django.conf.urls import include, url
from . import views

urlpatterns = [
  #url('^callback/', views.callback),
  url('^youtube/omoide/', views.youtube_omoide),
  url('^library/check/', views.library_check),
  url('^library/test/', views.library_test),
  url('^callback/', views.callback)
]

