from hackday.users.models import Tshirt, Diet, Location, UserProfile
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'diet', 'tshirt', 'notify_by_email',
                    'dinner_required', 'breakfast_required', 'create_date')
    list_filter = ('location', 'tshirt', 'diet', 'dinner_required',
                   'breakfast_required', 'create_date')

admin.site.register(Tshirt)
admin.site.register(Diet)
admin.site.register(Location)
admin.site.register(UserProfile, UserProfileAdmin)
