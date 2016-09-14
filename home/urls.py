from django.conf.urls import url
from django.contrib.auth import views as auth_views
from home.views import *

urlpatterns = [
	url(r'^$', ulogin),
	url(r'^main/$', mainpg),  # URL for home page.
	url(r'^logout/$', logout_view), # URL for logout
	url(r'^users/$', get_users), # URL for adding friends
	url(r'^folusers/$', foll_users), # URL for getting all not following
	url(r'^api/(?P<tablename>\w{0,50})/$', user_api),
	url(r'^getweets/$',get_tweets), #self plus of those following
	url(r'^selftweets/$', self_tweets), #self only
	url(r'^main/(?P<userid>\d+)/$', userpg),
	url(r'^fe_tw/$',fe_tw),
	url(r'^stats/$',stats),
]
