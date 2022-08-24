from django.db import models
from test_app.models import Question, Test
from school_app.models import SchoolStudent
from django_minio_backend import MinioBackend
from school_app.models import SchoolStudent


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
    student = models.ForeignKey(
        SchoolStudent, on_delete=models.CASCADE, null=True, blank=True
    )
    score = models.IntegerField(null=True, blank=True)
    ansQs = models.ManyToManyField(AnsweredQuestion)
    omr_ans_sheet = models.FileField(upload_to="omr/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.test} :: {self.student_name} :: {self.score}"

    class Meta:
        db_table = "student_grades"


class AnswerSheet(models.Model):
    class statusChoices(models.TextChoices):
        ...

    image = models.FileField(
        verbose_name="test image",
        storage=MinioBackend(bucket_name="parikshana-media"),
        upload_to="test_images",
        null=True,
        blank=True,
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="answer_test")
    student = models.ForeignKey(
        SchoolStudent,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="answer_student",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0, null=True, blank=True)
    failed = models.BooleanField(default=False)
    job_id = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(
        max_length=20, null=True, choices=statusChoices, blank=True
    )

    class Meta:
        db_table = "test_answer"

    def __str__(self):
        return f"{self.test}"
