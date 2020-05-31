from rest_framework import serializers
from .models import Tweet

MAX_TWEET_LENGTH = 150

class LikeActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    ## limiting the actions sent by the client
    ## we only need to check the value of 'action'
    def validate_action(self, value):
        ## in case client mistakenly asks for "LIke   "
        value = value.lower().strip()
        if not value in ["like", "unlike", "retweet"]:
            raise serializers.ValidationError("Invalid action request")
        return value
    

class TweetSerializer(serializers.ModelSerializer):
    # A read-only field that get its representation from calling a 
    # method on the parent serializer class. The method called will 
    # be of the form "get_{field_name}", and should take a single 
    # argument, which is the object being serialized.
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = Tweet 
        fields = ['id','content', 'likes']
    def get_likes(self, obj):
        # the value of likes will represent the number of likes
        return obj.likes.count()
    ## similar to how we validated in forms.py
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("The tweet is too long")
        return value