#!/usr/bin/env python
# -*- coding: utf-8

"""
:mod:`question.models` --

ORM models to store :mod:`question.models.Profile` persistantly.

"""

import logging
from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.db.models import Q
# from django_countries.fields import CountryField

from category.models import Category

from .managers import ProfileManager
from .managers import QuestionManager
from .managers import AnswerManager

from . import GENDER_CHOICES
from . import LOOKFOR_CHOICES
from . import VALUE_CHOICES
from . import IMPORTANCE_CHOICES

logger = logging.getLogger(__name__)


class Profile(models.Model):
    """
    The actual Profile to describe a user in the context of matchmaking.

    In this module is also covered the business logic, related to individual
    users of the service. It hosts data specific to the user and functions
    for comparing to others.
    """

    user = models.ForeignKey(User, unique=True, related_name="match_profile")
    """Reference to :mod:`django.contrib.auth.models.User`"""

    is_public = models.BooleanField(default=False)
    """Describes whether the profile shall be visible publically."""

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES[0][0]
    )
    """Describe the gender of the user."""

    lookfor = models.CharField(
        max_length=1,
        choices=LOOKFOR_CHOICES,
        default=LOOKFOR_CHOICES[0][0]
    )
    """Describe what gender the user is looking for."""

    dob = models.DateField(blank=True, null=True)
    """Date of Birth."""

    objects = ProfileManager()
    """Use :mod:`question.models.ProfileManager` for Profile.objects."""

    @property
    def age(self):
        """
        Calculate a users age in years.
        """
        return relativedelta(date.today(), self.dob).years

    @property
    def answers(self):
        """
        Return all Answers for this User.

        If `category` is not None, return Answers in the corresponding
        `Category`.
        """
        return Answer.objects.for_profile(self)

    def answers_by_category(self):
        result = dict()
        for r in Category.objects.all():
            result[str(r)] = "0"
#        for a in Answer.objects.for_profile(self):
#            result[str(a.category)] += 1
        return (result,)

    def __str__(self):
        """
        Unicode representation of self
        """
        return u'%s (%s, %s)' % (self.user.username, self.gender, self.age)

    @models.permalink
    def get_absolute_url(self):
        return ('question:profile-view', [str(self.id)])


