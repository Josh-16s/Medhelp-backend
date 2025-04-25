from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
            model = User
            fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                  'date_of_birth', 'gender', 'phone_number', 'adress', 
                  'emergency_contact',  'default_latitude', 'default_longitude')
            read_only_fields = ('id',)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            data.update({
                "succeeded": True,
                "message": "Login successful.",
                "user": {
                    "username": self.user.username,
                    "email": self.user.email
                }
            })
            return data
        except AuthenticationFailed as e:
            raise AuthenticationFailed({
                "succeeded": False,
                "message": str(e)
            })
        


class UpdateUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'date_of_birth', 'gender', 'phone_number', 'adress', 
            'emergency_contact', 'age', 'medical_history',
            'default_latitude', 'default_longitude'
        )
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
      
        instance.age = validated_data.get('age', instance.age)
        instance.medical_history = validated_data.get('medical_history', instance.medical_history)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.adress = validated_data.get('adress', instance.address)
        instance.emergency_contact = validated_data.get('emergency_contact', instance.emergency_contact)
        instance.save()
        return instance

   


    
class RegisterSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
        password_confirm = serializers.CharField( write_only=True, required=True)

        class Meta(object):
               model = User
               fields = ('username', 'email', 'password', 'password_confirm', 
                  'first_name', 'last_name', 'date_of_birth', 'gender')
               
        
        def validate(self, attrs):
              if attrs["password"] != attrs["password_confirm"]:
                    raise serializers.ValidationError({"password" : "The Pasword field does not match"})
              return attrs
        
        def create(self, validated_data):
               validated_data.pop('password_confirm')
               user = User.objects.create_user(**validated_data)
               return user
