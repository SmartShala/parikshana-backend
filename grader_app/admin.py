from django.contrib import admin
from grader_app.models import * 
# Register your models here.

admin.site.register(AnsweredQuestion)
admin.site.register(StudentGrade)
admin.site.register(AnswerSheet)