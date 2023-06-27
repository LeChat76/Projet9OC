from django.contrib import admin
from authentication.models import UserFollows


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('followed_user', 'user')

admin.site.register(UserFollows, UserFollowsAdmin)
