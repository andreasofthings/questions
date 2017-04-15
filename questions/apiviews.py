#!/usr/bin/env python
# -*- coding: utf-8

"""
:mod:`question` -- Ask user questions.#

"""

from rest_framework import viewsets
from questions.serializers import QuestionSerializer
from questions.serializers import CategorySerializer
from category.models import Category
from .models import Question


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
