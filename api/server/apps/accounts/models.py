from __future__ import unicode_literals

import textwrap
from typing import Final, final

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken

from server.apps.accounts.logic.managers import UserManager


def user_image_file(instance, filename):
    return '/'.join(['images', 'users', '', filename])


@final
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    first_name = models.CharField(_('First name'), max_length=60, blank=True)
    last_name = models.CharField(_('Last name'), max_length=60, blank=True)
    photo = models.ImageField(_('Photo'), upload_to=user_image_file)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('Active'), default=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_tokens(self):
        tokens = RefreshToken.for_user(self)
        return {
            'refresh-token': str(tokens),
            'access-token': str(tokens.access_token)
        }

    def __str__(self) -> str:
        """ Return email as representation string. """
        return str(self.email)
