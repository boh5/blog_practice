from django.contrib import admin

from account.models import UserProfile, UserInfo


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth', 'phone']
    list_filter = ['phone']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserInfo)
