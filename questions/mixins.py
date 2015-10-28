#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from braces.views import LoginRequiredMixin
from question.models import Profile
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class ProfileRequiredMixin(LoginRequiredMixin):
    """
    Mixin for all pages that require a userprofile.

    If user has no profile, redirect to the profile page first.
    """
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return HttpResponseRedirect(reverse('question:profile-edit'))

        return super(
            ProfileRequiredMixin,
            self
        ).dispatch(request, *args, **kwargs)
