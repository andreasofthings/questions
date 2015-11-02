from __future__ import absolute_import

from .compat import patterns, include, url


urlpatterns = patterns(
    ''
    url('^$', include('questions.urls')),
)
