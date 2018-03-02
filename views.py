from django.shortcuts import get_object_or_404, render

from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse

import requests
import praw
import datetime


from .models import Subreddit_Info, Reddit_Post

# Create your views here.

def index(request):
    return HttpResponse("This is the reddit index.")

def form(request):
    return render(request, 'reddit/index.html')
    #return render(request, 'reddit/form.html')

def search(request):

    if request.method == 'POST':
        sub_name = request.POST.get('sub_name', None)


        reddit = praw.Reddit(client_id='wJFgeD5oMtXKAQ',
                      client_secret='PSdJeUpG_tZNtolnIB9lVWYnG58',
                      username='RemarkableSituation',
                      password='2018@pp',
                      user_agent='PRAW Tester v0.1')
                      
        #print(reddit.read_only)
        #return HttpResponse(reddit.read_only)
                      
                      
        # assume you have a Reddit instance bound to variable `reddit`
        subreddit = reddit.subreddit(sub_name)#('redditdev')
    
    #     print(subreddit.display_name)   # Output: redditdev
    #     print(subreddit.title)          # Output: reddit Development
    #     print(subreddit.description)    # Output: A subreddit for discussion of ...
    
        titles = "<b>" + subreddit.display_name + "</b><br/><br/>"
        i = 1
        limits = 5
        limitMax = 5
        lFlag = True
        while lFlag: 
        
            
            print("start: ", limits)
            
            limVal = limits + limitMax
            limits = limitMax
             
            for submission in reddit.subreddit(sub_name).hot(limit = limVal ):
                
            
                print("loop: ", limits)
                if limits == 0:
                    lFlag = False
                    break
                if submission.stickied is False:
                    time = datetime.datetime.fromtimestamp(submission.created)
#             titles = titles + str(i) + ". " + submission.title + "<br/>&emsp;&emsp;" + str(time) + "<br/>" #print(submission.title)
#             i = i + 1

                # this avoids integrity errors from unique constraints
            
                    Reddit_Post.objects.get_or_create(subreddit=sub_name,title=submission.title,pub_date=time)
                    limits -= 1
                    print ("Limits in if", limits)
                  
#             red_post = Reddit_Post()
#             red_post.subreddit = sub_name
#             red_post.title = submission.title
#             red_post.pub_date = time
#             red_post.save()
            if limits == 0:
                break
            
        qs = Reddit_Post.objects.filter(subreddit=sub_name).order_by('-pub_date')
         
   
        return render(request, 'reddit/results.html', {'reddit': qs, 'title': sub_name})
        #return HttpResponse(titles)#subreddit.display_name + subreddit.title + subreddit.description)
        
    else:
        return render(request, 'reddit/index.html')
    
        
        
        
        
        
        
        
        
        
        

        
# the below only shows up if a user goes to /reddit/<subreddit> on
#   the test server. It's currently disabled because I've removed
#   the client information from the praw.Reddit() call.

# This should basically not see any actual use, and is left at the
#   moment purely for reference.
        
def reddit_test(request, sub_name):

    reddit = praw.Reddit(client_id='INSERT_CLIENT_ID',
                  client_secret='INSERT_CLIENT_SECRET',
                  username='INSER_USERNAME',
                  password='INSERT_PASSWORD',
                  user_agent='PRAW Tester v0.1')
                  
    #print(reddit.read_only)
    #return HttpResponse(reddit.read_only)
                  
                  
    # assume you have a Reddit instance bound to variable `reddit`
    subreddit = reddit.subreddit(sub_name)#('redditdev')

#     print(subreddit.display_name)   # Output: redditdev
#     print(subreddit.title)          # Output: reddit Development
#     print(subreddit.description)    # Output: A subreddit for discussion of ...

    return HttpResponse(subreddit.display_name + subreddit.title + subreddit.description)





