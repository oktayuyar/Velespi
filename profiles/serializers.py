from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField

User=get_user_model()

class  UserSerializer(serializers.ModelSerializer):
    email=EmailField(label="E-Posta Adresi")
    class Meta:
        model = User
        fields = ("id", "username","password","email" )
        extra_kwargs={
            "password" :{
                "write_only" :True}
               }


    def create(self, validated_data):
        username=validated_data["username"]
        password=validated_data["password"]
        email=validated_data["email"]
        user_obj=User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class  UserLoginSerializer(serializers.ModelSerializer):
    token=CharField(allow_blank=True,read_only=True)
    username=CharField(label="Kullanıcı Adı")
    password = serializers.CharField(label="Parola",
    style={'input_type': 'password'}
    )
    class Meta:
        model = User
        fields = ("id", "username","password","token")
        extra_kwargs={
            "password" :{
                "write_only" :True}
               }

    def validate(self, data):
        username = data["username"]
        password = data["password"]
        user_obj = User(
            username=username,
        )
        user_obj.set_password(password)
        return data
