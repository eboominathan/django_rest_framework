from rest_framework import serializers
from .models import Color, Person

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id','colors_name']

class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    class Meta:
        model = Person
        fields = '__all__'

    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError("Age should be greater than 18")
        return data
