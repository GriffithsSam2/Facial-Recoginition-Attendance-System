from django.db import models
from django.utils.translation import gettext_lazy as _


class Semester(models.Model):
    member = models.CharField(_('Member'), max_length=60)
    department = models.CharField(_('Department'), max_length=120, blank=True)
    programme = models.CharField(_('Program of study'), max_length=120, blank=True)
    semester_year = models.CharField(_('Semester year'), max_length=60)
    semester = models.IntegerField(_('Semester'), default=1)
    attendance = models.IntegerField(_('Expected attendance'), default=1)
    is_current = models.BooleanField(_('is_current'), default=False)

    class Meta:
        verbose_name = _('Semester')
        verbose_name_plural = _('Semesters')

    def __str__(self) -> str:
        return str(self.semester_year)
