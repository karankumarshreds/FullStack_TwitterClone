from django.db import models
from django.contrib.auth.models import User

## this table would have been made with ManyToMany field
## relation by default, but we want to add a 'timestamp' 
## field as well. Therefore, making this and passing in
## the other model's field using "through" attribute
class TweetLike(models.Model):
                            ## quotes since the Tweet model
                            ## is below this model
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# Create your models here.
class Tweet(models.Model):
    #foreign key means many-to-one 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    # to check who all liked this post, many users can like 
    # a single post therefore we are using manytomanyfield
    likes = models.ManyToManyField(User, related_name="tweet_user", blank=True, through=TweetLike)
    ## through :
    ## Django will automatically generate a table to manage many-to-many relationships. 
    # However, if you want to manually specify the intermediary table, you can use the 
    # through option to specify the Django model that represents the intermediate table 
    # that you want to use.


    class Meta: 
        #ordering in the reverse order of IDs 
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
        }
    def __str__(self):
        return self.content[0:10] + "..."


