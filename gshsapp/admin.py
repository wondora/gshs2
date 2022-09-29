from django.contrib import admin
from .models import Gubun, User, Buyproduct, Location, Gigiinfo, Repair, Replacement 

admin.site.register(User)
admin.site.register(Buyproduct)
admin.site.register(Location)
admin.site.register(Gigiinfo)
admin.site.register(Repair)
admin.site.register(Gubun)
admin.site.register(Replacement)
