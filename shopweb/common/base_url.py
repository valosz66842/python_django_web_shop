import os

if os.name=="nt":
    base_url="http://127.0.0.1:8000/"
elif os.name=="posix":
    base_url = "http://shop.com/"
# from main.form import UserForm
