from django.db import models
from django.utils.translation import gettext_lazy as _


def lecturer_image_file(instance, filename):
    return '/'.join(['images', 'lecturers', '', filename])


class Lecturer(models.Model):
    
    first_name = models.CharField(_('First name'), max_length=60)
    last_name = models.CharField(_('Last name'), max_length=60)
    dob = models.DateField(_('Date of birth'))
    department = models.CharField(_('Department'), max_length=120)
    photo = models.ImageField(_('Photo'), upload_to=lecturer_image_file)

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

    def __str__(self):
        return f'{self.first_name} {self.first_name}'.strip()
