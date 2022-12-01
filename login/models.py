from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, username, password, email, name, subject, **extra_fields):
        if not username:
            raise ValueError('username Required!')

        user = self.model(
            username = username,
            email = email,
            name = name,
            subject = subject,           
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None, name=None, subject=None):

        user = self.create_user(username, password, email, name, subject)

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True

        user.save(using=self._db)
        return user

class User(AbstractUser):
    objects = UserManager()

    username = models.CharField(max_length=20, null=True, unique=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)  
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50, null=True)
    subject = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.name}({self.subject})'

    class Meta:
        db_table = "user"