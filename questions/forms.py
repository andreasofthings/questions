#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""


from django.core.urlresolvers import reverse
from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import InlineRadios

from .models import Question, Answer, Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        fields = ('gender', 'lookfor', 'dob', 'is_public', )
        model = Profile

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.user = kwargs['initial']['profile'].user
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('question:profile-edit')
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        obj = super(ProfileForm, self).save(False)
        obj.user = self.user
        obj.save()
        return obj


class QuestionBaseForm(forms.ModelForm):
    """
    BaseForm for questions.
    """

    def __init__(self, *args, **kwargs):
        super(QuestionBaseForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.user = kwargs['initial'].get('user', None)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'question:submit'
        self.helper.layout = Layout(
            Fieldset(
                _('Question'),
                'question',
            ),
            Submit('submit', _('OK')),
        )

    def save(self, commit=True):
        obj = super(QuestionBaseForm, self).save(False)
        if not obj.submitted_by and hasattr(self, 'user'):
            obj.submitted_by = self.user
        if self.is_valid():
            obj.is_complete = True
        commit and obj.save()
        return obj


class QuestionForm(QuestionBaseForm):
    """
    Form to allow asking questions.
    """
    class Meta:
        fields = ('question', )
        model = Question

    def __init__(self, *args, **kwargs):
        return super(QuestionForm, self).__init__(*args, **kwargs)


class QuestionAdminForm(QuestionBaseForm):
    """
    Form to admin questions.
    """
    class Meta:
        fields = ('question', 'category', )
        model = Question

    def __init__(self, *args, **kwargs):
        super(QuestionAdminForm, self).__init__(*args, **kwargs)


class AnswerQuestionForm(forms.ModelForm):
    """
    Form that allows visitiors of the website to answer questions
    """
    class Meta:
        model = Answer
        exclude = ('question', 'profile',)
        widgets = {
            'user_answer': RadioSelect(),
            'acceptable_answer': CheckboxSelectMultiple(),
            'importance': RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(AnswerQuestionForm, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            self.profile = kwargs['initial']['profile']
            self.question = kwargs['initial']['question']
        else:
            self.question = self.instance.question

        try:
            possible_answers = \
                self.question.possible_answers().values_list("id", "answer")
        except Exception as e:
            raise Exception(e)

        self.fields['user_answer'].choices = possible_answers
        self.fields["acceptable_answer"].choices = possible_answers
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = reverse(
            'question:answer-question',
            kwargs={'pk': self.question.id}
        )
        self.helper.layout = Layout(
            Fieldset(
                _('Question:'),
                HTML("%s" % (self.question)),
                'user_answer',
                'acceptable_answer',
                InlineRadios('importance'),
                'is_public',
                'description',
            ),
            ButtonHolder(
                Submit('submit', _('Submit'), css_class='btn-small'),
            )
        )

    def save(self, commit=True):
        obj = super(AnswerQuestionForm, self).save(False)
        obj.profile = self.profile
        obj.question = self.question
        commit and obj.save()
        commit and self.save_m2m()
        return obj
