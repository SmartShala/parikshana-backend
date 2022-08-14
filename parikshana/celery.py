# parikshana/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parikshana.settings")
app = Celery("parikshana_broker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
