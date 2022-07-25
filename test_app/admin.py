from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Board)
admin.site.register(Standard)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(TestQuestionMapping)
