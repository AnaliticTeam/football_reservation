from django.contrib import admin
from .models import Stadium, Reservation, Payment,ApiUrls

admin.site.register(Stadium)
admin.site.register(Reservation)
admin.site.register(Payment)
admin.site.register(ApiUrls)