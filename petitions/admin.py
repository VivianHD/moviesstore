from django.contrib import admin
from .models import Petition, Vote

# Register your models here.
admin.site.register(Petition)
admin.site.register(Vote)