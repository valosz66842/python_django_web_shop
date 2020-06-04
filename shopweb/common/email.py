from .base_url import *
from main.models import SystemConfig,Users
from main.models import ActivationEmail
from email.mime.text import MIMEText
from common.base_url import *
from django.utils import timezone
import smtplib, random, datetime, string
from django.core.mail import send_mail
from django.template import Context, loader
from high.settings_local import EMAIL_HOST_USER
import hashlib
import datetime
from django.forms.models import model_to_dict

def utility(request):
    return {"base_url":base_url}


def hash_code(account):
    h = hashlib.sha256()
    account += str(datetime.datetime.now())
    h.update(account.encode())
    return h.hexdigest()


def user_send_mail(account):
    account_code=hash_code(account)
    account_email=model_to_dict(Users.objects.get(account=account)).get("email")
    account_name = model_to_dict(Users.objects.get(account=account)).get("name")
    systemconfig=SystemConfig(key1=account_code,
                              account=account)
    systemconfig.save()
    email_url = base_url + "enable/"+account_code
    send_mail('吳聲涫 Shop 您好！帳號驗證啟用信',
              '''{}您好！\n\n　　歡迎您加入 吳聲涫 Shop！請點擊以下連結以啟用帳號享受全部的功能！\n\n　　{}\n\n祝 順心\n\n 吳聲涫 Shop 營運團隊敬上'''.format(account_name,email_url),
              EMAIL_HOST_USER,
              [account_email],
              fail_silently=False)


def user_patch_email(email):
    account=model_to_dict(Users.objects.get(email=email)).get("account")
    account_name = model_to_dict(Users.objects.get(email=email)).get("name")
    account_code = hash_code(account)
    SystemConfig.objects.filter(account=account).update(key1=account_code)
    email_url=base_url + "enable/"+account_code
    send_mail('吳聲涫 Shop 您好！帳號驗證啟用信',
              '''{}您好！\n\n　　歡迎您加入 吳聲涫 Shop！請點擊以下連結以啟用帳號享受全部的功能！\n\n　　{}\n\n祝 順心\n\n 吳聲涫 Shop 營運團隊敬上'''.format(account_name,email_url),
              EMAIL_HOST_USER,
              [email],
              fail_silently=False)
