from django.contrib import admin
from .models import Comedian

class ComedianAdmin(admin.ModelAdmin):
   list_display = ('username', 'inspiration', 'joke_of_the_day')
   list_per_page = 25
   readonly_fields = ('username', 'inspiration', 'joke_of_the_day')

admin.site.register(Comedian, ComedianAdmin)
