from django.contrib import admin
from .models import details, comments, check_in_data

# Register your models here.
admin.site.register(details)
admin.site.register(comments)
admin.site.register(check_in_data)