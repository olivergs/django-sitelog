# -*- coding: utf-8 -*-
"""
Website log application
===============================================

.. module:: sitelog
    :platform: Django
    :synopsis: Website log application
.. moduleauthor:: (C) 2013 Oliver Gutiérrez
"""

# Django imports
from django.conf import settings

SITELOG_MAIL_ADMINS_LEVEL = getattr(settings, 'SITELOG_MAIL_ADMINS_LEVEL', 0)
