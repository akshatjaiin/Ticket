from django.contrib import admin
from .models import User, Ticket

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0  # No extra empty forms will be displayed by default

class UserAdmin(admin.ModelAdmin):
    inlines = [TicketInline]

admin.site.register(User, UserAdmin)
admin.site.register(Ticket)
