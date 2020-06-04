from django.db import models


class ActivationEmail(models.Model):
    to_user = models.CharField(primary_key=True, max_length=200)
    is_expired = models.IntegerField()
    random_string = models.CharField(max_length=100)
    send_time = models.DateTimeField()
    expire_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'activation_email'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Business(models.Model):
    buyer = models.CharField(max_length=200)
    seller = models.CharField(max_length=200)
    amount = models.CharField(max_length=100)
    totalprice = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100)
    transactiontime = models.DateTimeField()
    ordernumber = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'business'


class ConfirmString(models.Model):
    code = models.CharField(max_length=100, blank=True, null=True)
    user = models.CharField(max_length=100)
    time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'confirm_string'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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



class Limitedtime(models.Model):
    seller = models.CharField(max_length=200)
    limitquantity = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100)
    srcset = models.ImageField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'limitedtime'


class MainConfirmstring(models.Model):
    code = models.CharField(max_length=256)
    time = models.DateTimeField()
    user_id = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'main_confirmstring'


class MainImg(models.Model):
    img_url = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'main_img'





class Record(models.Model):
    title = models.CharField(max_length=2000, blank=True, null=True)
    ip = models.CharField(max_length=2000, blank=True, null=True)
    date = models.CharField(db_column='Date', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    time = models.CharField(db_column='Time', max_length=2000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'record'


class SnippetsSnippet(models.Model):
    created = models.DateTimeField()
    title = models.CharField(max_length=100)
    code = models.TextField()
    linenos = models.IntegerField()
    language = models.CharField(max_length=100)
    style = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'snippets_snippet'


class SystemConfig(models.Model):
    account = models.CharField(primary_key=True, max_length=100)
    key1 = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'system_config'


class Udn(models.Model):
    title = models.CharField(max_length=2000, blank=True, null=True)
    link = models.CharField(max_length=2000, blank=True, null=True)
    report = models.CharField(max_length=2000, blank=True, null=True)
    content = models.CharField(max_length=2000, blank=True, null=True)
    time = models.CharField(max_length=2000, blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=200)
    img = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'udn'

import django.utils.timezone as timezone
class Users(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    time = models.DateTimeField(default=timezone.now)
    confirmed = models.IntegerField()
    account = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'users'

class Product(models.Model):
    title = models.CharField(max_length=2000, blank=True, null=True)
    srcset = models.CharField(max_length=1000)
    sold = models.IntegerField()
    money = models.IntegerField()
    sell = models.CharField(max_length=1000)
    id = models.IntegerField(primary_key=True)
    stock = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product'

