from django.shortcuts import render
from django.http import HttpResponse

from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', {})


from django.http import JsonResponse
def tweet_detail_view(request, id):
    data = {
        "id": id
    }
    try:
        tweet = Tweet.objects.get(id=id)
        data['content'] = tweet.content
        status=200
    except:
        data['content'] = "Not Found"
        status=404

    return JsonResponse(data, status=status)

