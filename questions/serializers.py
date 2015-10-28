#!/usr/bin/env python
# -*- coding: utf-8

"""
:mod:`question.serializers` -- serializers
"""

from rest_framework import serializers
from .models import Question, PossibleAnswer
from category.models import Category


class PossibleAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PossibleAnswer
        fields = (
            'id',
            'possible_answer',
        )


class QuestionSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    possible_answer = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'question',
            'category',
            'possible_answer',
            'male_answer_count',
            'female_answer_count',
            'all_answer_count',
        )


class CategorySerializer(serializers.ModelSerializer):
    def count(self):
        """
        {{ category.question_set.count }}
        """
        return self.question_set.count()

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
        )
