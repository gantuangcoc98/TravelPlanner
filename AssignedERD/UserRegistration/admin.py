from django.contrib import admin
from .models import User, Destination, BookOrder

# Register your models here.
admin.site.register(User)
admin.site.register(Destination)
admin.site.register(BookOrder)
