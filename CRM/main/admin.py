from django.contrib import admin
from main import models
# Register your models here.

admin.site.register(models.Userinfo)
admin.site.register(models.Customer)
admin.site.register(models.Campuses)
admin.site.register(models.ClassList)