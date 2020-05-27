from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Tweet
from .forms import TweetForm

#home
def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', {})

#create_view
def tweet_create_view(request):
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        #to make it empty afer saving
        form = TweetForm()
    context = {
        'form': form
    }
    return render(request, 'components/form.html', context)



#list view
def tweet_list_view(request):
    try:
        query_set = Tweet.objects.all()
        tweet_list = [
            {"id": query.id, "content": query.content, "likes": 0} 
            for query in query_set
        ]
        print(tweet_list)
        data = {
            "response": tweet_list
        }
        status = 200
    except:
        data = {
            "response": 'Not Found'
        }
        status = 404
    return JsonResponse(data, status=status)
    

#detail view
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

