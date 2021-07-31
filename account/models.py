from django.db import models
from django.contrib.auth.models import PermissionsMixin, User
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('Profile'))
    name = models.CharField(max_length=50, blank=True, verbose_name=_('Name'))
    surname = models.CharField(max_length=50, blank=True, verbose_name=_('Surname'))

    def __str__(self):
        return self.surname


