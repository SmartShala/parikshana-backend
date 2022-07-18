from django.db import models
from test_app.models import Question, Test


class AnsweredQuestion(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answered_question"
    )
    answer = models.CharField(max_length=1, null=True, blank=True)  # A, B, C, D
    is_correct = models.BooleanField(default=False)  # True or False

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "answered_questions"


class StudentGrade(models.Model):
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="student_grades"
    )
    student_name = models.CharField(max_length=20, null=True, blank=True)
    student_id = models.CharField(max_length=120, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    ansQs = models.ManyToManyField(AnsweredQuestion, null=True, blank=True)
    omr_ans_sheet = models.FileField(upload_to="omr/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.test} :: {self.student_name} :: {self.score}"

    class Meta:
        db_table = "student_grades"