class Question(models.Model):
    """
    Class to hold actual questions.

    Each Question belongs to a :mod:`category.models.Catgory`
    """

    category = models.ForeignKey(Category, blank=True, null=True)
    """The :mod:`category.models.Catgory` to which the question belongs to."""

    question = models.TextField(null=False)
    """The question."""

    submitted_by = models.ForeignKey(Profile, blank=True, null=True)
    """The question might have been submitted by somebody from the portal."""

    is_active = models.BooleanField(default=False)
    """Whether the question is being asked to people."""

    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text='Short descriptive unique name for use in urls.',
        null=True,
        blank=True
    )
    """Slug for this question."""

    objects = QuestionManager()
    """Reference the :mod:`question.models.QuestionManager`."""

    def possible_answers(self):
        """
        return possible answers for this question.

        :rtype: list of possible answers for this question.

        """
        return self.possible_answer.all()

    def possible_answer_count(self):
        """
        :rtype: count of possible answers for this question.

        """
        return self.possible_answer.all().count()

    def user_answer(self, user):
        """
        :rtype: user answer for this question
        """
        return self.answers.get(user=user)

    def has_answer(self, user):
        """
        Determines whether this question has an answer for the user
        from the argument.

        :rtype: True or False, whether the question was answered.
        """
        if self.answers.filter(profile=user).count():
            return True
        else:
            return False

    def last_answer(self):
        """
        :rtype: date of the last / most recent answer
        """
        answer = self.answers.order_by('-when')
        if answer.count() < 1:
            return None
        else:
            return answer[0].when

    def male_answer_count(self):
        """
        :rtype: How often male users answered this question.
        """
        return self.answers.filter(
            profile__user__match_profile__gender='M'
        ).count()

    def female_answer_count(self):
        """
        :rtype: How often female users answered this question.
        """
        return self.answers.filter(
            profile__user__match_profile__gender='F'
        ).count()

    def all_answer_count(self):
        """
        :rtype: How often this question was answered.
        """
        return self.answers.all().count()

    def male_quote(self):
        answers = self.all_answer_count()
        if answers > 0:
            return self.male_answer_count() / answers
        else:
            return 0

    def female_quote(self):
        answers = self.all_answer_count()
        if answers > 0:
            return self.female_answer_count() / answers
        else:
            return 0

    def male_matches(self, user):
        """
        return quote of answers that would accept the users answer
        """
        answer = self.user_answer(user)
        raise NotImplemented

    def female_matches(self, user):
        """
        return quote of answers that would accept the users answer
        """
        answer = self.user_answer(user)
        raise NotImplemented

    def answer_percent(self):
        """
        returns an dictionairy where the key is the possible answer and the
        value is the percent of give answers
        """
        result = {}
        answer_count = float(self.all_answer_count())
        for answer in self.possible_answers():
            user_answer_count = float(Answer.objects.filter(
                question=self,
                user_answer=answer
            ).count())
            if user_answer_count > 0:
                """Only if somebody answered this question before."""
                result[answer] = int(
                    (user_answer_count / answer_count) * 100.0
                )
            else:
                """It has to be 0.0% otherwise."""
                result[answer] = 0.0
        return result

    def acceptable_percent(self):
        """
        returns an dictionairy where the key is the possible answer and the
        value is the percent of give answers
        """
        answer_count = float(self.all_answer_count())
        result = {}
        for answer in self.possible_answers():
            acceptable_answer_count = Answer.objects.filter(
                question=self,
                acceptable_answer=answer
            ).count()
            if answer_count > 0:
                result[answer] = int(
                    (acceptable_answer_count / answer_count) * 100.0)
            else:
                result[answer] = 0
        return result

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)
        super(Question, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('question:question-detail', [str(self.id)])


class PossibleAnswer(models.Model):
    question = models.ForeignKey(Question, related_name="possible_answer")
    answer = models.CharField(max_length=200)

    value = models.CharField(max_length=1, choices=VALUE_CHOICES, default='2')

    def __str__(self):
        return str(self.answer)


class Answer(models.Model):
    """
    Store the answer a user(profile) can give to a question.

    The class contains functions related to individual answers.

    .. moduleauthor: Andreas Neumeier <andreas@neumeier.org>
    """
    question = models.ForeignKey(Question, related_name='answers')
    """Which question is this the answer for?"""

    profile = models.ForeignKey(Profile)
    """The (user)profile to which this answer belongs to."""

    when = models.DateTimeField(auto_now=True, auto_now_add=True)
    """The date and time when this answer was given."""

    user_answer = models.ForeignKey(
        PossibleAnswer,
        null=True,
        related_name="user_answer",
        verbose_name=_("users answer")
    )
    """The value of the answer the user has given. This is a single value."""

    acceptable_answer = models.ManyToManyField(
        PossibleAnswer,
        blank=True,
        related_name="acceptable_answer",
        verbose_name=_("answer the user would answer")
    )
    """The answers the user would allow from a potential matching partner."""

    importance = models.CharField(
        max_length=1,
        choices=IMPORTANCE_CHOICES, default='2'
    )
    """How important are answer and acceptable answers to the user."""

    is_public = models.BooleanField(default=True)
    """A user may choose to answer this privately, with default to public."""

    description = models.TextField(null=True, blank=True)
    """Allow the user to leave a statement or description to his answer."""

    objects = AnswerManager()

    class Meta:
        unique_together = (("question", "profile"),)

    def __str__(self):
        str_template = """
        %s answered question "%s" with: %s (and will accept %s as an answer)
        """
        return str_template % (
            self.profile,
            self.question.question,
            self.user_answer,
            self.acceptable_answer.all()
        )

    def save(self, *args, **kwargs):
        super(Answer, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('question:answer-detail', [str(self.id)])


class CatScore(models.Model):
    user = models.ForeignKey(User, unique=True)
    cat = models.ForeignKey(Category, unique=True)
    score = models.FloatField()

    class Meta:
        unique_together = (("user", "cat",))


class FacebookAnswerStatus(models.Model):
    answer = models.ForeignKey(Answer, related_name="facebook_status")
    user = models.ForeignKey(User)
    fid = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)


# vim: ts=4 et sw=4 sts=4
