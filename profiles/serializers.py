from django.contrib.auth import get_user_model
from rest_framework import serializers

User=get_user_model()

class  UserSerializer(serializers.ModelSerializer):
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


