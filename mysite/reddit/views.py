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

from .models import Subreddit_Info, Reddit_Post, Twitter_Post, Saved_Post, Youtube_Post
from django.shortcuts import redirect

# Create your views here.

def index(request):
	return redirect('form')

def form(request):
    qs = Reddit_Post.objects.order_by('-pub_date')[:15]

    yt = Youtube_Post.objects.order_by('-id')[:15]
    
    tw = Twitter_Post.objects.order_by('-id')[:15]

    tw_list = []

    for elem in tw:
        tw_status = twitter.models.Status()
        tw_status.user = twitter.models.User()
        tw_status.urls = []
        tw_status.hashtags = []
        tw_status.user_mentions = []

        url_list = elem.urls.split()
        for (e_url, url) in zip(url_list[0::2], url_list[1::2]):
#             print("url: ", e_url, " | ", url)
            newUrl = twitter.models.Url()
            newUrl.expanded_url = e_url
            newUrl.url = url
            tw_status.urls.append(newUrl)


        for hash in elem.hash.split():
#             print(" >> ", hash)
            newHash = twitter.models.Hashtag()
            newHash.text = hash
            tw_status.hashtags.append(newHash)


        for mention in elem.mentions.split():
            newMention = twitter.models.User()
            newMention.screen_name = mention
            tw_status.user_mentions.append(newMention)


        tw_status.text = elem.message
        tw_status.user.name = elem.username
        tw_status.user.screen_name = elem.handle
        tw_status.created_at = elem.pub_date
        tw_status.user.profile_image_url = elem.icon

        tw_list.append(tw_status)


    return render(request, 'reddit/index.html', {'reddit' : qs, 'tweets' : tw_list, 'yt' : yt})


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

        qs = []
        notFound_flag = False

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
            except (prawcore.NotFound, prawcore.Redirect) as e:
                print("reddit exception")
                temp = Reddit_Post()
                temp.title = 'No "{}" subreddit was found'.format(sub_name)
                qs.append(temp)
                notFound_flag = True
                break

#                 qs = Reddit_Post.objects.order_by('-pub_date')
#                 return render(request, 'reddit/indexerr.html', {'reddit': qs, 'sub_name': sub_name})

        if (not notFound_flag):
            qs = Reddit_Post.objects.filter(subreddit=sub_name).order_by('-pub_date')

        print("reddit done")


        api = twitter.Api(consumer_key='RTFA7AJK32oqVqxNpePQ8ML7J',
                consumer_secret='aZy708i2jRW5K0QWujjVedMIVHepeT3ywYOogFC1sMRJNTHwTA',
                access_token_key='974079585171136512-CquWg1lGWu4nHQxSkOrSC3Rk8xeUAPS',
                access_token_secret='aXNhllvBHxqkESE7liT4qkwj4RQN2HnzTc1nIu9hzzXoC')

        results = api.GetSearch(raw_query="q={}%20&result_type=popular&lang=en&count=5".format(sub_name))


        print("twitter api done")







            # Twitter_Post fields:
            #   message
            #   username
            #   handle
            #   pub_date
            #   icon

        for message in results:
            all_urls = ''
            all_hash = ''
            all_mentions = ''
            for urls in message.urls:
                all_urls += urls.expanded_url
                all_urls += ' '
                all_urls += urls.url
                all_urls += ' '

#             print(message.hashtags)
            for hash in message.hashtags:
                all_hash += hash.text
                all_hash += ' '


            for mention in message.user_mentions:
                all_mentions += mention.screen_name
                all_mentions += ' '

            Twitter_Post.objects.get_or_create(searchQuery=sub_name, message=message.text, username=message.user.name, handle=message.user.screen_name, pub_date=message.created_at, icon=message.user.profile_image_url, urls=all_urls, hash=all_hash, mentions=all_mentions)



        if not results:
            tw_status = twitter.models.Status()
            tw_status.user = twitter.models.User()
            tw_status.urls = []
            tw_status.hashtags = []
            tw_status.user_mentions = []

            newUrl = twitter.models.Url()
            newUrl.expanded_url = ''
            newUrl.url = ''
            tw_status.urls.append(newUrl)


            newHash = twitter.models.Hashtag()
            newHash.text = ''
            tw_status.hashtags.append(newHash)


            newMention = twitter.models.User()
            newMention.screen_name = ''
            tw_status.user_mentions.append(newMention)


            tw_status.text = 'No "{}" results were found.'.format(sub_name)

            tw_status.created_at = datetime.datetime.now()
            tw_status.created_at = tw_status.created_at.strftime("%a %b %d %H:%M:%S +0000 %Y")

#             print(tw_status.created_at)



            results.append(tw_status)

            print("twitter no results")

#         print("results:", results)

####Youtube integration begin####


        YOUTUBE_API_SERVICE_NAME = 'youtube'
        YOUTUBE_API_VERSION = 'v3'

        r = requests.get("https://www.googleapis.com/youtube/v3/search?key=AIzaSyAUVFVHPo7dFJ53756t50YqrmVfPF5laKE&part=snippet&q={}".format(sub_name))
        data = json.loads(r.text)
#         print("-------------")
#         print(data)
#         print("-------------")
        for i in range(0,5):
            if 'videoId' in (data['items'][i]['id']):
                print((data['items'][i]['id']['videoId']))
                videoid= (data['items'][i]['id']['videoId'])
                Youtube_Post.objects.get_or_create(ytid=videoid, searchQuery=sub_name)
#             else:
#                 print((data['items'][i]['id']))

        yt = Youtube_Post.objects.filter(searchQuery=sub_name)

###End Youtube integration####



        return render(request, 'reddit/results.html', {'reddit': qs, 'title': sub_name, 'tweets' : results, 'youtube_results': yt})
        #return HttpResponse(titles)#subreddit.display_name + subreddit.title + subreddit.description)

    else:
        return render(request, 'reddit/index.html')



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
