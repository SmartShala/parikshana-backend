from django.db import models
from user.models import User
from django.contrib.postgres.fields import ArrayField
from django_minio_backend import MinioBackend


class Board(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "educational_boards"


class Standard(models.Model):
    name = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "class_standards"


class Subject(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "subjects"


class Topic(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="topic_subject"
    )
    standard = models.ForeignKey(
        Standard, on_delete=models.CASCADE, related_name="topic_standard"
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="topic_board",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "topics"


from school_app.models import SchoolSection


class Test(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    topic = models.ForeignKey(
        Topic,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="test_topic",
    )

    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="test_created_by",
    )
    section = models.ForeignKey(
        SchoolSection,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="test_section",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pending = models.BooleanField(default=True)
    is_shuffled = models.BooleanField(default=False)
    test_question_pdf = models.FileField(
        verbose_name="test papers",
        storage=MinioBackend(bucket_name="parikshana-media"),
        upload_to="test_papers",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tests"


class Question(models.Model):
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="test_question", null=True
    )
    question = models.CharField(max_length=250, null=True, blank=True)
    options = ArrayField(
        models.CharField(max_length=50, null=True, blank=True),
        size=4,
        null=True,
    )
    correct_option = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True
    )  # 0,1,2,3
    marks = models.IntegerField(default=1, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question}"

    class Meta:
        db_table = "question_bank"
