from django.db import models, transaction
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
import uuid
from django.utils import timezone
from django_minio_backend import MinioBackend

# Create your models here.


class Role(models.Model):
    IS_SUPERADMIN = 1
    IS_TEACHER = 2
    IS_ADMIN = 3

    ROLE_CHOICES = (
        (IS_SUPERADMIN, "superadmin"),
        (IS_TEACHER, "teacher"),
        (IS_ADMIN, "admin"),
    )
    ROLES_CHOICES = (
        ("SUPERADMIN", "is_superadmin"),
        ("TEACHER", "is_teacher"),
        ("ADMIN", "is_admin"),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
    name = models.CharField(max_length=50, choices=ROLES_CHOICES, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("roles_id", 1)

        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, default="abc@xyz.com")
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, default=2)
    contact = models.BigIntegerField(default=0, unique=True, blank=True, null=True)
    teacher_id = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    image = models.FileField(
        verbose_name="User Image",
        storage=MinioBackend(bucket_name="parikshana-media"),
        upload_to="student_images",
        null=True,
        blank=True,
    )
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return str(self.email)

    class Meta:
        ordering = ["-date_joined"]
