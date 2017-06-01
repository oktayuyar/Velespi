from django.db import models
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

User=get_user_model()
class UserManager(models.User):

    def validate(self, data):
        username = data["username"]
        user_gs = User.objects.filter(username=username)
        if user_gs.exists():
            raise ValidationError("Bu kullanıcı adı kullanılmaktadır.")
        return data