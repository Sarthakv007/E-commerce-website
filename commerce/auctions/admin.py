from django.contrib import admin
from .models import User, Brand, Listings, Comment, Bid
# Register your models here.

admin.site.register(User)
admin.site.register(Brand)
admin.site.register(Listings)
admin.site.register(Comment)
admin.site.register(Bid)
