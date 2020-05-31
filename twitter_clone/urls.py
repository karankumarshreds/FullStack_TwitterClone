from django.contrib import admin
from django.urls import path

from tweets.views import (home_view,
    tweet_detail_view, 
    tweet_list_view,
    tweet_create_view,
    tweet_delete_view,
    tweet_action_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('tweets/', tweet_list_view, name="tweets"),
    path('tweets/<int:id>', tweet_detail_view, name="tweets"),
    path('create-tweet/', tweet_create_view, name="create-tweet"),
    path('delete-tweet/<int:id>', tweet_delete_view, name="delete-tweet"),
    path('tweet-action/', tweet_action_view, name="tweet-action")
]

