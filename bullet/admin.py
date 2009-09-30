from django.contrib import admin
from bullet.models import Bullet, Address, Organization, Type


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


class BulletAdmin(admin.ModelAdmin):
    search_fields = ('name', 'comment')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    #inlines = [AddressInline]

admin.site.register(Bullet, BulletAdmin)
admin.site.register(Address)
admin.site.register(Organization)
admin.site.register(Type)

