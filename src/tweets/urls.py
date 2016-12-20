from django.conf.urls import url
from django.views.generic import RedirectView
from .views import (
    TweetDetailView,
    TweetDeleteView,
    TweetListView,
    TweetCreateView,
    TweetUpdateView,
    tweet_detail_view)

urlpatterns = [
    url(r'^search$', TweetListView.as_view(), name='list'), #/tweet/
    url(r'^$', RedirectView.as_view(url='/'), name='list'), #/tweet/
    #url(r'^(?P<pk>\d+)/$', tweet_detail_view, name='detail'), #/tweet/1/
    url(r'^create/$', TweetCreateView.as_view(), name='create'), #/tweet/1/
    url(r'^(?P<pk>\d+)/$', TweetDetailView.as_view(), name='detail'), #/tweet/1/
    url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(), name='update'), #/tweet/1/update/
    url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete'), #/tweet/1/delete/


]
