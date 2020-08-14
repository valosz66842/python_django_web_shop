import random
import time
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# Create your views here.
from .models import Users, Business, ActivationEmail, Product, Limitedtime, SystemConfig
from itsdangerous import URLSafeTimedSerializer as utsr
import base64
from django.template import loader, Context, RequestContext
from django.template.loader import get_template
import re
from django.db.models import Q
import random
import string
import sys
from PIL import Image, ImageDraw, ImageFont
import datetime
from .form import UsersForm, ProductForm
import hashlib
from django.core.mail import EmailMultiAlternatives
from high import settings
from .form import UsersForm
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict
import json
import datetime
import random
from rest_framework import viewsets
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.decorators import list_route, detail_route
from django.db import transaction


class UsersViewSet(viewsets.ModelViewSet):

    @list_route(methods=['post'])
    def login(self, request):

        result = {"status": False, "errcode": None, "errmsg": None, "account": None}
        data = request.data
        account = data.get('account')
        password = data.get('password')
        user = Users.objects.filter(account=account, password=password)

        if user:
            request.session['account'] = account  # 使用session來保存用戶登錄信息
            request.session['password'] = password
            result["status"] = True
            result['account'] = account

            return JsonResponse(result)

        elif (Users.objects.filter(account=account).exists()):
            result["errcode"] = 410
            result["errmsg"] = "密碼錯誤"

            return JsonResponse(result)

        else:
            result["errcode"] = 411
            result["errmsg"] = "帳號不存在"

            return JsonResponse(result)

    @list_route(methods=['post'])
    def logout(self, request):
        request.session['account'] = None
        request.session['password'] = None

        return JsonResponse({"status": True})

    @list_route(methods=['post'])
    def regist(self, request):
        result = {"status": False, "errcode": None, "errmsg": None}
        if request.method == 'POST':
            login_form = UsersForm(request.POST)
            if login_form.is_valid():  # 表單有效
                name = login_form.cleaned_data.get('name')
                password = login_form.cleaned_data.get('password')
                email = login_form.cleaned_data.get('email')
                phone = login_form.cleaned_data.get('phone')
                account = login_form.cleaned_data.get('account')
                if Users.objects.filter(account=account).exists():
                    result["errcode"] = 410
                    result["errmsg"] = "此帳號已經存在"
                elif Users.objects.filter(email=email).exists():
                    result["errcode"] = 411
                    result["errmsg"] = '此信箱已註冊過'
                elif Users.objects.filter(phone=phone).exists():
                    result["errcode"] = 412
                    result["errmsg"] = '此手機號碼已註冊過'
                else:
                    try:
                        new_user = Users(name=name,
                                         password=password,
                                         email=email,
                                         phone=phone,
                                         account=account,
                                         confirmed=0)
                        new_user.save()
                        result["status"] = True
                        user_send_mail(account)
                    except Exception as e:
                        result["errcode"] = 404
                        result["errmsg"] = str(e)
            else:
                result["errcode"] = 402
                result["errmsg"] = "表單無效"
        else:
            result["errcode"] = 400
            result["errmsg"] = "非GET請求"
        print(result["errmsg"])
        return JsonResponse(result)


