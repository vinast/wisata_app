from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import uuid

ROLE_CHOICES = [
    ('super_admin', 'Super Admin'),
    ('admin_prov', 'Admin Provinsi'),
    ('admin_kab', 'Admin Kabupaten')
]

class Master_UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, phone, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not phone:
            raise ValueError('The Phone field must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', False)
        return self._create_user(email, username, phone, password, **extra_fields)

    def create_superuser(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_verified') is not True:
            raise ValueError('Superuser must have is_verified=True.')

        return self._create_user(email, username, phone, password, **extra_fields)

class CreateUpdateTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    archive_at = models.DateTimeField(default=None, null=True)
    deleted_at = models.DateTimeField(default=None, null=True)

    class Meta:
        abstract = True

class Tahun(models.Model):
    tahun = models.IntegerField(default=2024)

    class Meta:
        abstract = True

class Master_User(AbstractBaseUser, CreateUpdateTime):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=50)
    full_name = models.CharField(max_length=50)
    alamat = models.TextField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='images/avatar/', default='images/avatar/default_avatar.png')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    email_verification_token = models.CharField(max_length=100, default='')

    objects = Master_UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone', 'role', 'is_superuser']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
