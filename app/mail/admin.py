from django.contrib import admin
from .models import Mail, Message, Attachment

# Register your models here.
admin.site.register(Mail)
admin.site.register(Message)
admin.site.register(Attachment)
