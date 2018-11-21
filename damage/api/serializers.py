
from rest_framework import serializers
from damage.models import Damage


class DamageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Damage
        fields = [
            'firstname',
            'lastname',
            'address',
            'email',
            'mobile',
            'damagetype']
        read_only_fields=['email']


    def validate_mobile(self, value):
        if value == '123':
            raise serializers.ValidationError('Oxi 123')
        else:
            return value