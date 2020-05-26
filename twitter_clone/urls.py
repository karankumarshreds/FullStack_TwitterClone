from django.contrib import admin
from django.urls import path

from tweets.views import home_view, tweet_detail_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('tweets/<int:id>', tweet_detail_view, name="tweets"),
]

