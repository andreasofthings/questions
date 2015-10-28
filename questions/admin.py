#!/usr/bin/env python
# -*- coding: utf-8

"""
:mod:`admin` -- Django Admin


PossibleAnswerInline
####################

AnswerInline
############

QuestionAdmin
#############

AnserAdmin
##########

ProfileAdmin
############

"""


from django.contrib import admin

from question.models import Question, Answer, PossibleAnswer, Profile
from question.forms import QuestionAdminForm, AnswerQuestionForm


class PossibleAnswerInline(admin.TabularInline):
    """
    Inline Form to display/edit possible answers from `QuestionAdmin`.
    """
    model = PossibleAnswer
    extra = 1
    fieldsets = [
        (
            'Possible Answers', {
                'fields': ['answer', 'value'],
                'classes': ('collapse'),
            }
        ),
    ]


class AnswerInline(admin.TabularInline):
    """
    User Answer for a particular question
    """
    model = Answer
    extra = 1

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "acceptable_answers":
            kwargs['choices'] = (('a', 'a'), ('b', 'b'),)
        return super(AnswerInline, self).formfield_for_choice_field(
            db_field,
            request,
            **kwargs
        )


class QuestionAdmin(admin.ModelAdmin):
    """
    User Question options
    """
    change_form_template = 'question/admin/question_change_form.html'
    form = QuestionAdminForm

    fieldset = (
        None,
        ('question', )
    )
    list_display = (
        'question',
        'submitted_by',
        'category',
        'possible_answer_count',
        'all_answer_count',
    )

    inlines = [PossibleAnswerInline, AnswerInline]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        return super(QuestionAdmin, self).change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context
        )


class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    form = AnswerQuestionForm


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'gender', 'age', 'is_public',)
    list_filter = ('is_public',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Answer, AnswerAdmin)
