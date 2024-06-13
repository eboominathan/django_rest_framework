from rest_framework import serializers
from .models import Color, Person


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id','colors_name']

class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    country = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'        
     
    def get_country(self, obj):     
        color_obj = Color.objects.get(id=obj.color.id)
        return {'color_name':color_obj.colors_name,'hex_code':'#000'}
     
    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError("Age should be greater than 18")
        return data
    
