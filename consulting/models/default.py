from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django_mysql.models import JSONField
import time


def get_utc_epoch_time():
    return int(round(time.time()))


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    username = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    reset_link = models.CharField(default=None, null=True, max_length=255)
    reset_date = models.IntegerField(default=None, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        db_table = "user"


class Query(models.Model):
    user = models.ForeignKey(User, default=None)
    database = models.CharField(max_length=255, blank=True)
    query = JSONField()
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "query"
