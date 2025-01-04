from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.core.validators import FileExtensionValidator

from django.conf import settings
import base64
import os

class UserManager(BaseUserManager):
    """
        Custom user model manager where email is the unique identifiers
        for authentication instead of usernames.
    """

    def create_user(self, email, cpf, password=None, **extra_fields):
        """
            Create and return a regular user with an email, cpf and password.
        """

        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        if not cpf:
            raise ValueError('Users must have a CPF')

        user = self.model(
            email=self.normalize_email(email), cpf=cpf, **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf, password=None, **extra_fields):
        """
            Create and return a superuser with the given email, cpf and password.
        """
        
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")

        user = self.create_user(
            email, cpf, password, **extra_fields
        )

        return user
    
class User(AbstractUser):
    """
        Custom user model with email as unique identifier and first_name, 
        last_name, cpf are required. The rest of the fields are optional.
    """

    username = None

    id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    cpf = models.CharField(max_length=11, unique=True)

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    address = models.CharField(max_length=255,  blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)

    gender = models.CharField(max_length=12, blank=True, null=True)
    
    state = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    neighborhood = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    complement = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)

    birth_date = models.DateField(blank=True, null=True)

    id_description = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    #     profile_picture = models.BinaryField(blank=True, null=True)  # Save image as binary data in SQLite
    # else:
    #     profile_picture = models.ImageField(
    #         # db_column='foto perfil',
    #         blank=True,
    #         null=True,
    #         validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
    #         help_text="Upload de imagem de perfil (formatos permitidos: jpg, jpeg, png)."
    #     )

    profile_picture = models.BinaryField(
        # db_column='foto perfil',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text="Upload de imagem de perfil (formatos permitidos: jpg, jpeg, png)."
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','cpf']

    class Meta:
        db_table = "users"
        managed = True

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
