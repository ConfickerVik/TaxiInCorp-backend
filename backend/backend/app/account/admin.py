from django.contrib import admin
from .models import User, UserRole, Car

# Register your models here.
admin.register(User)
admin.register(UserRole)
admin.register(Car)
