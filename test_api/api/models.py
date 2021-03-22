from django.db import models
from django.contrib.auth.models import User


class PurseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    money = models.IntegerField()

    def __str__(self):
        return self.name


class Transactions(models.Model):
    purse = models.ForeignKey(PurseUser, on_delete=models.CASCADE)
    money = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.purse} {self.money}'
