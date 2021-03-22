from rest_framework import serializers
from .models import PurseUser, Transactions


class PurseSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return PurseUser.objects.create(**self.initial_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', None)
        instance.save()
        return instance

    class Meta:
        model = PurseUser
        exclude = ('user', )


class TransactionsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Transactions.objects.create(**self.initial_data)

    class Meta:
        model = Transactions
        fields = ['purse', 'money', 'date', 'comment']
