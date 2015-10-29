#!/usr/bin/env python
# -*- coding: utf-8

"""
:mod:`question` -- Ask user questions.

.. module:: question
    :platform: Python

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
"""

from django.views.generic.edit import CreateView, UpdateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView

from category.models import Category

from .models import Question, Answer, Profile
from .forms import ProfileForm, QuestionForm, AnswerQuestionForm
from .mixins import ProfileRequiredMixin


class Home(TemplateView):
    """
    .. class:: Home

    A static page that marks the entrypage to this application.

    The application allows any eligable user to answer questions from
    categories, and to match his answers to other users preferences.

    Part of this application are :mod:`models.Question`s,
    :mod:`models.PossibleAnswer`s, `Answer`s and the users `Profile`.

    Requires Login
    Requires Group Membership: 'question'

    .. codeauthor:: Andreas Neumeier

    """
    template_name = "question/home.html"
    group_required = u'question'
    # permission_required = "question"
    login_url = "/profile/login/"

    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(*args, **kwargs)
        context['category_count'] = Category.objects.count()
        return context


class ProfileEditView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    """
    .. class:: ProfileEditView

    Allow a user to view and edit his own profile.

    User is self.request.user
    """
    template_name = "question/profile_edit.html"
    group_required = u'question'
    login_url = "/profile/login/"
    model = Profile
    form_class = ProfileForm

    def get_object(self, queryset=None):
        """
        Get or create the userprofile.
        """
        obj, created = Profile.objects.get_or_create(user=self.request.user)
        if created:
            obj.save()
        return obj

    def get_initial(self):
        """
        Get initial values for 'user', to ensure no other user is edited.
        """
        profile = Profile.objects.get(user=self.request.user.pk)
        self.initial.update({'profile': profile})
        return self.initial


class ProfileView(LoginRequiredMixin, GroupRequiredMixin, DetailView):
    """
    .. class:: ProfileView

    Allow a user to view a profile.

    """
    template_name = "question/profile_view.html"
    group_required = u'question'
    login_url = "/profile/login/"
    model = Profile

    def get_queryset(self, queryset=None):
        """
        Filter all non public profiles.
        """
        return Profile.objects.filter(is_public=True)


class QuestionList(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """
    .. class:: QuestionList

    Display a list of questions the user can answer.
    Requires user to be in the 'questions' group
    """
    model = Question
    group_required = u'question'
    template_name = "question/question_list.html"

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user.pk)
        return Question.objects.unanswered(profile)


class QuestionDetail(DetailView):
    """
    .. class:: QuestionDetail

    Show details for a question.

    This shall include:
    - the question
    - possible answers
    - stats about already given answers
    """
    model = Question
    template_name = "question/question_detail.html"
    login_url = "/profile/login/"
    group_required = u'question'


class AnswerList(GroupRequiredMixin, ProfileRequiredMixin, ListView):
    """
    .. class:: AnswerList

    List all given answers for the logged in user.
    A user shall see his answers, but not (in listing) which other user
    answered which questions. This shall only be achievable by comparing two
    users.

    .. seealso:: :mod:`questions.views.Match`.

    .. seealso:: :mod:`questions.views.Compare`.

    .. codeauthor:: Andreas Neumeier
    """

    model = Answer
    """Based on the :mod:`questions.models.Answer` model."""

    group_required = u'question'
    """Requires user to belong to the 'question' group of users."""

    template_name = "question/answer_list.html"
    """Use the 'question/answer_list.html' template to render the result."""

    def get_queryset(self):
        """
        .. classmethod:: get_queryset(self)

        Returns an :mod:`questions.models.Answer`-queryset that is filtered for
        Answers from the current user.

        :rtype: A queryset for :mod:`questions.models.Answer`

        """
        return Profile.objects.get(user=self.request.user).answers
        # return Answer.objects.filter(profile__user=self.request.user)


class AnswerDetail(DetailView):
    model = Answer
    group_required = u'question'
    template_name = "question/answer_detail.html"

    def get_queryset(self):
        return self.model.objects.public()


class AnswerQuestion(GroupRequiredMixin, ProfileRequiredMixin, UpdateView):
    model = Answer
    group_required = u'question'
    form_class = AnswerQuestionForm
    template_name = "question/answer_question.html"

    def get(self, *args, **kwargs):
        self.question = Question.objects.get(pk=kwargs['pk'])
        return super(AnswerQuestion, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.question = Question.objects.get(pk=kwargs['pk'])
        return super(AnswerQuestion, self).post(*args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        question = self.question

        try:
            obj = queryset.get(
                profile__user=self.request.user,
                question=question
            )
        except Answer.DoesNotExist:
            obj = None
        return obj

    def get_initial(self):
        self.initial.update(
            {'profile': Profile.objects.get(user=self.request.user)}
        )
        self.initial.update(
            {'question': self.question}
        )
        return self.initial


class CategoryList(ListView):
    model = Category
    template_name = "question/category_list.html"

    def get_queryset(self):
        return Category.objects.all()  # filter(parent__title="Questions")


class CategoryDetail(DetailView):
    model = Category
    template_name = "question/category_detail.html"


class Submit(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    group_required = u'question'
    template_name = "question/submit.html"

    def get_initial(self):
        self.initial.update(
            {'user': self.request.user}
        )
        return self.initial


class ProfileList(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Profile
    group_required = u'question'
    paginate_by = 10
    template_name = "question/profile_list.html"


class Compare(LoginRequiredMixin, GroupRequiredMixin, ListView):
    """
    .. class:: Compare

    Compare a users answers to own answers.
    Shows answers for one user and allows to see difference to viewing user.

    :param pk: The primary key of the Profile to compare to.

    """

    group_required = u'question'
    """User will be required to be in group 'question'."""

    template_name = "question/compare.html"
    login_url = "/profile/login/"

    def get_queryset(self):
        """
        .. classmethod:: get_queryset(self)

        All questions that were answered by either the viewing user
        or the user being looked at.

        :param pk: Primary Key of the user-profile to compare to.

        :rtype: a list of :mod:`questions.model.Question` the user has
        :mod:`questions.model.Answer` for.

        """
        other = self.kwargs['pk']
        return Question.objects.answered(other)

    def get_context_data(self, **kwargs):
        """
        .. classmethod:: get_context_data(self, (*args, (**kwargs)))

        :rtype: Profile of the user to compare to.
        """
        context = super(Compare, self).get_context_data(**kwargs)
        other = self.kwargs['pk']  # Other profile ID!
        context['profile'] = Profile.objects.get(pk=self.request.user.pk)
        context['other'] = Profile.objects.get(pk=other)
        context['others_questions'] = self.get_queryset()
        return context


#
# API
#

from rest_framework import viewsets
from questions.serializers import QuestionSerializer
from questions.serializers import CategorySerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API View for Questions
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API View for Categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# vim: ts=4 et sw=4 sts=4
