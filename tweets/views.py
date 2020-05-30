from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer

## REST FRAMEWORK ##
from rest_framework.response import Response
#only authenticated users are able to create, update and delete
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

#home
def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', {})

#create_view using serialiers
@api_view(['POST'])
@permission_classes([IsAuthenticated])  ##403 Forbidden
def tweet_create_view(request):
    serializer = TweetSerializer(data=request.POST)
    ##raise exception does what the we are manually
    ##doing in the last line ##error handling
    if serializer.is_valid(raise_exception=True):
        #we need the user field as it cannot be null
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


#list view using serializers
@api_view(['GET'])
def tweet_list_view(request):
    #getting all tweets 
    tweets = Tweet.objects.all()
    #changing all tweets to json
    serializer = TweetSerializer(tweets, many=True)
    ##serializer.data has all the fields mentioned
    ##in the serializers file
    data = {
            "response": serializer.data
        }
    return Response(data, status=200)


#detail view using serializer
@api_view(['GET'])
def tweet_detail_view(request, id):
    tweet = Tweet.objects.get(id=id)
    serializer = TweetSerializer(tweet)
    data = {
        "id": id,
        "content": serializer.data
    }
    return Response(data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, id):
    tweet = Tweet.objects.filter(id=id)
    if not tweet.exists():
        return Response({"error": "Tweet doesn't exist"}, status=404)
    print('#####################################################')
    print(tweet.get().user)
    print(request.user)
    if tweet.get().user != request.user:
        return Response({"error": "Not authorized"}, status=403)     
    tweet.get().delete()
    return Response({}, status=200)



#create_view without using serializers
##### NOT BEING USED #####
def tweet_create_view_(request):
    form = TweetForm(request.POST or None)
    #getting the data from the below input field
    #<input type="hidden" name="next" value="/"/>
    next_url = request.POST.get('next') or None
    if not request.user.is_authenticated: 
        return JsonResponse({}, status=401)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user 
        obj.save()
        #the way to check if the request is ajax 
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        elif next_url != None:
            return redirect(next_url)
        form = TweetForm()
    if form.errors: 
        return JsonResponse(form.errors, status=400)
    context = {
        'form': form
    }
    return render(request, 'components/form.html', context)

#list view without using serializers
##### NOT BEING USED #####
def tweet_list_view_(request):
    try:
        query_set = Tweet.objects.all()
        # tweet_list = [
        #     {"id": query.id, "content": query.content, "likes": 0} 
        #     for query in query_set
        # ]
        tweet_list = [
            query.serialize() for query in query_set
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
    

#detail view without using serializers 
##### NOT BEING USED #####
def tweet_detail_view_(request, id):
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

