from django.shortcuts import get_object_or_404, render

from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse

import requests
import praw
import prawcore
import datetime
import twitter
import json
import time
# from datetime import *

from .models import Subreddit_Info, Reddit_Post, Twitter_Post, Saved_Post
from django.shortcuts import redirect

# Create your views here.

def index(request):
	return redirect('form')

def form(request):
    qs = Reddit_Post.objects.order_by('-pub_date')
    
    tw = Twitter_Post.objects.order_by('-id')
    
    tw_list = []
    
    for elem in tw:
        tw_status = twitter.models.Status()
        tw_status.text = elem.message
        tw_status.user = twitter.models.User
        tw_status.user.name = elem.username
        tw_status.user.screen_name = elem.handle
        tw_status.created_at = elem.pub_date
        tw_status.user.profile_image_url = elem.icon
        
        tw_list.append(tw_status)
    
    
    
    return render(request, 'reddit/index.html', {'reddit' : qs, 'tweets' : tw_list})
    #return render(request, 'reddit/form.html')

    
    
    
    
    
    
    
    
    
    
    
def youtube(request):
    return render(request, 'reddit/results.html')
    
# def twitter(request):
#     api = twitter.Api(consumer_key='RTFA7AJK32oqVqxNpePQ8ML7J',
#                   consumer_secret='aZy708i2jRW5K0QWujjVedMIVHepeT3ywYOogFC1sMRJNTHwTA',
#                   access_token_key='974079585171136512-CquWg1lGWu4nHQxSkOrSC3Rk8xeUAPS',
#                   access_token_secret='aXNhllvBHxqkESE7liT4qkwj4RQN2HnzTc1nIu9hzzXoC')
#     results = api.GetSearch(raw_query="q=twitter%20&result_type=recent&since=2014-07-19&count=100")
#     print (results)
#     return render(request, 'reddit/results.html', {'twitter_results' : results})

def archives(request):


    # return render(request, 'reddit/archives.html')
    subname_list = set()
    for sub in Reddit_Post.objects.all():
        sub_name = sub.subreddit
        subname_list.add(sub_name)
    qs = Reddit_Post.objects.order_by('-pub_date')
   
    return render(request, 'reddit/archives.html', {'set': subname_list, 'reddit': qs})

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
        
            
#             print("start: ", limits)
            
            limVal = limits + limitMax
            limits = limitMax
             
            try:
	            for submission in reddit.subreddit(sub_name).hot(limit = limVal ):
	                
	            
# 	                print("loop: ", limits)
	                if limits == 0:
	                    lFlag = False
	                    break
	                if submission.stickied is False:
	                    time = datetime.datetime.fromtimestamp(submission.created)
	#             titles = titles + str(i) + ". " + submission.title + "<br/>&emsp;&emsp;" + str(time) + "<br/>" #print(submission.title)
	#             i = i + 1
	
	                # this avoids integrity errors from unique constraints
	            
	                    Reddit_Post.objects.get_or_create(subreddit=sub_name,title=submission.title,pub_date=time, link=submission.url)
	                    limits -= 1
# 	                    print ("Limits in if", limits)
	                  
	#             red_post = Reddit_Post()
	#             red_post.subreddit = sub_name
	#             red_post.title = submission.title
	#             red_post.pub_date = time
	#             red_post.save()
	            if limits == 0:
	                break
            except prawcore.NotFound:
                qs = Reddit_Post.objects.order_by('-pub_date')
                return render(request, 'reddit/indexerr.html', {'reddit': qs, 'sub_name': sub_name})
#                 return redirect('form')
            
        qs = Reddit_Post.objects.filter(subreddit=sub_name).order_by('-pub_date')

        api = twitter.Api(consumer_key='RTFA7AJK32oqVqxNpePQ8ML7J',
                consumer_secret='aZy708i2jRW5K0QWujjVedMIVHepeT3ywYOogFC1sMRJNTHwTA',
                access_token_key='974079585171136512-CquWg1lGWu4nHQxSkOrSC3Rk8xeUAPS',
                access_token_secret='aXNhllvBHxqkESE7liT4qkwj4RQN2HnzTc1nIu9hzzXoC')
        
        results = api.GetSearch(raw_query="q={}%20&result_type=popular&lang=en&count=5".format(sub_name))
        
            # there is an error displaying twitter user icons on some
            #   browsers/setups for some reason. Shows up as a broken
            #   image link, even though the link itself is correct.
#         for user_result in results:
#             print(user_result.user.profile_image_url)



            # Twitter_Post fields:
            #   message
            #   username
            #   handle
            #   pub_date
            #   icon

        for message in results:
            Twitter_Post.objects.get_or_create(message=message.text, username=message.user.name, handle=message.user.screen_name, pub_date=message.created_at, icon=message.user.profile_image_url)


        YOUTUBE_API_SERVICE_NAME = 'youtube'
        YOUTUBE_API_VERSION = 'v3'

        r = requests.get("https://www.googleapis.com/youtube/v3/videos?key=AIzaSyAUVFVHPo7dFJ53756t50YqrmVfPF5laKE&part=snippet&chart=mostPopular&regionCode=US")
        data = json.loads(r.text)

   
        return render(request, 'reddit/results.html', {'reddit': qs, 'title': sub_name, 'tweets' : results, 'youtube_results': data})
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





