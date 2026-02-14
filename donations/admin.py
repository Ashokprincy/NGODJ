from django.contrib import admin
from .models import Campaign

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    # 1. list_display: These become the columns in your admin table
    list_display = ('id', 'goal_amount', 'raised_amount', 'get_progress_percent')

    # 2. list_filter: Adds a sidebar to filter data (e.g., by amount)
    list_filter = ('goal_amount',)

    # 3. search_fields: Adds a search bar at the top
    # search_fields = ('title',)  # Uncomment if you have a 'title' field in models.py

    # 4. list_editable: Allows you to edit values directly from the list page
    # list_editable = ('raised_amount',)