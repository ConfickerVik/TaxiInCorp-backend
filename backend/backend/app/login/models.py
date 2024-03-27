import datetime

from django.db import models
from django.core.validators import RegexValidator
from django.contrib import auth
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self.model(
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class UserRole(models.Model):
    ROLE_CHOICES = (
        (1, "Passenger"),
        (2, "Driver")
    )
    role = models.IntegerField(choices=ROLE_CHOICES)


class User(AbstractUser):
    phone_regex = RegexValidator(regex=r"^(\+7|8)\d{10}$",
                                 message="Телефонный номер должен быть введен в формате +7(8)xxxxxxxxxx")
    phone_number = models.CharField(max_length=12, unique=True, validators=[phone_regex])

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    about_info = models.TextField(max_length=500, blank=True)
    # date_joined   comes with AbstractBaseUser

    fk_role = models.ForeignKey(
        UserRole,
        on_delete=models.DO_NOTHING,
        db_column="fk_role",
        default=lambda: UserRole.objects.get(id=1)
    )

    objects = CustomManager()
    username = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name", "about_info"]


class Car(models.Model):
    car_brand = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50, blank=True)
    car_color = models.CharField(max_length=50, blank=True)

    plate_regex = RegexValidator(
        regex=r'^[АВЕКМНОРСТУХABEKMHOPCTYX]\d{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2} \d{2}$',
        message='Введите номер автомобиля в формате <X666XX 69> латинскими или русскими буквами'
    )
    car_plate = models.CharField(max_length=9, unique=True, validators=[plate_regex])

    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='fk_user')
