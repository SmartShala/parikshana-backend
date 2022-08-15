from django.db import models
from user.models import User
from test_app.models import Subject, Standard
from django_minio_backend import MinioBackend

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="school_created_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "school"

    def __str__(self):
        return self.name


class SchoolTeacher(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="school_teacher_school",
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="school_teacher_teacher",
    )
    subjects = models.ManyToManyField(Subject, related_name="school_teacher_subjects")
    standards = models.ManyToManyField(
        Standard, related_name="school_teacher_standards"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "school_teacher"

    def __str__(self):
        return f"{self.teacher}"


class SchoolStudent(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    std_id = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    image = models.FileField(
        verbose_name="Object Upload",
        storage=MinioBackend(bucket_name="parikshana-media"),
        upload_to="teacher_images",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "school_student"

    def __str__(self):
        return f"{self.name}: {self.age}: {self.std_id}: {self.sex}"


class SchoolClass(models.Model):
    description = models.TextField(null=True, blank=True)
    standard = models.ForeignKey(
        Standard,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="school_class_standard",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="school_class_subject",
    )
    teachers = models.ManyToManyField(
        User,
        related_name="school_class_teachers",
    )
    students = models.ManyToManyField(
        SchoolStudent,
        related_name="school_class_students",
    )

    class Meta:
        db_table = "school_class"

    def __str__(self):
        return f"{self.standard} {self.subject}"
