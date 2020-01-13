from django.urls import path

from . import views
from .views import (TrackView)


app_name = 'track'

urlpatterns = [
    path('track/', views.TrackView, name='track')
]