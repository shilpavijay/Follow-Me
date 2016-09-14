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

def get_tweets(request):
	rel_tweets={}
	cur_user = request.user
	foll_list=base.objects.filter(username=cur_user,followers='NA') 
	usrtweets=tweet.objects.all()
	self_tweets=tweet.objects.filter(username=cur_user)

	for tw in usrtweets:
		if not foll_list:
			rel_tweets=self_tweets
		else:
			for fol in foll_list:
				if tw.username == fol.username or tw.username == cur_user:
					rel_tweets[tw.username]=tw.tweet_text
	return HttpResponse(serializers.serialize('json',rel_tweets))
	
def self_tweets(request):
	cur_user = request.user
	usrtweets=tweet.objects.filter(username=cur_user)
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

@csrf_exempt
def fe_tw(request):
	if request.method == 'POST':
		tw = tweet()
		tw.tweet_text = request.POST.get("tweetxt",False)
		tw.username = request.user
		tw.post_date = timezone.now()
		tw.save()
		return HttpResponse("pass")

@csrf_exempt
@login_required(login_url='/')
def get_users(request): 

	if request.method == 'POST' and request.is_ajax:
		rec=request.POST.get("selection",False)
		foll=User.objects.get(username=rec)
		#adding following to current user
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
	return render(request, 'users.html')

@csrf_exempt
@login_required(login_url='/')
def foll_users(request):
	users={}
	temp={}
	usernm = request.user.username
	cur_user = request.user
	foll_list=base.objects.filter(username=cur_user,followers='NA')  #get all followers of cur user
	for d in User.objects.all():    #get only those users whom current user doesnt follow. 
		if foll_list:
			for u in foll_list:
				if d.username != usernm and d.username != u.following: #Also omit self.
					temp[d] = d.username
		else:
			if d.username != usernm:
				temp[d] = d.username
	print temp
	return HttpResponse(serializers.serialize('json',temp))

@csrf_exempt
def logout_view(request):
	logout(request)
	if request.method == 'POST':
		return render(request,'login.html')
	return render(request,'logout.html')

@login_required
def userpg(request,userid):
	print userid
	return render(request,'userpg.html');	