# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Boss(models.Model):
    business_id = models.IntegerField(unique=True)
    settings_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'boss'


class Business(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'business'


class BusinessStores(models.Model):
    business_id = models.IntegerField()
    store_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'business_stores'
        unique_together = (('business_id', 'store_id'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ItemLog(models.Model):
    action = models.CharField(max_length=255)
    operation = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    change = models.CharField(max_length=255)
    previous_value = models.CharField(max_length=255)
    date = models.IntegerField()
    details = models.TextField()  # This field type is a guess.
    business_id = models.IntegerField(blank=True, null=True)
    store_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'item_log'


class Settings(models.Model):
    start_time = models.IntegerField()
    date_range = models.CharField(max_length=15)
    ip_address = models.CharField(max_length=100)
    header = models.TextField()  # This field type is a guess.
    footer = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'settings'


class Store(models.Model):
    name = models.CharField(max_length=100)
    tax = models.CharField(max_length=12)
    link_columns = models.TextField()  # This field type is a guess.
    include_columns = models.TextField()  # This field type is a guess.
    columns = models.TextField()  # This field type is a guess.
    picture_column = models.CharField(max_length=100)
    inventory = models.TextField()  # This field type is a guess.
    order_by = models.CharField(max_length=100)
    reverse = models.IntegerField()
    transaction_filter = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'store'


class Transaction(models.Model):
    items = models.TextField()  # This field type is a guess.
    payment_type = models.CharField(max_length=255)
    tax = models.CharField(max_length=12)
    subtotal = models.CharField(max_length=255)
    memo = models.CharField(max_length=255)
    date = models.IntegerField()
    boss_id = models.IntegerField()
    seller_id = models.IntegerField()
    store_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transaction'


class InventoryUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=15)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    reset_link = models.CharField(max_length=255, blank=True, null=True)
    reset_date = models.IntegerField(blank=True, null=True)
    is_staff = models.IntegerField()
    is_superuser = models.IntegerField()
    boss_id = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
