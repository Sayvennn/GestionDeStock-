from django.contrib import admin
from .models import Employe
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(Employe)
class EmployeAdmin(UserAdmin):
     search_fields = ("username", "email")