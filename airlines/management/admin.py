from django.contrib import admin
from django.contrib.admin import BooleanFieldListFilter

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.urlresolvers import reverse
from django.template.defaultfilters import escape

from management.models import Booking, Flight, Passenger, Airplane, Airport


class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('type', 'company', 'aircraft_capacity')
    search_fields = ('type', 'company', 'aircraft_capacity')


class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'state', 'country')
    search_fields = ('code', 'name', 'city', 'state', 'country')


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'image_tag', 'date_joined')
    search_fields = ('username', 'email', 'date_joined')

    def image_tag(self, obj):
        return '<img src="/static/%s" style="max-height:40px;max-width:40px">' % obj.user.photo_path.url.split('/')[-1]

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'is_active', 'user_link', 'image_tag',
                    'cell_phone_number', 'date_of_birth', 'gender')

    @staticmethod
    def first_name(obj):
        return obj.user.first_name

    @staticmethod
    def last_name(obj):
        return obj.user.last_name

    @staticmethod
    def email(obj):
        return obj.user.email

    def is_active(self, obj):
        return obj.user.is_active

    def user_link(self, obj):
        user = obj.user
        return '<a href="{}" target="_blank">{}</a>'.format(reverse("admin:auth_user_change", args=(user.id,)),
                                                            escape(user.username))

    user_link.allow_tags = True

    def image_tag(self, obj):
        return u'<img src="/static/%s" style="max-height:40px;max-width:40px">' % obj.photo_path.url.split('/')[-1]

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airplane', 'departure', 'arrival', 'departure_time', 'arrival_time',
                    'remaining_seats')
    search_fields = ('flight_number', 'airplane', 'departure', 'arrival')

    @staticmethod
    def departure(obj):
        return str(obj.departure)

    @staticmethod
    def arrival(obj):
        return str(obj.arrival)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'date_of_booking', 'flight', 'price', 'price_paid')
    list_filter = (('price_paid', BooleanFieldListFilter),)


admin.site.register(Booking, BookingAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Airplane, AirplaneAdmin)
admin.site.register(Airport, AirportAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
