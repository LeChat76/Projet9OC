from django.contrib import admin

from www.models import Ticket, Review

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'body', 'user')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
