from django.contrib import admin

from user_model.models import User, Account, Address, Fullname

# Register your models here.

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Address)
admin.site.register(Fullname)
