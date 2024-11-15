from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager

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

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    cpf = models.CharField(max_length=11, unique=True)

    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255,  blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)

    gender = models.CharField(max_length=12, blank=True, null=True)
    
    state = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','cpf']

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
