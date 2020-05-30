from rest_framework import serializers
from .models import Tweet

MAX_TWEET_LENGTH = 150

class TweetSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tweet 
        fields = ['id','content', 'likes']
    ## similar to how we validated in forms.py
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("The tweet is too long")
        return value