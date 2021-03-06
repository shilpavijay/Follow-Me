from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.template.context_processors import csrf
from .models import tweet, User, base
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict,OrderedDict
import operator
import json


@csrf_exempt
def ulogin(request):
	if request.method == 'POST' and request.is_ajax:
		usernm = request.POST.get("username",False)
		pswd = request.POST.get("password",False)
		auth = authenticate(username=usernm,password=pswd)
		if auth is not None:
			print("User is valid and authenticated")
			login(request,auth)
			print("login done returning...")
			return HttpResponse("pass")
		else:
			logout(request)
			print("Wrong username or password entered. Please check.")
	return render(request,'login.html')	

@csrf_exempt
@login_required(login_url='/')
def mainpg(request): 
	return render(request, 'mainpg.html')

	
def user_api(request,tablename):
	tabledata = eval(tablename).objects.all()
	return HttpResponse(
		serializers.serialize('json',tabledata))

class OrderedDefaultDict(OrderedDict):
    def __init__(self, default_factory=None, *args, **kwargs):
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        val = self[key] = self.default_factory()
        return val


def get_tweets(request):
	rel_tweets=OrderedDefaultDict(OrderedDict)
	cur_user = request.user
	foll_list=base.objects.filter(username=cur_user,followers='NA') 
	usrtweets=tweet.objects.order_by('-post_date')
	self_tweets=tweet.objects.filter(username=cur_user).order_by('-post_date')

	for tw in self_tweets:
		rel_tweets[tw.post_date.strftime('%Y-%m-%d %H:%M:%S')].update({tw.tweet_text:cur_user.username})
	else:
		if foll_list:
			for fol in foll_list:		
				user = User.objects.filter(username=fol.following)		
				if tweet.objects.filter(username=user):
					for tw in tweet.objects.filter(username=user).order_by('-post_date'):		
						nm = tw.username.username				
						rel_tweets[tw.post_date.strftime('%Y-%m-%d %H:%M:%S')].update({tw.tweet_text:nm})
	rel_tweets=sorted(rel_tweets.items(),reverse=True)
	return HttpResponse(json.dumps(OrderedDict(rel_tweets)))


def self_tweets(request):
	cur_user = request.user
	usrtweets=tweet.objects.filter(username=cur_user).order_by('-post_date')
	return HttpResponse(serializers.serialize('json',usrtweets))

def usersptweets(request,username):
	u = username
	cur_user = User.objects.get(username=u)
	usrtweets=tweet.objects.filter(username=cur_user).order_by('-post_date')
	return HttpResponse(serializers.serialize('json',usrtweets))

def stats(request):
	resp_data={}
	cur_user = request.user
	count = tweet.objects.filter(username=cur_user).count()
	follwing=base.objects.filter(username=cur_user,followers='NA').count()
	follwers=base.objects.filter(username=cur_user,following='NA').count()
	resp_data['count']=int(count)
	resp_data['following']=int(follwing)
	resp_data['followers']=int(follwers)
	return HttpResponse(json.dumps(resp_data))

def userspstats(request,username):
	u = username
	resp_data={}
	cur_user = User.objects.get(username=u)
	count = tweet.objects.filter(username=cur_user).count()
	follwing=base.objects.filter(username=cur_user,followers='NA').count()
	follwers=base.objects.filter(username=cur_user,following='NA').count()
	resp_data['count']=int(count)
	resp_data['following']=int(follwing)
	resp_data['followers']=int(follwers)
	return HttpResponse(json.dumps(resp_data))

def following(request,username):
	u=username
	cur_user = User.objects.get(username=u)
	fing = base.objects.filter(username=cur_user,followers='NA')
	return HttpResponse(serializers.serialize('json',fing))

def followers(request,username):
	u=username
	cur_user = User.objects.get(username=u)
	fers=base.objects.filter(username=cur_user,following='NA')
	return HttpResponse(serializers.serialize('json',fers))

def fol(request,username):
	return render(request,'foll.html')

@csrf_exempt
def fe_tw(request):
	if request.method == 'POST':
		tw = tweet()
		tw.tweet_text = request.POST.get("tweetxt",False)
		tw.username = request.user
		tw.post_date = timezone.now()
		tw.save()
		print tw.tweet_text
		print 'done'
		return HttpResponse("pass")

@csrf_exempt
@login_required(login_url='/')
def get_users(request): 
	print "in get users"
	if request.method == 'POST' and request.is_ajax:
		rec=request.POST.get("selection",False)
		print rec
		foll=User.objects.get(username=rec)
		#adding following to current user
		print foll
		b = base()
		b.username = request.user
		b.following = foll
		b.followers = 'NA'
		b.save() 
		#adding follower to user clicked on
		b=base()
		b.username = foll
		b.following = 'NA'
		b.followers = request.user.username
		b.save()
		print "done"
	return render("pass")

@csrf_exempt
@login_required(login_url='/')
def foll_users(request):
	users={}
	temp=[]
	usernm = request.user.username
	cur_user = request.user
	foll_list=base.objects.filter(username=cur_user,followers='NA').order_by('following')  #get all followers of cur user
	for each in foll_list:
		a = each.following
		temp.append(a)
	if not foll_list:	
		for username in User.objects.all(): 
			if username !=cur_user:
				users[username.username] = username.username
	else:
		for u in User.objects.all():
			if u.username not in temp and u.username != usernm: #Also omit self.and username != usernm
				users[u.username] = u.username	
	return HttpResponse(json.dumps(users.keys()))

def userspfol(request,username):
	u=username
	uobj=User.objects.get(username=u)
	users={}
	temp=[]
	usernm = uobj.username
	cur_user = uobj
	foll_list=base.objects.filter(username=cur_user,followers='NA').order_by('following')  #get all followers of cur user
	for each in foll_list:
		a = each.following
		temp.append(a)
	if not foll_list:	
		for u in User.objects.all(): 
			if u != cur_user:
				users[u.username] = u.username
	else:
		for u in User.objects.all():
			if u.username not in temp and u.username != usernm: #Also omit self.and username != usernm
				users[u.username] = u.username	
	return HttpResponse(json.dumps(users.keys()))


@csrf_exempt
def logout_view(request):
	logout(request)
	if request.method == 'POST':
		return render(request,'login.html')
	return render(request,'logout.html')

@login_required
def userpg(request,username):
	print username
	return render(request,'userpg.html');	
