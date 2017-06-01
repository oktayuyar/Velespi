from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User=get_user_model()

class  UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username","password","email" )
        #extra_kwargs={
         #   "password" :{
         #       "write_only" :True}
         #       }

    def validate(self, data):
        username=data["username"]
        user_gs=User.objects.filter(username=username)
        if user_gs.exists():
            raise ValidationError("Bu kullanıcı adı kullanılmaktadır.")
        return data

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


