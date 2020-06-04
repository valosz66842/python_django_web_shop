#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'high.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

#
# from django_mysql.models import Bit1BooleanField
# from django.db import models
# import django.utils.timezone as timezone
#     phone = models.CharField(max_length=12)
#     time = models.DateTimeField(default=timezone.now)