"""
URLsconf for the :mod:`question` project
"""

from django.conf.urls import patterns, url, include

from questions.views import Home
from questions.views import QuestionList
from questions.views import QuestionDetail
from questions.views import AnswerList
from questions.views import AnswerDetail
from questions.views import AnswerQuestion

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^q/$', QuestionList.as_view(), name='question-list'),
    url(r'^q/(?P<pk>\d+)/$', QuestionDetail.as_view(), name='question-detail'),
    url(r'^a/$', AnswerList.as_view(), name='answer-list'),
    url(r'^a/d/(?P<pk>\d+)/$', AnswerDetail.as_view(), name='answer-detail'),
    url(r'^a/(?P<pk>\d+)/$', AnswerQuestion.as_view(), name='answer-question'),
)

from questions.views import ProfileList, ProfileEditView, ProfileView

urlpatterns += patterns(
    '',
    url(r'^p/$', ProfileEditView.as_view(), name='profile-edit'),
    url(r'^p/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile-view'),
    url(r'^u/$', ProfileList.as_view(), name='profile-list'),
)

from questions.views import CategoryList, CategoryDetail
""" URLpattern to list categories and see contained quesitons.  """

urlpatterns += patterns(
    '',
    url(r'^c/$', CategoryList.as_view(), name='category-list'),
    url(r'^c/(?P<pk>\d+)/$', CategoryDetail.as_view(), name='category-detail'),
)

from questions.views import Submit
""" Urlpatterns required to submit new questions.  """

urlpatterns += patterns(
    '',
    url(r'^s/$', Submit.as_view(), name='submit'),
)

from questions.views import Compare
""" URLpattern to compare and match user(profiles) """

urlpatterns += patterns(
    '',
    url(r'^compare/(?P<pk>\d+)/$', Compare.as_view(), name='compare'),
)

from rest_framework import routers
from questions.views import QuestionViewSet
from questions.views import CategoryViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'question', QuestionViewSet, base_name="api-question")
router.register(r'category', CategoryViewSet, base_name="api-category")

urlpatterns += patterns(
    '',
    url(r'^api/', include(router.urls)),
)
