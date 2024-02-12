from django.contrib import admin
from .models import Custom_User, DataModel, Tag

# Register your models here.


admin.site.register(Custom_User)
admin.site.register(DataModel)
admin.site.register(Tag)