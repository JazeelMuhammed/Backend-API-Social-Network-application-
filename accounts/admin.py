from django.contrib import admin
from .models import UserProfile, Connection

# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Connection)