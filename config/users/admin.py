from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')  # Show in list view
    search_fields = ('user__username', 'phone_number')  # Enable search
    list_editable = ('phone_number',)  # Make phone number editable in list view

admin.site.register(Profile, ProfileAdmin)