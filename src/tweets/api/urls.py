from django.conf.urls import url
from django.views.generic import RedirectView

from .views import TweetListAPIView

urlpatterns = [
    url(r'^$', TweetListAPIView.as_view(), name='list'), #/api/tweet
]