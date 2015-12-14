#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Tasks to compare user profiles, other related functions.
"""
from __future__ import absolute_import

from celery import shared_task


@shared_task
def debug():
    return 0

# vim: ts=4 et sw=4 sts=4
