"""
.. moduleauthor: Andreas Neumeier <andreas@neumeier.org>
"""

__all__ = [
    'admin',
    'forms',
    'managers',
    'mixins',
    'models',
    'serializers',
    'views',
    'urls',
]

__version__='0.5'

from django.utils.translation import gettext_lazy as _

IMPORTANCE_CHOICES = (
    ('0', _('Not very important')),
    ('1', _('A bit important')),
    ('2', _('I care')),
    ('3', _('Very Important')),
    ('4', _('Mandatory')),
)

GENDER_CHOICES = (
    ('u', _('undefined')),
    ('M', _('Male')),
    ('F', _('Female')),
)

LOOKFOR_CHOICES = (
    ('a', _('any')),
    ('M', _('Man')),
    ('F', _('Female')),
)

VALUE_CHOICES = (
    ('0', '-1.0'),
    ('1', '-0.5',),
    ('2', '0.0',),
    ('3', '0.5',),
    ('4', '1.0',),
)
