from rest_framework import serializers
from .models import Color, Person
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100, min_length=4, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        max_length=100, min_length=4, required=True)  
    class Meta:
        model = User
        fields = ('username', 'email', 'password') 

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username already exists")
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("Email already exists")
        return data
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']          
        )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'colors_name']


class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    country = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'

    def get_country(self, obj):
        color_obj = Color.objects.get(id=obj.color.id)
        return {'color_name': color_obj.colors_name, 'hex_code': '#000'}

    def validate(self, data):
        if data['age'] < 18:
            raise serializers.ValidationError("Age should be greater than 18")
        return data
