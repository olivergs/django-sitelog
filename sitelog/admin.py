# -*- coding: utf-8 -*-
"""
Website log application administration module
===============================================

.. module:: 
    :platform: Django
    :synopsis: Website log application administration module
.. moduleauthor:: (C) 2013 Oliver Gutiérrez

TODO: Action for exporting log to text files, CSV, etc.
"""
# Python imports

# Django imports
from django.contrib import admin

# EVODjango imports
from evodjango.admin import BaseGenericTabularInline,BaseModelAdmin

# Application imports
from sitelog.models import SiteLog

class SiteLogInline(BaseGenericTabularInline):
    """
    Site log inline administration class
    """
    model = SiteLog
    all_fields_readonly=True
    superuser_skips_all_readonly=False

    def has_add_permission(self, request):
        return False

class SiteLogAdmin(BaseModelAdmin):
    """
    Administration class
    """
    # Admin parameters    
    list_display = ('timestamp','tag','message','level','ip','user','content_type','object_id','content_object',)
    list_filter = ('timestamp','level','tag','user')
    search_fields = ('message','tag','user__username','user__first_name','user__last_name','ip','data')
    ordering = ('-timestamp',)
    all_fields_readonly = True

    def has_add_permission(self, request):
        return False

# Admin models registration
admin.site.register(SiteLog, SiteLogAdmin)
