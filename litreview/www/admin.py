from django.contrib import admin

from www.models import Ticket, Review, UserFollows

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review)
admin.site.register(UserFollows)

