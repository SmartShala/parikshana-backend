from django.contrib import admin
from school_app.models import SchoolSection, SchoolStudent, SchoolTeacher, School
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register([SchoolStudent, SchoolTeacher, School], ImportExportModelAdmin)


class SchoolSectionAdmin(
    ImportExportModelAdmin,
    admin.ModelAdmin,
):
    list_display = ("name", "standard")


admin.site.register(SchoolSection, SchoolSectionAdmin)
