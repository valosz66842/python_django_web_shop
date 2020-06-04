from django_mysql.models import Bit1BooleanField
# class SystemConfig(models.Model):
#     name = models.CharField(primary_key=True, max_length=200)
#     key1 = models.CharField(max_length=200, blank=True, null=True)
#     value1 = models.CharField(max_length=200, blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'system_config'
# from django_mysql.models import Bit1BooleanField
# class ActivationEmail(models.Model): #紀錄是否驗證過的信箱
#     to_user = models.ForeignKey('Users', models.DO_NOTHING)
#     is_expired = Bit1BooleanField(default=False)
#     random_string = models.CharField(max_length=70)
#     send_time = models.DateTimeField()
#     expire_time = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'activation_email'