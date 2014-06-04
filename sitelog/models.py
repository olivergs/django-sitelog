# -*- coding: utf-8 -*-
"""
Web site log application models module
===============================================

.. module:: 
    :platform: Django
    :synopsis: Web site log application models module
.. moduleauthor:: (C) 2013 Oliver Gutiérrez

TODO: Integrate with django logging facilities (https://docs.djangoproject.com/en/dev/topics/logging/)
"""

# Python imports
import sys
import traceback

# Django imports
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from django.utils.translation import ugettext_lazy as _
from django.core.mail import mail_admins as django_mail_admins
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class SiteLog(GenericNullModel):
    """
    Web site log model
    """
    INFO=1
    WARNING=2
    ERROR=3
    CRITICAL=4
    DEBUG=5
        
    LOG_LEVELS=(
        (INFO,_('Info')),
        (WARNING,_('Warning')),
        (ERROR,_('Error')),
        (CRITICAL,_('Critical')),
        (DEBUG,_('Debug')),
    )
    
    class Meta:
        """
        Metadata for this model
        """
        verbose_name=_('Site log')
        verbose_name_plural=_('Site logs')
    
    timestamp=models.DateTimeField(_('Created'),auto_now_add=True,
        help_text=_('Creation date'))
    site=models.ForeignKey(Site,verbose_name=_('Site'),blank=True, null=True,
        help_text=_('Associated website'))
    level=models.PositiveIntegerField(_('Level'),default=1,choices=LOG_LEVELS,
        help_text=_('Log level'))
    tag=models.CharField(_('Tag'),max_length=20,default='django',
        help_text=_('Tag for identifying this log message sender'))
    user=models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_('User'),blank=True,null=True,
        help_text=_('Associated user'))
    ip=models.GenericIPAddressField(_('IP address'),default='0.0.0.0',
        help_text=_('Associated IP address'))
    message=models.CharField(_('Message'),max_length=200,
        help_text=_('Log message'))
    data=models.TextField(_('Data'),blank=True,null=True,
        help_text=_('Extra data for log message'))
    content_type = models.ForeignKey(ContentType,verbose_name=_('Content type'),blank=True,null=True,
        help_text=_('Associated content type'))
    object_id = models.PositiveIntegerField(_('Object ID'),blank=True,null=True,
        help_text=_('Associated object identifier'))
    content_object = GenericForeignKey('content_type', 'object_id')


    @staticmethod
    def log(tag,message,data=None,level=INFO,content_object=None,request=None,ip=None,user=None,site=None,mail_admins=False,callback=None):
        """
        Logs a message into site log
        """
        # Set IP value
        if ip is None:
            if not request is None:
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    ip=request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
                else:
                    ip=request.META['REMOTE_ADDR']
            else:
                ip='0.0.0.0'
                
        # Set user value
        if user is None:
            if not request is None:    
                if request.user.is_authenticated():
                    user=request.user
        
        # Set site value
        if site is None:
            if not request is None:
                site=get_current_site(request)
            else:
                site=Site.objects.get_current()
        # Check exceptions    
        if sys.exc_info() != (None,None,None):
            if data is not None:
                data=unicode(data) + '\n\n---\n' + traceback.format_exc()
            else:
                data=traceback.format_exc()

        # Save log object
        log=SiteLog(tag=tag,message=u'%s' % message,level=level,data=u'%s' % data,ip=ip,user=user,site=site)
        log.content_object=content_object
        log.save()
        
        # Mail admins if specified or needed
        if mail_admins or log.level <= settings.SITELOG_MAIL_ADMINS_LEVEL:
            print log
            body=render_to_string('sitelog/mail_admins.html', {'log': log})
            django_mail_admins(message,body,fail_silently=True)

        # Callback execution
        if callback is not None:
            return callback(log)

    def __unicode__(self):
        """
        Model unicode representation
        """
        return u'%s %s %s: %s' % (self.timestamp,self.get_level_display(),self.tag,self.message)
