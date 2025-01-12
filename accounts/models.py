from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import date
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, phone_number, address, dob, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            dob=dob,
        )

        user.set_password(password)
        user.save(using=self._db)


        Profile.objects.get_or_create(user=user)

        return user

    def create_superuser(self, email, username, first_name, last_name, phone_number, address, dob, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            dob=dob,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


        Profile.objects.get_or_create(user=user)

        return user

class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=100, default='Enter Address')
    dob = models.DateField(default=date(2000, 1, 1))
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'address', 'phone_number', 'dob']

    objects = MyAccountManager()

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    coins = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}'s profile with {self.coins} coins"

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            try:
                Profile.objects.create(user=instance)
            except IntegrityError:

                pass

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_short_name(self):
        return self.user.first_name
