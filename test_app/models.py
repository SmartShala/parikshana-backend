from django.db import models
from user.models import User


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


class Question(models.Model):
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="question_topic"
    )
    question = models.CharField(max_length=250, null=True, blank=True)
    options = models.JSONField(default=dict, null=True, blank=True)
    correct_option = models.CharField(max_length=1, null=True, blank=True)  # A,B,C,D
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="question_created_by"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="question_updated_by",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question}"

    class Meta:
        db_table = "question_bank"


from school_app.models import SchoolSection


class Test(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    topic = models.ForeignKey(Topic, null=True, blank=True, on_delete=models.CASCADE)

    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    questions = models.ManyToManyField(
        Question, blank=True, related_name="test_questions"
    )

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

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tests"


class TestQuestionMapping(models.Model):
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="test_mapping"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_mapping"
    )
    marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.test} : {self.question}"

    class Meta:
        db_table = "test_question_mapping"
