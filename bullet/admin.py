from django.contrib import admin
from bullet.models import *


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


class BulletAdmin(admin.ModelAdmin):
    search_fields = ('name', 'comment')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    #inlines = [AddressInline]

admin.site.register(Address)
admin.site.register(Organization)
admin.site.register(EmailChannel)
admin.site.register(TwitterChannel)
admin.site.register(Bulletin)
admin.site.register(BulletinEdition)
admin.site.register(Event)

