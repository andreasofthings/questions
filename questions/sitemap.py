#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Question Sitemap
"""

from django.contrib.sitemaps import Sitemap

from questions.models import Question, Answer

class QuestionSitemap(Sitemap):
    """
    SiteMap for Questions
    """

    def changefreq(self, obj):
        return "weekly"

    def priority(self, obj):
        return 1.0

    def items(self):
        return Question.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.last_answer()


class AnswerSitemap(Sitemap):
    """
    SiteMap for Questions
    """

    def changefreq(self, obj):
        return "weekly"

    def priority(self, obj):
        return 1.0

    def items(self):
        return Answer.objects.filter(is_public=True)

    def lastmod(self, obj):
        return obj.last_answer()


