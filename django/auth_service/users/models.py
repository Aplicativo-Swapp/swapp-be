from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, cpf, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        if not password:
            raise ValueError('Users must have a password')
        
        if not cpf:
            raise ValueError('Users must have a CPF')

        user = self.model(
            email=self.normalize_email(email), cpf=cpf,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(
            email, cpf, password, **extra_fields
        )

        return user
    
class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    cpf = models.CharField(max_length=11, unique=True)

    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255,  blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)

    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
