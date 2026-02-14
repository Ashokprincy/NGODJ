from django.contrib import admin
from .models import Campaign # The dot means "look in the same folder"

admin.site.register(Campaign)