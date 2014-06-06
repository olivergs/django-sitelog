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
# Django imports
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.admin import GenericTabularInline

# Application imports
from sitelog.models import SiteLog

class SiteLogInline(GenericTabularInline):
    """
    Site log inline administration class
    """
    model = SiteLog

    def has_add_permission(self, request):
        return False

class SiteLogAdmin(admin.ModelAdmin):
    """
    Administration class
    """
    # Admin parameters    
    list_display = ('timestamp','tag','message','level','ip','user','content_type','object_id','admin_content_object')
    list_filter = ('timestamp','level','tag','user')
    search_fields = ('message','tag','user__username','user__first_name','user__last_name','ip','data')
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False

    def admin_content_object(self,obj):
        """
        Show content object unicode representation
        """
        try:
            if obj.content_object:
                return unicode(obj.content_object)
        except:
            pass
        return None
    admin_content_object.short_description=_('Content object')

# Admin models registration
admin.site.register(SiteLog, SiteLogAdmin)
