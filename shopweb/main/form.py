from django import forms
from .models import Users,Business,Product

class UsersForm(forms.ModelForm):
    class Meta:
        model=Users
        fields=['phone','email','name','account','password']
        widgets={
            'account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '使用者帳號'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '手機'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '電子信箱'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密碼'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名'})
        }
class BusinessForm(forms.ModelForm):
    class Meta:
        model=Business
        fields=['buyer','seller','totalprice','amount','product_id','ordernumber']
        widgets={
            'buyer':forms.TextInput(),
            'seller': forms.TextInput(),
            'amount':forms.TextInput(),
            'product_id':forms.TextInput(),
            'totalprice':forms.TextInput(),
            'ordernumber':forms.TextInput()
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = ['title','money','stock','srcset']
        widgets={
            'title':forms.TextInput(attrs={'class': 'form-control','placeholder': '商品標題'}),
            'money':forms.TextInput(attrs={'class': 'form-control','placeholder': '商品售價'}),
            'stock':forms.TextInput(attrs={'class': 'form-control','placeholder':'庫存數量'}),
            'srcset': forms.TextInput(attrs={'type': "file", 'placeholder': '商品圖片'})
        }