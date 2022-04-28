from django.contrib import admin
from .models import Thread, PersonalMessage
# Register your models here.

admin.site.register(Thread)
admin.site.register(PersonalMessage)