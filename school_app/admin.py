from django.contrib import admin
from school_app.models import SchoolSection, SchoolStudent, SchoolTeacher, School

# Register your models here.

admin.site.register([SchoolStudent, SchoolTeacher, School])


class SchoolSectionAdmin(admin.ModelAdmin):
    list_display = ("name", "standard")


admin.site.register(SchoolSection, SchoolSectionAdmin)
