from django.contrib import admin
from .models import Course,Unit,Chapter,Question


# Register your models here.

admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Chapter)
admin.site.register(Question)
