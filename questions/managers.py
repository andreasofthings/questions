#!/usr/bin/env python
# -*- coding: utf-8

"""
:mod:`question.managers` -- managers
"""

import logging
from django.db import models


logger = logging.getLogger(__name__)


class ProfileManager(models.Manager):
    """
    .. class:: ProfileManager

    Django Manager class for :mod:`question.models.Profile` objects.

    It provides simple statistic methods.
    """

    def female(self):
        """
        .. classmethod:: female(self)

        Returns the number of all female profiles in database.

        :rtype: count of female profiles.

        .. todo: Should depend on the definition in the module, not a
        magic tring.
        """
        return super(ProfileManager, self).get_queryset().filter(
            gender='F'
        )

    def male(self):
        """
        .. classmethod:: male(self)

        Returns all male profiles in database.

        :rtype: all male profiles.

        .. todo: Should depend on the definition in the module, not a
        magic tring.
        """
        return super(ProfileManager, self).get_queryset().filter(
            gender='M'
        )

    def female_percent(self):
        """
        .. classmethod:: female_percent(self)

        Returns the percent of female profiles in database.

        :rtype: percent of female profiles.
        """
        return float(self.female().count()) / float(self.count())

    def male_percent(self):
        """
        .. classmethod:: male_percent(self)

        Returns the percent of male profiles in database.

        :rtype: percent of male profiles.
        """
        return float(self.male().count()) / float(self.count())

    def age_range(start, end):
        """
        return all profiles in a range between `start` and `end`.
        """
        if start > end:
            """
            Swap `start` and `end` if `start` is after `end`.
            """
            tmp = end
            end = start
            start = tmp
        return self.objects.filter(dob__gt=start).filter(dob_lt=end)
        """Filter objects greater than `start` and less than `end`."""

    def get_by_natural_key(self, username):
        return self.get(username=username)

class QuestionManager(models.Manager):
    """
    .. class:: QuestionManager

    Django Manager class for :mod:`question.models.Question` objects.

    It provides simple statistic methods.
    """

    def answered(self, profile):
        """
        .. method:: answered(self, profile)

        :rtype: queryset filtered for questions answered by provided user.

        get all answers for user
        """
        return self.filter(answers__profile=profile)

    def unanswered(self, profile):
        """
        .. method:: unanswered(self, user)

        :rtype: queryset filtered for questions unanswered by provided user.
        """
        return self.exclude(answers__profile=profile)

    def get_by_natural_key(self, slug):
        """
        Get Questions by natural kea to allow serialization
        """
        return self.get(slug=slug)

class AnswerManager(models.Manager):
    def for_profile(self, profile):
        """
        Return answers for this profile.
        """
        return self.filter(profile=profile)

    def public(self):
        """
        filter answers that have the same user answer
        """
        return self.filter(is_public=True)

    def agree(self, instance):
        """
        filter answers that have the same user answer
        """
        total_answers = self.filter(question=self.instance.question)
        agreeing_answers = total_answers.filter(
            user_answer=self.instance.user_answer
        )
        return agreeing_answers / total_answers
