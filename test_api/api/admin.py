from django.contrib import admin

from .models import PurseUser, Transactions

admin.site.register(PurseUser)
admin.site.register(Transactions)