class ProductViewSet(viewsets.ModelViewSet):

    @list_route(methods=['post'])
    def ajax_time(self, request):  # 限時特賣的AJAX

        result = {"status": False, "errcode": None, "errmsg": None}

        if request.method == "POST":
            account = request.session.get('account')
            data = request.data
            product_list = data.get("product_list")  # 要特賣的所有商品 [0]限制數量 [1]特價 [2]商品ID [3]開始 [4]結束日期
            product_list = eval(product_list)
            if product_list:
                for product in product_list:
                    product[3] = date_format(product[3])
                    product[4] = date_format(product[4])
                    Limitedtime_modles = Limitedtime(seller=account,
                                                     limitquantity=product[0],
                                                     product_id=product[2],
                                                     price=product[1],
                                                     starttime=product[3],
                                                     endtime=product[4],
                                                     id=make_id(),
                                                     srcset=str(model_to_dict(Product.objects.get(id=product[2])).get(
                                                         "srcset")))
                    Limitedtime_modles.save()
                result["status"] = True

            else:
                result["errcode"] = 404
                result["errmsg"] = "沒有這個商品"
        else:
            result["errcode"] = 400
            result["errmsg"] = "不是GET請求"

        return JsonResponse(result)

    @list_route(methods=['post'])
    def checkout(self, request):  # 結帳的Ajax
        result = {"status": False, "errcode": None, "errmsg": ""}
        if 'account' in request.session:
            user = Users.objects.get(account=request.session['account'])
        else:
            user = None
        if user == None:
            return HttpResponseRedirect("請登入進行購買")
        else:
            if request.method == "POST":
                data = request.data
                product_list = data.get("product_list")  # 要結帳的所有商品 ID跟數量
                product_list = eval(product_list)
                atomicity = True
                error_list = []
                ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
                try:
                    with transaction.atomic():
                        for product_count, product in enumerate(product_list):
                            product_data = Product.objects.select_for_update().get(id=product[0])
                            # product_data = Product.objects.get(id=product[0])
                            product_dict = model_to_dict(product_data)
                            if (int(product_dict["stock"]) - int(product_dict["sold"]) - int(
                                    product[1])) >= 0:  # 檢查商品數量是否足夠
                                newsold = int(product_dict["sold"]) + int(product[1])
                                business = Business(buyer=request.session.get("account"),
                                                    seller=product_dict.get("sell"),
                                                    amount=product[1],
                                                    totalprice=str(int(product_dict.get("money")) * int(product[1])),
                                                    transactiontime=datetime.datetime.now().strftime(ISOTIMEFORMAT),
                                                    product_id=product[0],
                                                    ordernumber=make_ordernumber())
                                Product.objects.filter(id=product[0]).update(sold=newsold)
                                business.save()
                            else:
                                error_list.append(product_data.title + "數量不足")
                except:
                    atomicity = False
                    error_list.append(str(product_data.id) + " error,")
                if atomicity:
                    result["status"] = True
                    request.session["ber_car_list"] = None
                else:
                    result["errcode"] = 404
                    for error in error_list:
                        result["errmsg"] += error

            else:
                result["errcode"] = 400
                result["errmsg"] = "非GET請求"

        return JsonResponse(result)

    @list_route(methods=['post'])
    def directly_buy(self, request):  # 直接購買
        result = {"status": False, "errcode": None, "errmsg": None}

        if 'account' in request.session:
            user = Users.objects.get(account=request.session['account'])
        else:
            user = None
        if user == None:
            return HttpResponseRedirect("請登入進行購買")
        else:
            if request.method == "POST":
                product = request.POST.get("product_list")
                product = eval(product)
                result["errmsg"] = product
                ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'
                product_data = model_to_dict(Product.objects.get(id=product[0]))
                business = Business(buyer="account",
                                    seller="sell",
                                    amount=product[1],
                                    totalprice=str(int(product_data.get("money")) * int(product[1])),
                                    transactiontime=datetime.datetime.now().strftime(ISOTIMEFORMAT),
                                    product_id=product[0],
                                    ordernumber=make_ordernumber())
                business.save()
                result["status"] = True
            else:
                result["errcode"] = 400
                result["status"] = "非POST請求"

        return JsonResponse(result)

    @list_route(methods=['post'])
    def del_buy_car(self, request):  # 刪除購物車
        result = {"status": False, "errcode": None, "errmsg": None}

        if request.method == "POST":
            data = request.data
            product_id = data.get("product_id")
            if product_id:
                ber_car_list = request.session.get("ber_car_list")
                for n, product in enumerate(ber_car_list):
                    if product[0] == product_id:
                        del ber_car_list[n]
                        result["status"] = True
                request.session["ber_car_list"] = ber_car_list
            else:
                result["errcode"] = 404
                result["errmsg"] = "刪除失敗"
        else:
            result["errcode"] = 400
            result["errmsg"] = "非POST請求"

        return JsonResponse(result)

    @list_route(methods=['post'])
    def ber_car(self, request):  # 新增購物車

        result = {"status": False, "errcode": None, "errmsg": None}

        if request.method == "POST":
            data = request.data
            product_id = data.get("product_id")
            product_count = data.get("product_count")
            try:
                product = Product.objects.get(id=product_id)
            except:
                product = None
            if product == None:
                result['errcode'] = 404
                result['errmsg'] = "沒有這個商品"
            else:
                ber_car_list = request.session.get("ber_car_list")
                repeat = False
                if ber_car_list:
                    for n, product_list in enumerate(ber_car_list):
                        if product_list[0] == product_id:
                            product_list[1] = int(product_list[1]) + int(product_count)
                            repeat = True
                            ber_car_list[n] = [product_list[0], int(product_list[1])]
                    if repeat == False:
                        ber_car_list.append([product_id, product_count])
                    request.session["ber_car_list"] = ber_car_list
                else:
                    request.session["ber_car_list"] = [[product_id, product_count]]
                result['status'] = 1
        else:
            result['errcode'] = 400
            result['errmsg'] = "非POST請求"

        return JsonResponse(result)

    def joinstring(self, string, symbol):
        string = "".join(string.split(symbol))
        return string

    def undate(self):
        date = str(datetime.datetime.now())
        new_date = self.joinstring(self.joinstring(self.joinstring(date, " "), "-"), ":").split(".")[0]
        return new_date

    @list_route(methods=['post'])
    def addProduct(self, request):
        result = {"status": False, "errcode": None, "errmsg": None}
        newtime = self.undate()
        file_path = "static/images/" + request.session.get("account") + newtime + ".png"

        f1 = request.FILES.get('srcset')
        fname = '%s/%s' % (settings.MEDIA_ROOT, file_path)
        with open(fname, 'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
        try:
            product = Product(title=request.POST.get("title"),
                              sold=0,
                              money=request.POST.get("money"),
                              sell=request.session.get("account"),
                              id=int(Product.objects.all().count()) + 1,
                              stock=request.POST.get("stock"),
                              srcset="/" + file_path
                              )
            product.save()
            result["status"] = True
            result["errmsg"] = str(int(Product.objects.all().count()) + 1)
        except Exception as e:
            result["errmsg"] = str(int(Product.objects.all().count()) + 1)
        return JsonResponse(result)


class LimitedtimeViewSet(viewsets.ModelViewSet):
    queryset = Limitedtime.objects.all()
    serializer_class = LimitedtimeSerializer


def date_format(date):  # 將限時特賣的日期 格式化

    new_date = date[0:4] + "-" + date[4:6] + "-" + date[6:8] + " " + date[8:10] + ":" + date[10:12]

    return new_date


def make_id():  # 產生限時特賣的ID

    while (True):

        id = random.randrange(10000000, 99999999)

        if (Limitedtime.objects.filter(id=id).exists()):
            pass
        else:
            break

    return str(id)


def sellercenter(request):  # 賣家中心的資料
    usersForm = UsersForm()
    productForm = ProductForm()
    account = request.session.get('account')
    product_count = Product.objects.filter(sell=account).count()
    # Product.objects.filter(sell=account).delete()
    product_list = Product.objects.filter(sell=account)

    return render(request, 'sellercenter.html', locals())


def limited_item(request):  # 限時購物的商品頁面
    usersForm = UsersForm()
    productForm = ProductForm()
    return render(request, 'limited_item.html', locals())


def limited_time_sale(request):  # 限時購物的頁面
    usersForm = UsersForm()
    productForm = ProductForm()
    if 'account' in request.session:
        user = Users.objects.get(account=request.session['account'])
    else:
        user = None
    if user == None:
        return HttpResponseRedirect("請登入進行購買")
    else:
        ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'

        product_list = Limitedtime.objects.filter(starttime__lte=timezone.now(), endtime__gte=timezone.now())
        # lte小於等於 gte大於等於

    return render(request, 'limited_time_sale.html', locals())


def make_ordernumber():  # 製造出訂單的編號

    while (True):

        ordernumber = random.randrange(10000000, 99999999)
        if (Business.objects.filter(ordernumber=ordernumber).exists()):
            pass
        else:
            break

    return str(ordernumber)


def cart(request):
    usersForm = UsersForm()
    productForm = ProductForm()
    if Users.objects.filter(account=request.session['account']).exists():
        user = Users.objects.get(account=request.session['account'])
    else:
        user = None
    if user == None:
        return HttpResponse("請登入使用購物車")
    else:
        car_product_list = request.session.get("ber_car_list")
        if car_product_list:
            car_count = len(car_product_list)
        else:
            car_count = 0

    product_list = []
    buy_product_money = 0  # 紀錄購買商品的總價格
    buy_product_count = 0  # 紀錄總共買了幾個商品
    if car_product_list:
        for product in car_product_list:
            temp_product = Product.objects.get(id=product[0])
            product_list.append([temp_product, product[1], int(model_to_dict(temp_product)["money"]) * int(product[1])])
            buy_product_money += int(model_to_dict(temp_product)["money"]) * int(product[1])
            buy_product_count += int(product[1])

    return render(request, "cart.html", locals())


def search(request, keyword):
    usersForm = UsersForm()
    keyword = str(keyword)
    productForm = ProductForm()
    product = Product.objects.filter(title__contains=keyword)
    productcount = Product.objects.filter(title__contains=keyword).count()
    return render(request, "search.html", locals())


def user_confirm(request):
    productForm = ProductForm()
    return render(request, 'enable.html', locals())


def items(request, id):
    usersForm = UsersForm()
    product = Product.objects.get(id=id)
    productForm = ProductForm()
    product_count = model_to_dict(Product.objects.get(id=id)).get("stock") - model_to_dict(
        Product.objects.get(id=id)).get("sold")

    return render(request, 'item.html', locals())


def index(request):
    usersForm = UsersForm()
    productForm = ProductForm()
    return render(request, 'index.html', locals())


from common.email import user_send_mail

from common.email import user_patch_email


@csrf_exempt
def patch_email(request):
    result = {"status": False, "errcode": None, "errmsg": None}

    if request.method == "POST":

        try:
            user_email = request.POST.get("user_email")
            user_patch_email(user_email)
            result["status"] = True

        except:
            result["errcode"] = 404
            result["errmsg"] = "找不到信箱，發送失敗。"

    else:
        result["errcode"] = 400
        result["errmsg"] = "非POST請求"

    return JsonResponse(result)


def enable(reuqest, key1):
    productForm = ProductForm()
    usersForm = UsersForm()
    account = model_to_dict(SystemConfig.objects.get(key1=key1)).get("account")
    Users.objects.filter(account=account).update(confirmed=1)

    if model_to_dict(Users.objects.get(account=account)).get(confirmed=1):
        message = "帳號啟用成功"

    return render(reuqest, "enable.html", locals())
