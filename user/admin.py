from django.contrib import admin
from .models import User, Role


class UserAdminView(admin.ModelAdmin):
    list_display = ("name", "email", "contact", "teacher_id", "date_joined", "id")


admin.site.register(User, UserAdminView)
admin.site.register(Role)
