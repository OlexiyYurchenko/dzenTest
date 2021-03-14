from django.contrib import admin
from articles.models import *
from mptt.admin import MPTTModelAdmin

class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20

admin.site.register(Comments, CustomMPTTModelAdmin)
