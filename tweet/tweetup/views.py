from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm,UserRegisterationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request,'index.html')


def tweet_list(request):
    tweets=Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})

#To create a tweet
@login_required
def tweet_create(request):
    if request.method=="POST":
        form=TweetForm(request.POST,request.FILES)
        if form.is_valid():
            #build in security
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm()
    return render(request,'tweet_form.html',{'form':form})

#To edit the tweet 
@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=
                            request.user)
    if request.method=='POST':
      form=TweetForm(request.POST,request.FILES,
       instance=tweet)
      if form.is_valid():
          tweet=form.save(commit=False)
          tweet.user=request.user
          tweet.save()
          return redirect('tweet_list')
    else:
        form=TweetForm(instance=tweet)    
    return render(request,'tweet_form.html',{'form':form}) 

@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=
                            request.user)
    if request.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})

def register(request):
    if request.method=="POST":
        form=UserRegisterationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            #this is the security check for the password ,this will take the data from the Form and check for the clened data
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')

    else:
        form=UserRegisterationForm()


    return render(request,'registration/register.html',{'form':form})


def tweet_search(request):
    query = request.GET.get('query', '')  # Get the search query from the request
    if query:
        # Filter tweets containing the search query in text
        tweets = Tweet.objects.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)
        )
    else:
        tweets = Tweet.objects.all()  # Return all tweets if no query
    
    return render(request, 'tweets/tweet_search.html', {'tweets': tweets, 'query': query})




    




