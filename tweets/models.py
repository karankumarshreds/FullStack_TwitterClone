from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tweet(models.Model):
    #foreign key means many-to-one 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    
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

    